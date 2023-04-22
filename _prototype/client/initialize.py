import argparse

from modules.config import configuration
from modules.common import tools

###

t = tools()

### MOVE THIS TO TOOLS / BEGIN

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

### MOVE THIS TO TOOLS / END

if arguments.purge:
  t.purgeAll(config)
else:
  t.generateDirs(config)

  if t.isFile(config.private_key):
    try:
      private = t.importKeys(config.private_key)
    except:
      print("invalid private key")
      t.askGate("generate new keypair ?", "N", t.generateKeys, config)

    if t.isFile(config.public_key):
      print("keypair found")

      print("PRIVATE:\n{0}\n".format(private))
      print("PUBLIC:\n{0}\n".format(private.public_key()))
    else:
      print("public key missing")
      print("generating new public key from existing private key")

      t.generatePublicKey(config, private)
  else:
    print("private key missing")
    t.generateKeys(config)
