import argparse
import os

from modules.tools import tools
from modules.config import configuration

from Crypto.PublicKey import ECC

###

t = tools()

###

argument_parser = argparse.ArgumentParser(description = "shadowWire: initialization script", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
argument_parser.add_argument("-a", "--alias", help = "define alias", default = "default", metavar = "ALIAS")
argument_parser.add_argument("-c", "--config", help = "define configuration file", default = "config/main.json", metavar = "CONFIG_FILE")
argument_parser.add_argument("-p", "--purge", help = "purge all storages", action = "store_true")
arguments = argument_parser.parse_args()

###

if os.path.isfile(arguments.config):
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

def gen_keys():
  if os.path.isfile(config.private_key):
    os.remove(config.private_key)
  if os.path.isfile(config.public_key):
    os.remove(config.public_key)

  key = ECC.generate(curve = config.ecc_curve)

  f = open(config.private_key, "xt")
  f.write(key.export_key(format = "PEM"))
  f.close()

  f = open(config.public_key, "xt")
  f.write(key.public_key().export_key(format = "PEM"))
  f.close()

  print("keys generated")
  print(key)

###

if arguments.purge:
  print("purging")
else:

  if not os.path.isdir(config.storage):
    os.mkdir(config.storage)
    os.mkdir(config.alias_storage)
    os.mkdir(config.app_storage)
    os.mkdir(config.key_storage)
  else:
    if not os.path.isdir(config.alias_storage):
      os.mkdir(config.alias_storage)
      os.mkdir(config.app_storage)
      os.mkdir(config.key_storage)
    else:
      if not os.path.isdir(config.app_storage):
        os.mkdir(config.app_storage)
      if not os.path.isdir(config.key_storage):
        os.mkdir(config.key_storage)

  if os.path.isfile(config.private_key) and os.path.isfile(config.public_key):
    print("keys found")
    try:
      f = open(config.private_key, "rt")
      import_key = ECC.import_key(f.read())
      print(import_key)
    except:
      print("invalid keys")
      t.ynq("generate new keys ?", gen_keys)
  else:
    print("keys missing")
    gen_keys()
