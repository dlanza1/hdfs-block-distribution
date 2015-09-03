from utils import *

def main():
    # Run command
    command = 'hdfs fsck /user/ -files -blocks -locations'
    output = run_command(command)

    # Compute output
    block_lines = filter_block_lines(output)
    tuples = get_host_and_storage_id_tuples(block_lines)
    matrix = fill_matrix(tuples)

    # Show results
    show_matrix(matrix)
    show_total_blocks_per_host(matrix)

if __name__ == '__main__':
    main()