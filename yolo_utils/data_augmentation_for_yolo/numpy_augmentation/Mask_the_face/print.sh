#!/bin/sh  
while true  
do  
  echo 'Images:'
  ls -l data_masked/images | egrep -c '^-'

  echo 'Labels:'
  ls -l data_masked/labels | egrep -c '^-' 
  sleep 60  
done






