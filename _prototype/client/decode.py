import requests
import argparse
import json
import base64
import sys

from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from modules.config import configuration
from modules.common import tools

###

url = "http://localhost:60606/read"
t = tools()
debug = False

###

argument_parser = argparse.ArgumentParser(description = "shadowWire: message decode script", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
argument_parser.add_argument("-a", "--alias", help = "define alias", default = "default", metavar = "ALIAS")
argument_parser.add_argument("-c", "--config", help = "define configuration file", default = "config/main.json", metavar = "CONFIG_FILE")
argument_parser.add_argument("-l", "--load", help = "load file", metavar = "load file")
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

if t.isFile(config.private_key):
  try:
    with open(config.private_key, "rb") as key_file:
      receivers_key = serialization.load_pem_private_key(key_file.read(), password = None)
  except Exception as e:
    print(e)
    print("error reading receiver private key")
    exit()

  try:
    query = {"height": 0}
    req = requests.post(url, json = query)

    if req.status_code == 200:
      messages = json.loads(req.text)

      last = 0

      for message in messages:
        dec_message = []
        try:
          for d in range(0,len(message["data"])):
            dec_message.append(receivers_key.decrypt(bytes(base64.b64decode(str(message["data"][d]))), padding.OAEP(mgf = padding.MGF1(algorithm = hashes.SHA256()), algorithm = hashes.SHA256(), label = None)).decode("utf-8"))

          decrypted = json.loads("".join(dec_message))

          print("================================================================================")
          print("DATE: %s" % decrypted["date"])
          print("--------------------------------------------------------------------------------")
          print(decrypted["data"])
          print("--------------------------------------------------------------------------------")
          print("SENDER PUBLIC KEY:\n%s" % decrypted["sender"])
          print("================================================================================\n")
        except Exception as e:
          if debug:
            print(e)
            print("[x]")

    else:
      print(req.status_code)

  except Exception as e:
    print(e)

else:
  print("recipients public key not found")
