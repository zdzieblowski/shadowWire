import argparse
import requests
import base64

from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from modules.config import configuration
from modules.common import tools

###

url = "http://localhost:60606/write"
t = tools()

###

argument_parser = argparse.ArgumentParser(description = "shadowWire: message encode script", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
argument_parser.add_argument("-a", "--alias", help = "define alias", default = "default", metavar = "ALIAS")
argument_parser.add_argument("-c", "--config", help = "define configuration file", default = "config/main.json", metavar = "CONFIG_FILE")
argument_parser.add_argument("-r", "--recipient", help = "recipient's public key", metavar = "PUBLIC_KEY")
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
    enc_message = recipients_key.encrypt(message, padding.OAEP(mgf = padding.MGF1(algorithm = hashes.SHA256()), algorithm = hashes.SHA256(), label = None))
    print(enc_message)
    print(str(enc_message))

    try:
      query = {"message": base64.b64encode(enc_message).decode("utf-8")}
      req = requests.post(url, json = query)

      if req.status_code == 200:
        print("{0} {1} ".format(req.elapsed, req.text))
      else:
        print(req.status_code)

    except Exception as e:
      print(e)

else:
  print("recipients public key not found")
