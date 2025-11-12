#!/bin/bash

SPARK_WORKLOAD=$1 # $1 corresponde o primeiro parâmetro que é passado ao executar o arquivo

echo "SPARK_WORKLOAD: $SPARK_WORKLOAD"

if [ "$SPARK_WORKLOAD" == "master" ];
then
  start-master.sh -p 7077
elif [ "$SPARK_WORKLOAD" == "worker" ];
then
  start-worker.sh spark://spark-master-dsa:7077
elif [ "$SPARK_WORKLOAD" == "history" ]
then
  start-history-server.sh
fi # comando que encerra o bloco condicional