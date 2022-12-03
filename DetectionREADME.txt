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

detection.py

This python script calls a couple of shell command to help speed up the process as well as
some python logic to help determine when an attack is actually happening.

ps -elf | grep sec-lab > /REPLACEME/syspids

This command takes the current processes that are running and saved the list to a file.
All of the process IDs in this file are considered to be part of the whitelist that detection ignores.
This helps prevent random system processes from triggering an alert.

This same command is used every loop to get a list of the current running processes to ensure it stays up to date.
The difference is that when this command is called it is saving to /REPLACEME/currentpids instead of /REPLACEME/syspids

I have to create a string for the next command.

"grep -E " + str(logtime) + " /REPLACEME/file_tracker > /REPLACEME/test"

logtime is a timestamp that is being tracked in the cpu usage file that is being generated from monitoring.
Basically this command is filtering through the file tracker file that is being generated from monitoring and
created a new file of all entries containing the selected timestamp.

The rest of the script is pure python.


Grab system processes

Clear file_tracker, CPU_usage, alertfile, and suspicious_processes

Grab current processes

if the process isn't whitelisted from the intial grab, scan the process for whitelisted keywords and whitelist process if there is a match

Try to read timestamp, if cant read then give a value of ~~~~~
Try to read cpu usage percentage, if cant read then give a value of ~~~~~
If either have a value of ~~~~~ wait until value can be read in
This prevent detection from crashing or reading garbage values

if the cpu usage is over 90% then do the following
Grab list of all files modified at timestamp
Count the number of files changed
if more than 20 files were changed at timestamp then continue checking for attack
(We have to check the number of files being changed because monitoring is only providing a timestamp and "File has been modified" for each file modified

if the last 2 if statements pass then analyze current processes.
if it is not a whitelisted process or a previously reported process then an attack is happening
The process id will be reported
This prevent the alert file from having too many processes in it
Then we write the suspected process to a file for mitigation to read
We also trigger an alert to a file for mitigation and an alert to the terminal for the user

The script continues to loop until you kill the detection script.

~~~~~~~~~~~~~~~~~~~~~~detection script below~~~~~~~~~~~~~~~~~~~~~~

import os
import time

pids = []
reportedpids = []
whitelist = ["/usr/libexec/tracker-store\n", "/usr/libexec/tracker-extract\n", "/REPLACEME/currentpids\n", "-elf\n", "sec-lab\n", "./monitoring\n", "/home/sec-lab/\n", "-1\n", "2\n", "$15}\n"]

print("Starting Detection")
time.sleep(2)
print("Grabbing Processes")

os.system("ps -elf | grep sec-lab > /REPLACEME/syspids")

f = open("/REPLACEME/syspids", "r")
lines = f.readlines()
f.close()

for line in lines:
	sline = line.split(" ")
	for i,split in enumerate(sline):
		if i > 3 and split.isdigit():
			pids.append(split)
			break

print("Processes Collected, Starting Analysis")

clearfile = open("/REPLACEME/file_tracker", "w")
clearfile.write("")
clearfile.close()

clearfile = open("/REPLACEME/CPU_usage", "w")
clearfile.write("")
clearfile.close()

alertfile = open("/REPLACEME/alertfile", "w")
alertfile.write("Start\n")
alertfile.close()

susfile = open("/REPLACEME/suspicious_processes", "w")
susfile.write("Start\n")
susfile.close()

#read cpu file
cpufile = open("/REPLACEME/CPU_usage", "r")

while(True):
	alertfile = open("/REPLACEME/alertfile", "a")
	susfile = open("/REPLACEME/suspicious_processes", "a")

	#this delay allows time to kill process
	time.sleep(0.002)

	currentpids = []
	tempfile = []

	os.system("ps -elf | grep sec-lab > /REPLACEME/currentpids")
	
	f = open("/REPLACEME/currentpids", "r")
	lines = f.readlines()
	f.close()

	for line in lines:
		sline = line.split(" ")
		for i,split in enumerate(sline):
			if i > 3 and split.isdigit():
				tempfile.append(line)
				currentpids.append(split)
				if split not in pids and sline[len(sline) - 1] in whitelist:
					pids.append(split)
				break
	try:
		logtime = cpufile.readline().replace("\n","")
	except:
		#pass
		logtime = "~~~~~"
	try:
		usage = cpufile.readline().split(" ")[2].replace("%","")
	except:
		#pass
		usage = "~~~~~"
	
	while(logtime == "~~~~~"):
		try:
			logtime = cpufile.readline().replace("\n","")
		except:
			logtime = "~~~~~"
			
	while(usage == "~~~~~"):
		try:
			usage = cpufile.readline().split(" ")[2].replace("%","")
		except:
			usage = "~~~~~"
	
	if int(usage) >= 90:
		command = "grep -E " + str(logtime) + " /REPLACEME/file_tracker > /REPLACEME/test"
		os.system(command)
		trackerfile = open("/REPLACEME/test", "r")
		tlines = trackerfile.readlines()
		trackerfile.close()
		if len(tlines) >= 20:
			for i,pid in enumerate(currentpids):
				if pid not in pids and pid not in reportedpids:
					reportedpids.append(pid)
					susfile.write(tempfile[i])
					alertfile.write("Alert! " + str(pid) + " is attacking the system!\n")
					print("Alert! " + str(pid) + " is attacking the system! " + str(tempfile[i].split(" ")[len(tempfile[i].split(" ")) - 1].replace("\n","")))

	alertfile.close()
	susfile.close()