import argparse

from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from modules.config import configuration
from modules.common import tools

###

t = tools()

###
### MOVE THIS TO TOOLS / BEGIN

argument_parser = argparse.ArgumentParser(description = "shadowWire: message encode script", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
argument_parser.add_argument("-a", "--alias", help = "define alias", default = "default", metavar = "ALIAS")
argument_parser.add_argument("-c", "--config", help = "define configuration file", default = "config/main.json", metavar = "CONFIG_FILE")
argument_parser.add_argument("-r", "--recipient", help = "recipient's public key", metavar = "PUBLIC_KEY")
argument_parser.add_argument("-s", "--save", help = "save file", metavar = "MESSAGE_FILE")
arguments = argument_parser.parse_args()

###

if t.isFile(arguments.config):
  try:
    config = configuration(arguments.config, arguments.alias)
  except Exception as e:
    print("error reading configuration file: " + arguments.config)
    print(e)
    exit()
else:
  print("configuration file not found: " + arguments.config)
  exit()

### MOVE THIS TO TOOLS / END
###

if arguments.recipient:
  if t.isFile(arguments.recipient):
    try:
      with open(arguments.recipient, "rb") as key_file:
        recipients_key = serialization.load_pem_public_key(key_file.read())
      print(recipients_key)
    except:
      print("error reading recipients public key")
      exit()

    message = bytes(input("enter message: "), "utf-8")
    enc_message = recipients_key.encrypt(message, padding.OAEP(mgf = padding.MGF1(algorithm=hashes.SHA256()), algorithm = hashes.SHA256(), label = None))
    print(enc_message)

    f = open(arguments.save, "xb")
    f.write(enc_message)
    f.close()

    #message = enc_message = ""

else:
  print("recipients public key not found")
