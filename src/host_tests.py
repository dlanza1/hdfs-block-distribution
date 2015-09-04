import unittest
from host import Host

class HostTest(unittest.TestCase):
    
    def setUp(self):
        self.host = Host('188.184.9.234:1000')
        self.host.addBlock('s1')
        self.host.addBlock('s1')
        self.host.addBlock('s2')
        self.host.addBlock('s2')
        self.host.addBlock('s3')

    def testHostname(self):
        self.assertEqual(self.host.hostname, 'webrlb01.cern.ch')
        
        host = Host('288.184.9.234:1000')
        self.assertEqual(host.hostname, '288.184.9.234')

    def test_addBlock(self):
        self.assertEqual(self.host.storages['s1'].blocks, 2)
        self.assertEqual(self.host.storages['s2'].blocks, 2)
        self.assertEqual(self.host.storages['s3'].blocks, 1)
        
    def test_blocksPerDiskAsString(self):
        self.assertEqual(self.host.blocksPerDiskAsString(), '1 2 2 ')
        
    def test_totalBlocks(self):
        self.assertEqual(self.host.totalBlocks(), 5)
        
    def test_avgBlocks(self):
        self.assertAlmostEqual(self.host.avgBlocks(), 1.66666, 4)

if __name__ == "__main__":
    unittest.main()