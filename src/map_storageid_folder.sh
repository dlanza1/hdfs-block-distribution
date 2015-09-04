paths=`hdfs getconf -confKey dfs.datanode.data.dir | tr ',' '\n'`

for path in $paths
do
	path=`echo $path | sed 's/FILE://g'`
	storageid=`cat $path/current/VERSION | grep -Po '(?<=storageID=).*'` 
	
	echo $storageid,$path
done