import argparse
import json
import os

from Crypto.PublicKey import ECC

### CONFIG

user_home = os.path.expanduser("~") + "/"

keychain_dir = "keychain/"
prvkey_file = "sw_private.pem"
pubkey_file = "sw_public.pem"
contacts_file = "sw_contacts.json"

### INIT

argp = argparse.ArgumentParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)
argp.add_argument("-ds", "--data-storage", help = "define path to data storage", default = ".sw/")
args = argp.parse_args()

data_storage = args.data_storage + "/" if not args.data_storage.endswith("/") else args.data_storage
data_storage = user_home + data_storage
keychain_storage = data_storage + keychain_dir

prvkey_pem = keychain_storage + prvkey_file
pubkey_pem = keychain_storage + pubkey_file

### METHODS

def del_keys():
  os.remove(prvkey_pem)
  os.remove(pubkey_pem)

def gen_keys():
  key = ECC.generate(curve="Ed448")

  f = open(prvkey_pem,"xt")
  f.write(key.export_key(format="PEM"))
  f.close()

  f = open(pubkey_pem,"xt")
  f.write(key.public_key().export_key(format="PEM"))
  f.close()

  print("keys generated")

  print(key)

### RUNTIME

if not os.path.isdir(data_storage):
  os.mkdir(data_storage)
  os.mkdir(keychain_storage)

if os.path.isfile(prvkey_pem) and os.path.isfile(pubkey_pem):
  print("keys found")

  try:
    f = open(prvkey_pem,'rt')
    import_key = ECC.import_key(f.read())
    print(import_key)
  except:
    print("invalid keys")
    gen = input("generate new keys ? [y/N] ").upper()
    if gen in ("Y","N",""):
      if gen == "Y":
        del_keys()
        gen_keys()
      else:
        print("exiting")
    else:
      print("invalid input")
else:
  print("keys missing")
  gen_keys()
