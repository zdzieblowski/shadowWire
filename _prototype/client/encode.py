from datetime import datetime
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

def chunks(string, size):
  for start in range(0, len(string), size):
    yield string[start:start+size]

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

    message = input("enter message: ")
    #message = bytes("%s" % input("enter message: "), "utf-8")
    #print(message)

    enc_message = []
    iter = 0

    for chunk in chunks(message,446):
      print(chunk)
      enc_message.append(base64.b64encode(recipients_key.encrypt(bytes(chunk, "utf-8"), padding.OAEP(mgf = padding.MGF1(algorithm = hashes.SHA256()), algorithm = hashes.SHA256(), label = None))).decode("utf-8"))
      iter = iter + 1

    #enc_message = recipients_key.encrypt(message, padding.OAEP(mgf = padding.MGF1(algorithm = hashes.SHA256()), algorithm = hashes.SHA256(), label = None))

    try:
      query = {"message": enc_message, "date": str(datetime.now())}
      #query = {"message": base64.b64encode(enc_message).decode("utf-8"), "date": str(datetime.now())}
      req = requests.post(url, json = query)

      if req.status_code == 200:
        print("{0} {1}".format(req.elapsed, req.text))
      else:
        print(req.status_code)

    except Exception as e:
      print(e)

else:
  print("recipients public key not found")
