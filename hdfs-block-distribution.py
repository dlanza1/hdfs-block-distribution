import subprocess
import re

def run_command(command):
  p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  return iter(p.stdout.readline, b'')

def filter_block_lines(lines):
  block_lines = []
  regex = re.compile('\d+[.]\s')

  for line in lines:
    print line
    if regex.match(line):
      block_lines.append(line)

  return block_lines

def get_host_and_storage_id_tuples(block_lines):
  tuples = []
  p = re.compile('DatanodeInfoWithStorage')
  
  for line in block_lines:
    for replica in p.finditer(line):
      start_idx = replica.end() + 1
      end_idx = block_lines[0].find(']', start_idx)
      fields = line[start_idx:end_idx].split(",")
      tuples.append([fields[0], fields[1]])

  return tuples

def fill_matrix(tuples):
  hosts = {}

  for tuple in tuples:
    host = tuple[0]
    storage = tuple[1]
    if not hosts.has_key(host):
      hosts[host] = {}  
    
    if hosts[host].has_key(storage):
       hosts[host][storage] += 1
    else:
       hosts[host][storage] = 1

  return hosts

def show_total_per_host(matrix):
  for host_name, values in matrix.iteritems():
    total = 0
    for key, value in values.iteritems():
      total += value
    print "Host %s: %d blocks" % (host_name, total)

def show_matrix(matrix):
  for host_name, values in matrix.iteritems():
    line = ""
    print host_name
    for key, value in values.iteritems():
      line = line + str(value) + " "

    print line

command = 'hadoop fsck / -files -blocks -locations'.split()
block_lines = filter_block_lines(run_command(command))
tuples = get_host_and_storage_id_tuples(block_lines)
matrix = fill_matrix(tuples)
#show_matrix(matrix)
show_total_per_host(matrix)