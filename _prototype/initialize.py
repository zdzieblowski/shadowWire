import argparse
import os

from modules.config import configuration
from modules.generators import generators
from modules.tools import tools

from Crypto.PublicKey import ECC

###

g = generators()
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

if arguments.purge:
  print("purging")
else:
  g.dirs(config)

  if os.path.isfile(config.private_key) and os.path.isfile(config.public_key):
    print("keys found")
    try:
      f = open(config.private_key, "rt")
      import_key = ECC.import_key(f.read())
      print(import_key)
    except:
      print("invalid keys")
      t.ynq("generate new keys ?", g.keys, config)
  else:
    print("keys missing")
    g.keys(config)
