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

This is a bash script that is meant to be ran once an attack has taken place.
It reads the alert file to check for any alerts that might be thrown.
If there is an alter it parses the alert for the process ID and kills that process.
It then deletes the encrypted directories and restores the directory from the previous back up.

After this script it ran, it is expected that the directory be back to normal and no encryptions to have taken place.

~~~~~~~~~~~~~~~~~~~~~~mitigation script below~~~~~~~~~~~~~~~~~~~~~~

#/!bin/bash

#kill the suspicious pid
process_id=($(awk '{print $2}' /REPLACEME/alertfile))

for i in "${process_id[@]}"
do
	kill -9 $i
done

#delete the encrypted directories
rm -rf /home/sec-lab/*/

#restore from /home/sec-lab from /home_backup
rsync -av --include=*.* --include=*/ /REPLACEME/home_backup/ /home/sec-lab/ 
