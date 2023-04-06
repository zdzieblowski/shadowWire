import os

from Crypto.PublicKey import ECC

class generators:

  def dirs(self, config):
    def generate_directories():
      for index, (key, value) in enumerate(config.data["directories"].items()):
        temp_path = os.path.join(config.alias_storage, value["path"])
        if not os.path.isdir(temp_path):
          os.mkdir(temp_path)

    if not os.path.isdir(config.storage):
      os.mkdir(config.storage)
      os.mkdir(config.alias_storage)
      generate_directories()
    else:
      if not os.path.isdir(config.alias_storage):
        os.mkdir(config.alias_storage)
        generate_directories()
      else:
        generate_directories()

  def keys(self, config):
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

class tools:

  def ynq(self, question, function, attributes):
    gen = input(question + " [y/N] ").upper()
    if gen in ("Y","N",""):
      if gen == "Y":
        function(attributes)
      else:
        print("exiting")
        exit()
    else:
      print("invalid input\nexiting")
      exit()
