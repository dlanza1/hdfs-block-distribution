# HDFS block distribution

This tool shows how blocks of a particular folder or file are distributed along the nodes and disks of a cluster. 

Numbers showing the number of blocks are colored. Colors enable users to easily identify if blocks are not equally distributed.

### How it works

Based on the information provided by the HDFS filesystem checking utility, which lists the blocks of a particulas folder or file, this tool counts the blocks per disk and per machine.

An average is calculated per machine. Colors of numbers are determined by comparing number of blocks of each disk with the average in terms of percentage.

### Running it

Distribution folder (dist) contains the only necessary file to run this tool. This file (hdfs-blok-dist) must be placed on a machine where Hadoop is installed.

The file can be store in one of the $PATH directories, so it can be executed anywhere without writing the path to it.

The following command should be run: 

```
hdfs-blok-dist -p <path> [-n <hostname>] [-w <0-100>] [-e <0-100>] [--help]
```

Arguments:
 * -p <path>: (mandatory) path to the directory or file to analyze.
 * -w <0-100>: set percentage to use when coloring in yellow (default: 20).
 * -e <0-100>: set percentage to use when coloring in red (default: 50).
 * -n <hostname>: get detailed information for a given host (root access through SSH is needed).
 * -h: show help and exit.
