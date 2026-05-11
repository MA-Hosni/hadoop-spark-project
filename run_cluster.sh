#!/bin/bash

echo "Building base Hadoop image..."
docker build -t hadoop-base:3.3.5-dorian ./base

echo "Building base Spark image..."
docker build -t spark-base:3.4.3-dorian ./spark

echo "Starting all services..."
docker compose up -d --build

echo "Waiting for services to start..."
sleep 30

echo "Checking cluster status..."
docker ps

echo "NameNode dashboard: http://localhost:9870"
echo "ResourceManager dashboard: http://localhost:8088"
echo "Spark Master dashboard: http://localhost:9090"
echo ""
echo "To check HDFS status: docker exec -it namenode bash -c 'hdfs dfsadmin -report'"
