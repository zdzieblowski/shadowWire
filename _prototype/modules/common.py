import os
from Crypto.PublicKey import ECC

class tools:
  ###

  def isFile(self, path):
    return os.path.isfile(path)

  def isDir(self, path):
    return os.path.isdir(path)

  def mkDir(self, path):
    os.mkdir(path)

  def rmFile(self, path):
    os.remove(path)

  ###

  def generateDirs(self, config):
    def generateFromJSON():
      for index, (key, value) in enumerate(config.data["directories"].items()):
        temp_path = os.path.join(config.alias_storage, value["path"])
        if not self.isDir(temp_path):
          self.mkDir(temp_path)

    if not self.isDir(config.storage):
      self.mkDir(config.storage)
      self.mkDir(config.alias_storage)
    else:
      if not self.isDir(config.alias_storage):
        self.mkDir(config.alias_storage)
    generateFromJSON()

  def generateKeys(self, config):
    if self.isFile(config.private_key):
      self.rmFile(config.private_key)
    if self.isFile(config.public_key):
      self.rmFile(config.public_key)

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

  def importKey(self, key_file):
    return ECC.import_key(key_file.read())

  ###

  def noGate(self, question, function, attributes):
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
