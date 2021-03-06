import unittest
from utils import *

class UtilsTests(unittest.TestCase):
    
    def test_filter_block_lines(self):
        lines = []
        lines.append('1. ABCDEF');
        lines.append('. ABCDEF');
        lines.append('1 ABCDEF');
        lines.append('1.ABCDEF');
        lines.append(' ABCDEF');
        lines.append('ABCDEF');
        
        filtered_lines, other_lines = filter_block_lines(lines)
        
        self.assertEqual(filtered_lines[0], lines[0])
        self.assertEqual(len(filtered_lines), 1)
        
        self.assertEqual(len(other_lines), 5)

    def test_get_host_and_storage_id_tuples(self):
        lines = []
        lines.append('0. BP-2054394024:blk_1073853666 len=527 repl=3 '
                     '[DatanodeInfoWithStorage[128.142.210.238:1004,DS-bf6e5475,DISK], '
                     'DatanodeInfoWithStorage[128.142.210.234:1004,DS-09a26b31,DISK]]');
        lines.append('10. BP-2054394024:blk_1073853666 len=527 repl=3 '
                     '[DatanodeInfoWithStorage[128.142.210.200:1004,DS-c30988a4,DISK]]');
        
        tuples = get_host_and_storage_id_tuples(lines)
        
        self.assertEqual(tuples[0][0], '128.142.210.238:1004')
        self.assertEqual(tuples[0][1], 'DS-bf6e5475')
        self.assertEqual(tuples[1][0], '128.142.210.234:1004')
        self.assertEqual(tuples[1][1], 'DS-09a26b31')
        self.assertEqual(tuples[2][0], '128.142.210.200:1004')
        self.assertEqual(tuples[2][1], 'DS-c30988a4')
        
    def test_fill_matrix(self):
        tuples = []
        tuples.append(['h1:10', 's1'])
        tuples.append(['h1:10', 's1'])
        tuples.append(['h2:10', 's1'])
        tuples.append(['h2:10', 's2'])
        
        matrix = fill_matrix(tuples)
        
        self.assertEqual(matrix['h1:10'].storages['s1'].blocks, 2)
        self.assertEqual(matrix['h2:10'].storages['s1'].blocks, 1)
        self.assertEqual(matrix['h2:10'].storages['s2'].blocks, 1)
        
if __name__ == "__main__":
    unittest.main()
