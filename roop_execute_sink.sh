#!/bin/sh
for i in `seq 1 100`
do
  python cascade_smallworld_sink.py $1
done
