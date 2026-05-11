#!/bin/bash

if [ "$SPARK_WORKLOAD" == "master" ]; then
    # Start Spark Master
    $SPARK_HOME/sbin/start-master.sh
    # Keep container running
    tail -f /opt/spark/logs/spark-master.out
elif [ "$SPARK_WORKLOAD" == "worker" ]; then
    # Start Spark Worker
    $SPARK_HOME/sbin/start-worker.sh $SPARK_MASTER
    tail -f /opt/spark/logs/spark-worker.out
else
    echo "Undefined Workload Type $SPARK_WORKLOAD, must specify: master, worker"
fi
