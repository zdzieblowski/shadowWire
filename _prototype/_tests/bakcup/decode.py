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

argument_parser = argparse.ArgumentParser(description = "shadowWire: message decode script", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
argument_parser.add_argument("-a", "--alias", help = "define alias", default = "default", metavar = "ALIAS")
argument_parser.add_argument("-c", "--config", help = "define configuration file", default = "config/main.json", metavar = "CONFIG_FILE")
argument_parser.add_argument("-l", "--load", help = "load file", metavar = "load file")
argument_parser.add_argument("-r", "--receiver", help = "receiver's private key", metavar = "PRIVATE_KEY")

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

if arguments.receiver:
  if t.isFile(arguments.receiver):
    try:
      with open(arguments.receiver, "rb") as key_file:
        receivers_key = serialization.load_pem_private_key(key_file.read(), password = None)
      print(receivers_key)
    except Exception as e:
      print(e)
      print("error reading receiver private key")
      exit()

    #message = bytes(input("enter bytes: "), "utf-8")

    f = open(arguments.load, "rb")
    message = f.read()
    f.close()

    dec_message = receivers_key.decrypt(message, padding.OAEP(mgf = padding.MGF1(algorithm = hashes.SHA256()), algorithm = hashes.SHA256(), label = None))
    print(dec_message)

    message = ""

else:
  print("recipients public key not found")
