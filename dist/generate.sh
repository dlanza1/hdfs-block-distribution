NAME=hdfs-block-dist
DIST_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Compress binaries
cd $DIST_PATH/../src/
zip -r $DIST_PATH/$NAME.zip *

# Generate executable
echo '#!/usr/bin/env python' | cat - $DIST_PATH/$NAME.zip > $DIST_PATH/$NAME
chmod +x $DIST_PATH/$NAME

# Remove temporal files
rm $DIST_PATH/$NAME.zip