from utils import *
from colors import *
from optparse import OptionParser
import sys

class BadArguments(Exception):
    def __init__message(self, message):
        self.value = message
    def __str__(self):
        return self.message
    
def representsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def processArgs(arguments):    
    parser = OptionParser()
    parser.add_option("-d", "--dir", 
                      help="directory to be analyzed (mandatory)", 
                      metavar="PATH")
    parser.add_option("-w", "--perc_warn", 
                      help="percentage to use for coloring number of blocks in yellow (def=20)", 
                      default="20",
                      metavar="(0 - 100)")
    parser.add_option("-e", "--perc_err", 
                      help="percentage to use for coloring number of blocks in red (def=50)", 
                      default="50",
                      metavar="(0 - 100) ")

    (options, args) = parser.parse_args(args=arguments)
    
    if not options.dir:
        raise BadArguments("Directory must be specified with -d argument.")
    
    if not representsInt(options.perc_warn):
        raise BadArguments("-w argument must be an integer number.")
    if not representsInt(options.perc_err):
        raise BadArguments("-e argument must be an integer number.")
        
    if len(args) > 0:
        print color("WARNING: You have specified arguments which have not been processed:" + repr(args), colors.Y)
    
    return options

def main():
    try:
        options = processArgs(sys.argv)
    except BadArguments as e:
        print e
        sys.exit()
    
    command = 'hdfs fsck ' + options.dir + ' -files -blocks -locations'
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