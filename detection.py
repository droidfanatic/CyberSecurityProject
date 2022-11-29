import os
import time

pids = []
reportedpids = []
whitelist = ["/usr/libexec/tracker-store\n", "/usr/libexec/tracker-extract\n", "currentpids.txt\n", "-elf\n", "sec-lab\n"]

print("Starting Detection")
time.sleep(2)
print("Grabbing Processes")

os.system("ps -elf | grep sec-lab > syspids.txt")

f = open("syspids.txt", "r")
lines = f.readlines()
f.close()

for line in lines:
	sline = line.split(" ")
	for i,split in enumerate(sline):
		if i > 3 and split.isdigit():
			pids.append(split)
			break

print("Processes Collected, Starting Analysis")

alertfile = open("alertfile.txt", "w")
alertfile.write("Start\n")
alertfile.close()

susfile = open("suspicious_processes.txt", "w")
susfile.write("Start\n")
susfile.close()

while(True):
	alertfile = open("alertfile.txt", "a")
	susfile = open("suspicious_processes.txt", "a")

	#this delay allows time to kill process
	time.sleep(0.002)

	currentpids = []
	tempfile = []

	#read monitoring file
	mfile = open("syspids.txt", "r")
	mlines = mfile.readlines()
	mfile.close()

	os.system("ps -elf | grep sec-lab > currentpids.txt")
	
	f = open("currentpids.txt", "r")
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

	for i,pid in enumerate(currentpids):
		if pid not in pids and pid not in reportedpids:
			reportedpids.append(pid)
			susfile.write(tempfile[i])
			alertfile.write("Alert! " + str(pid) + " is attacking the system!\n")
			print("Alert! " + str(pid) + " is attacking the system!")

	#for line in lines:
		#look for weirdness
		#if line == "weirdness":
			#print("Alert")
			#print("Alert! " + str(pid) + " is attacking the system!")
			#alertfile.write("Alert! " + str(pid) + " is attacking the system!\n")
	alertfile.close()
	susfile.close()	
