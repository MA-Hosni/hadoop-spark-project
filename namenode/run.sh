#!/bin/bash

# Format namenode if not already formatted
if [ ! -d "/hadoop/dfs/name/current" ]; then
    $HADOOP_HOME/bin/hdfs namenode -format -force
fi

# Start NameNode
$HADOOP_HOME/bin/hdfs namenode
