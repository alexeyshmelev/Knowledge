#!/bin/bash
echo Lab 1. Var 23.
date

let count=0

handl(){
let count++
if [ $count -eq 2 ]
then
find ../Homework_2/ -maxdepth 1 -size +24b -atime -5 -ls > some_file
awk 'BEGIN{total=0} {total += $2} END{print "\nTotal size: " total}' < some_file
exit 0
fi
}

trap "handl" SIGINT
sleep 2
sleep 2
sleep 2
find ../Homework_2/ -maxdepth 1 -size +24b -atime -5 -ls > sime_file
awk 'BEGIN{print "Selected files:"} {print $11}' < some_file
