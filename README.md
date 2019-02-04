# Py-Onym
tellonym.me message spammer

## Summary ##
tellonym.me is an online service that allows you to receive anonymous messages from people who have your tag. For some reason it's also unprotected by a captcha so you can (ab)use that to rickroll your friends, assuming you have any, anonymously.

## Dependencies ##
* python3
* selenium

## Command line options ##
./tellonym.py -h
usage: tellonym.py [-h] [-i INPUT_FILE] [-t TIMES] [-r RETRIES] user

Py-onym: Tellonym message spammer.

positional arguments:
  user                  Name of the target user.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        Input file containing messages to be sent.
  -t TIMES, --times TIMES
                        Number of times to loop through the messages
  -r RETRIES, --retries RETRIES
                        Number of times to retry sending message until giving
                        up.
