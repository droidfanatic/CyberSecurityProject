import os

pids = []

for pid in os.listdir('/proc'):
	if pid.isdigit():
		pids.append(pid)

f = open("syspids.txt", "w")

for pid in pids:
	f.write(str(pid) + "\n")

f.close()

alertfile = open("alertfile.txt", "w")

while(True):
	#read monitoring file
	f = open("syspids.txt", "r")
	lines = f.readlines()
	f.close()

	for pid in os.listdir('/proc'):
		if pid.isdigit() and pid not in pids:
			alertfile.write("Alert!")
			print("Alert!")

	for line in lines:
		#look for weirdness
		if line == "weirdness":
			print("Alert! Attack in progress!")
			alertfile.write("Alert! Attack in progress!")
