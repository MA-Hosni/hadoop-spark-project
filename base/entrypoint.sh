#!/bin/bash

# Format the NameNode if needed (only on first run)
if [ ! -d "/hadoop/dfs/name/current" ]; then
    $HADOOP_HOME/bin/hdfs namenode -format -force
fi

# Start SSH service (needed for Hadoop communication)
service ssh start

# Execute whatever command was passed to the container
exec "$@"
