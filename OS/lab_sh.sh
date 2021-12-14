#!/bin/bash
let count=0
let date=`date | awk '{print $3}'`

handl(){
let count++
if [ $count -eq 2 ]
then
ls -sl ../Homework_2/ | tail -n +2 | awk 'BEGIN{total=0}
{
if ($1 > 12 && ($7 - $date) < 5){
total += $1
}
}
END{print "\nTotal size: " total}'
exit 0
fi
}

trap "handl" SIGINT
sleep 2
sleep 2
sleep 2
ls -sl ../Homework_2/ | tail -n +2 | awk 'BEGIN{print "Selected files:"}
{
if ($1 > 12 && ($8 - $date) < 5){
print $1, $7, $8, $10
}
}
'
