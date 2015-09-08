import socket
import os
import subprocess
from pkgutil import get_data
from colors import *

class Storage:
    
    def __init__(self, id):
        self.id = id
        self.blocks = 0
        self.folder = 'unknown'
        
    def addBlock(self):
        self.blocks += 1

class Host:
    
    def __init__(self, host_port):
        fileds = host_port.split(':')
        self.ip = fileds[0]
        self.port = int(fileds[1])
        self.storages = {}
        
        try:
            self.hostname = self.resolveHostname(self.ip)
        except socket.error:
            self.hostname = self.ip
         
    def resolveHostname(self, ip):
        return socket.gethostbyaddr(ip)[0]
    
    def addBlock(self, storageID):
        if not self.storages.has_key(storageID):
            self.storages[storageID] = Storage(storageID)
        
        self.storages[storageID].addBlock()
            
    def blocksPerDiskAsString(self):
        string = ''
        for storage in self.storages.itervalues():
            string += str(storage.blocks) + ' '
        return string
    
    def blocksPerDiskAsColouredString(self, perc_warn, perc_err):
        avg = self.avgBlocks()
        
        yellow_max = avg * (1 + perc_err)
        green_max = avg * (1 + perc_warn)
        green_min = avg * (1 - perc_warn)
        yellow_min = avg * (1 - perc_err)
        
        string = ''
        for storage in self.storages.itervalues():
            if storage.blocks < green_max and storage.blocks > green_min:
                string += color(storage.blocks, colors.G) + ' '
            elif storage.blocks < yellow_max and storage.blocks > yellow_min:
                string += color(storage.blocks, colors.Y) + ' '
            else:
                string += color(storage.blocks, colors.R) + ' '
            
        return string
    
    def totalBlocks(self):
        total = 0
        for storage in self.storages.itervalues():
            total += storage.blocks
        return total
    
    def avgBlocks(self):
        return float(self.totalBlocks()) / len(self.storages)
    
    def get_map_storageid_folder(self):
        remote_script = get_data('scripts', 'map_storageid_folder.sh')
        ssh_command = 'ssh root@' + self.hostname
        
        print 'SSHing for getting folders (root access is required): %s' %(ssh_command)
        print
        
        devnull = open(os.devnull, 'wb')
        p_ssh = subprocess.Popen(ssh_command.split(), 
                                 stdin=subprocess.PIPE, 
                                 stdout=subprocess.PIPE,
                                 stderr=devnull)
        p_ssh.stdin.write(remote_script)
        p_ssh.stdin.close()
        
        return iter(p_ssh.stdout.readline, b'')

    def fill_storage_folders(self):
        output = self.get_map_storageid_folder()
        
        for line in output:
            try:
                fields = line.split(',')
                self.storages[fields[0]].folder = fields[1].rstrip()
            except Exception:
                pass
    
    def showDetailedInfo(self, perc_warn, perc_err):
        print color("Detailed information for %s" % (self.hostname), colors.U)
        print
        
        avg = self.avgBlocks()
        
        yellow_max = avg * (1 + perc_err)
        green_max = avg * (1 + perc_warn)
        green_min = avg * (1 - perc_warn)
        yellow_min = avg * (1 - perc_err)
        
        self.fill_storage_folders()
        
        for storage in self.storages.itervalues():
            if storage.blocks < green_max and storage.blocks > green_min:
                nums = color(storage.blocks, colors.G)
            elif storage.blocks < yellow_max and storage.blocks > yellow_min:
                nums = color(storage.blocks, colors.Y)
            else:
                nums = color(storage.blocks, colors.R)
                
            print 'StorageID: %s' % (storage.id)
            print '\tFolder: %s' % (storage.folder)
            print '\tNumber of blocks: %s' % (nums)
            print
        

        
        
        
        
