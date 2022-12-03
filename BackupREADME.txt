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

backup is a simple bash script that copies all files with extensions to a back up directory that won't be touched by the ransomware.
After the directoring is created and back in run you should see a copy of /home/sec-lab/ in /REPLACEME/home_backup

~~~~~~~~~~~~~~~~~~~~~~backup script below~~~~~~~~~~~~~~~~~~~~~~

#/!bin/bash

#copy all file with extensions to a backup directory
rsync -av -f "- .*" --include=*.* --include=*/ --exclude=* /home/sec-lab/ /REPLACEME/home_backup
