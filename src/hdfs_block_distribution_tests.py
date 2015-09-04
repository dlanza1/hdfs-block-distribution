import unittest
from hdfs_block_distribution import processArgs, BadArguments

class HdfsBlockDistributionTests(unittest.TestCase):
    
    def test_processArgs(self):
        self.assertRaises(BadArguments, processArgs, [])
    
        options = processArgs(['-d', '/user/'])
        self.assertEqual(options.dir, '/user/')
        
        options = processArgs(['-d', '/user/', '-w', '23', '-e', '64'])
        self.assertEqual(options.dir, '/user/')
        self.assertEqual(options.perc_warn, '23')
        self.assertEqual(options.perc_err, '64')
        
        self.assertRaises(BadArguments, processArgs, ['-d', '/user/', '-w', 'ds'])
        self.assertRaises(BadArguments, processArgs, ['-d', '/user/', '-e', 'ds'])
        
if __name__ == "__main__":
    unittest.main()