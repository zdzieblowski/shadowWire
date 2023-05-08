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

print(config.private_key)

if t.isFile(config.private_key):
  try:
    with open(config.private_key, "rb") as key_file:
      receivers_key = serialization.load_pem_private_key(key_file.read(), password = None)
      print(receivers_key)
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
        #print(message)
        try:
          for d in message["data"]:
            #print(d)
            dec_message.append(receivers_key.decrypt(bytes(base64.b64decode(str(d))), padding.OAEP(mgf = padding.MGF1(algorithm = hashes.SHA256()), algorithm = hashes.SHA256(), label = None)).decode("utf-8"))
          if last != 0:
            sys.stdout.write("\n")
            last = 0
          print("%s:\n%s\n" % (message["date"], "".join(dec_message)))
        except:
          sys.stdout.write(".")
          last = 1

    else:
      print(req.status_code)

  except Exception as e:
    print(e)

else:
  print("recipients public key not found")
