FROM ubuntu:22.04

# Prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install Java, Python, SSH, and other tools
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    python3 \
    python3-pip \
    wget \
    curl \
    ssh \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Set Java environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin

# Download and install Hadoop 3.3.5
RUN wget https://archive.apache.org/dist/hadoop/common/hadoop-3.3.5/hadoop-3.3.5.tar.gz \
    && tar -xzf hadoop-3.3.5.tar.gz \
    && mv hadoop-3.3.5 /opt/hadoop \
    && rm hadoop-3.3.5.tar.gz

# Set Hadoop environment variables
ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Download and install Spark 3.4.3
RUN wget https://archive.apache.org/dist/spark/spark-3.4.3/spark-3.4.3-bin-hadoop3.tgz \
    && tar -xzf spark-3.4.3-bin-hadoop3.tgz \
    && mv spark-3.4.3-bin-hadoop3 /opt/spark \
    && rm spark-3.4.3-bin-hadoop3.tgz

# Set Spark environment variables
ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
ENV PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9.7-src.zip:$PYTHONPATH

# Create necessary Hadoop directories
RUN mkdir -p /hadoop/dfs/name /hadoop/dfs/data /tmp/hadoop-root

# Copy configuration files
COPY conf/* $HADOOP_CONF_DIR/

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
