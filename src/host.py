import socket

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
    
    def totalBlocks(self):
        total = 0
        for num in self.blocks_per_disk.itervalues():
            total += num
        return total
    
    def avgBlocks(self):
        return float(self.totalBlocks()) / len(self.blocks_per_disk)