#!/bin/sh
for i in `seq 1 33`
do
  python sensormodel/cascadesink.py $1
done
