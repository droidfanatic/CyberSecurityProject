This script is not needed to run the full test.

To run this scrip place in directory that you want to generate files in

Run "python3 genfiles"

observe that 200 files were created

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This was written to generate 200 files at a time in the need that the ransomware was too fast to detect and kill.
This script was not used at all in the demo for this project. It was just written just in case it was needed.

~~~~~~~~~~~~~~~~~~~~~~genfiles script below~~~~~~~~~~~~~~~~~~~~~~

for i in range(200):
	fname = "file" + str(i) + ".txt"
	f = open (fname, "w")
	for j in range(100):
		f.write("abcdefghijklmnopqrstuvwxyz\n")
	f.close()
