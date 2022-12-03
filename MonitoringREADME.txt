Steps for running scripts

1.download all of the files and ensure they don't have file extensions on them. Also make sure they are in /home to make it easier to run everything.
2.Run the following commands in termianl to make sure that the files will run properly and there are no hidden characters anywhere
	sudo mkdir /REPLACEME
	sudo chmod 777 /REPLACEME
	chmod 777 mitigation
	chmod 777 monitoring
	chmod 777 backup
	sed -i -e 's/\r$//' mitigation
	sed -i -e 's/\r$//' monitoring
	sed -i -e 's/\r$//' backup
	
  	if rsa is not installed run this command: pip install rsa
  	
3.Run "./backup" to create a backup of the system
4.Run "unzip TheImage.jpg" to expand the image

*NOTE* make sure you have the following command pretyped in terminals to ensure that you can run them fast enough.
Run them in this order.

5.Run "./monitoring" to start monitoring
6.Run "python3 detection" to start detection
7.Run "./content/image" to start ransomeware
8.AS SOON AS DETECTION says "Alert!" in terminal run "./mitigation" to kill ransomeware and restore system
9.Kill all processes still running by pressing ctrl+c in each terminal

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a bash script that is ran before the attack take place
This script will keeping looping and logging cpu usage and files that have been modified.

The cpu_usage function print a time stamp on one line
The next line prints the current cpu usage amount.

The file_tracker function prints a time stamp followed by the text "File was modified"

There will be 2 files named CPU_usage and file_tracker in the /REPLACEME directory.
You will see CPU usage in 1 file and you will see time stamps with File was modified.

This information is used by detection to determine if an attack is happening or not.

~~~~~~~~~~~~~~~~~~~~~~monitoring script below~~~~~~~~~~~~~~~~~~~~~~

#! /bin/bash

#tracking usage
cpu_usage(){
	date "+%T" >> /REPLACEME/CPU_usage
	echo "CPU Usage: "$[100-$(vmstat 1 2|tail -1|awk '{print $15}')]"%" >> /REPLACEME/CPU_usage
	}
	
#tracking file changes	
file_tracker(){
	inotifywait --exclude meta.* --timefmt='%T File was modified' --format '%T' -m -r -q -e modify /home/sec-lab/ >> /REPLACEME/file_tracker
	#inotifywait --exclude meta.* -m -r -q -e modify /home/sec-lab/ >> /REPLACEME/file_tracker
	}

while :
do
	file_tracker & cpu_usage && kill $!
	
done
