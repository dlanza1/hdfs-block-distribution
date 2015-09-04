import socket
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
    
    def showDetailedInfo(self, perc_warn, perc_err):
        print "Detailed information of %s" % (self.hostname)
        
        avg = self.avgBlocks()
        
        yellow_max = avg * (1 + perc_err)
        green_max = avg * (1 + perc_warn)
        green_min = avg * (1 - perc_warn)
        yellow_min = avg * (1 - perc_err)
        
        for sid, storage in self.storages.iteritems():
            if storage.blocks < green_max and storage.blocks > green_min:
                nums = color(storage.blocks, colors.G)
            elif storage.blocks < yellow_max and storage.blocks > yellow_min:
                nums = color(storage.blocks, colors.Y)
            else:
                nums = color(storage.blocks, colors.R)
                
            print 'StorageID: %s' % (storage.id)
            print '\tFolder: %s' % (storage.folder)
            print '\tNumber of blocks: %s' % (storage.blocks)
            print
        
        
        
        
        
        
        
