from utils import *
from colors import *
from optparse import OptionParser
import sys

class BadArguments(Exception):
    """Arguments were not specified properly"""
    
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
        
    if len(args) > 1:
        print color("WARNING: You have specified arguments which have not been processed: " + repr(args[1:]), colors.Y)
    
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
    hosts = fill_matrix(tuples)

    # Show results
    perc_warn = float(options.perc_warn) / 100
    perc_err = float(options.perc_err) / 100
    for host in hosts.itervalues():
        print 'Host: %s' % (host.hostname)
        print host.blocksPerDiskAsColouredString(perc_warn, perc_err)
        print
    
    for host in hosts.itervalues():
        print "Host %s: %d blocks" % (host.hostname, host.totalBlocks())

if __name__ == '__main__':
    main()