#!/bin/sh
echo Lab 1. Var 23.
date

count=0

handl(){
count=$((count+1))
if [ $count -eq 2 ]
then
awk 'BEGIN{total=0} {total += $2} END{print "\nTotal size: " total}' some_file
fi
}

trap "handl" 2
text=`find ../Homework_2/ -maxdepth 1 -size +24b -atime -5 -ls`
echo $text > some_file
sleep 2
sleep 2
sleep 2
awk 'BEGIN{print "Selected files:"} {print $11}' some_file
