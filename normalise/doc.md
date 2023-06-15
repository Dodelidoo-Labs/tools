# Usage

This script can be run in terminal to normalise any number found in a string.

This is useful for example when you are converting MidJourney prompts in batch to SD compatible prompts.

MJ Supports weights from 0 to 10000
SD only supports weights between 0 and approx 1.6
This script will simply normalise the MJ weights into values between 0 and 1

It might not be ideal, but useful still.

# ToDo

Make the code iterate through folders recursively or a CSV file.
Right now, it takes only ONE string a time that must be edited in the code.

See `cleanmjprompts.py` for an automated version of this script