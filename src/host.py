import socket
from colors import *

class Host:
    
    def __init__(self, host_port):
        fileds = host_port.split(':')
        self.ip = fileds[0]
        self.port = int(fileds[1])
        self.blocks_per_disk = {}
        
        try:
            self.hostname = self.resolveHostname(self.ip)
        except socket.error:
            self.hostname = self.ip
         
    def resolveHostname(self, ip):
        return socket.gethostbyaddr(ip)[0]
    
    def addBlock(self, storageID):
        if not self.blocks_per_disk.has_key(storageID):
            self.blocks_per_disk[storageID] = 1
        else:
            self.blocks_per_disk[storageID] += 1
            
    def blocksPerDiskAsString(self):
        string = ''
        for num in self.blocks_per_disk.itervalues():
            string += str(num) + ' '
        return string
    
    def blocksPerDiskAsColouredString(self, perc_warn, perc_err):
        avg = self.avgBlocks()
        
        yellow_max = avg * (1 + perc_err)
        green_max = avg * (1 + perc_warn)
        green_min = avg * (1 - perc_warn)
        yellow_min = avg * (1 - perc_err)
        
        string = ''
        for num in self.blocks_per_disk.itervalues():
            if num < green_max and num > green_min:
                string += color(num, colors.G) + ' '
            elif num < yellow_max and num > yellow_min:
                string += color(num, colors.Y) + ' '
            else:
                string += color(num, colors.R) + ' '
            
        return string
    
    def totalBlocks(self):
        total = 0
        for num in self.blocks_per_disk.itervalues():
            total += num
        return total
    
    def avgBlocks(self):
        return float(self.totalBlocks()) / len(self.blocks_per_disk)
    
    def showDetailedInfo(self, perc_warn, perc_err):
        print "Detailed information of %s" % (self.hostname)
        
        avg = self.avgBlocks()
        
        yellow_max = avg * (1 + perc_err)
        green_max = avg * (1 + perc_warn)
        green_min = avg * (1 - perc_warn)
        yellow_min = avg * (1 - perc_err)
        
        for sid, num in self.blocks_per_disk.iteritems():
            if num < green_max and num > green_min:
                nums = color(num, colors.G)
            elif num < yellow_max and num > yellow_min:
                nums = color(num, colors.Y)
            else:
                nums = color(num, colors.R)
                
            print 'Storage: %s' % (sid)
            print '\tStorageID: %s' % (sid)
            print '\tNumber of blocks: %s' % (nums)
        
        
        
        
        
        
        
