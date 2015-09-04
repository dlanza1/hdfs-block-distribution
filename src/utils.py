import subprocess
import re
from host import Host

def run_command(command):
    "Run command line"
    p = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')

def filter_block_lines(lines):
    "Return only lines which represent blocks"
    block_lines = []
    other_lines = []
    block_line_regx = re.compile('\d+[.]\s')
    directory_regx = re.compile('/')

    for line in lines:
        if block_line_regx.match(line):
            block_lines.append(line)
        elif directory_regx.match(line) is None and len(line) > 4:
            other_lines.append(line)
            
    return block_lines, other_lines

def get_host_and_storage_id_tuples(block_lines):
    "Get list of tuples with host and storage id"
    tuples = []
    p = re.compile('DatanodeInfoWithStorage')
  
    for line in block_lines:
        for replica in p.finditer(line):
            start_idx = replica.end() + 1
            end_idx = block_lines[0].find('\]', start_idx)
            fields = line[start_idx:end_idx].split(",")
            tuples.append([fields[0], fields[1]])

    return tuples

def fill_matrix(pairs):
    "Fill a matrix of host x storage with the number of blocks"
    hosts = {}

    for pair in pairs:
        host = pair[0]
        storage = pair[1]  
    
        if not hosts.has_key(host):
            hosts[host] = Host(host)
        hosts[host].addBlock(storage)

    return hosts

def representsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False