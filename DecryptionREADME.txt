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

Decryption is just a helper python scrip that allowed us to show that our ransomware was actually working.
It also allowed us to test out other scripts without have to reset the system and download all the files again.

This script will just reverse the the damage that was caused by the ransomware.
It reads the keys that were saved locally and decrypts all the files that were previously encrytped.

~~~~~~~~~~~~~~~~~~~~~~backup script below~~~~~~~~~~~~~~~~~~~~~~

import glob
import os
import cryptography
import rsa
from cryptography.fernet import Fernet
import smtplib


FERNET_KEY_LOCATION = os.path.expanduser('~') + '/'  # OPTIONAL - CHANGE TO KEY DIRECTORY
RSA_KEY_LOCATION = os.path.expanduser('~') + '/'  # OPTIONAL - CHANGE TO KEY DIRECTORY
ENCRYPTION_PATH = os.path.expanduser('~') + '/'  # OPTIONAL - CHANGE TO KEY DIRECTORY


# get_files uses glob to retrieve and create an array for the file locations
def get_files():
    f_array = [f for f in glob.glob(ENCRYPTION_PATH + "**/*.*", recursive=True)]
    return f_array

# load rsa keys
# read each key and return both keys for encrypt rsa function
def rsa_load_keys():
    with open(RSA_KEY_LOCATION + 'publicKey', 'rb') as k:
        publicKey = rsa.PublicKey.load_pkcs1(k.read())
    with open(RSA_KEY_LOCATION + 'privateKey', 'rb') as k:
        privateKey = rsa.PrivateKey.load_pkcs1(k.read())
    return publicKey, privateKey

def decrypt_rsa():
    pubKey, privKey = rsa_load_keys()
    with open(FERNET_KEY_LOCATION + 'fernetKey', 'rb') as o:
        encrypted_key = o.read()
    decrypted_key = rsa.decrypt(encrypted_key, privKey)
    with open(FERNET_KEY_LOCATION + 'fernetKey', 'wb') as o:
        o.write(decrypted_key)

# decrypt the files, provide file array, fernet key
def decrypt_fernet(file_array, fernet_key):
    # read the fernet key
    with open(fernet_key, 'rb') as encrypt_key:
        f_key = encrypt_key.read()
    fernet = Fernet(f_key)
    # loop through encrypted files
    for f in file_array:
        with open(f, 'rb') as encrypted_file:
            encrypted_text = encrypted_file.read()
        # decrypt the text
        decrypted_text = fernet.decrypt(encrypted_text)
        # write the decrypted text back to file
        with open(f, 'wb') as decrypted_file:
            decrypted_file.write(decrypted_text)


# Step 1:
filesarray = get_files()

# Step 2:
decrypt_rsa()
decrypt_fernet(filesarray, FERNET_KEY_LOCATION+'fernetKey')
