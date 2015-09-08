NAME=hdfs-block-dist
DIST_PATH=`dirname $0`

# COmpress binaries
zip -r $DIST_PATH/$NAME.zip ../src/*

# Generate executable
echo '#!/usr/bin/env python' | cat - $DIST_PATH/$NAME.zip > $DIST_PATH/$NAME
chmod +x $DIST_PATH/$NAME

# Remove temporal files
rm $DIST_PATH/$NAME.zip