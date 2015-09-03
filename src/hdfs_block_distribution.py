from utils import *
from colors import *
import sys

def processArgs():
    if len(sys.argv) != 2:
        print 'An argument must be specified indicating the HDFS directory to analyze'
        sys.exit()

    return sys.argv[1]

def main():
    directory = processArgs()
    
    command = 'hdfs fsck ' + directory + ' -files -blocks -locations'
    output = run_command(command)

    block_lines, other_lines = filter_block_lines(output)
    
    for line in other_lines:
        print color(line, colors.Y)
    
    tuples = get_host_and_storage_id_tuples(block_lines)
    matrix = fill_matrix(tuples)

    # Show results
    show_matrix(matrix)
    show_total_blocks_per_host(matrix)

if __name__ == '__main__':
    main()