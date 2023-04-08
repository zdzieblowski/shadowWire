import argparse

from modules.config import configuration
from modules.common import tools

###

t = tools()

###

argument_parser = argparse.ArgumentParser(description = "shadowWire: initialization script", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
argument_parser.add_argument("-a", "--alias", help = "define alias", default = "default", metavar = "ALIAS")
argument_parser.add_argument("-c", "--config", help = "define configuration file", default = "config/main.json", metavar = "CONFIG_FILE")
argument_parser.add_argument("-p", "--purge", help = "purge all storages", action = "store_true")
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

if arguments.purge:
  print("purging")
  # ADD PURGE HERE
else:
  t.generateDirs(config)

  if t.isFile(config.private_key):
    if t.isFile(config.public_key):
      print("keypair found")
      try:
        f = open(config.private_key, "rt")
        import_key = t.importKey(f)
        print(import_key)
      except:
        print("invalid private key")
        t.noGate("generate new keypair ?", t.generateKeys, config)
    else:
      print("public key missing")
      # ADD PUBLIC KEY REGENERATION HERE
  else:
    print("private key missing")
    t.generateKeys(config)
