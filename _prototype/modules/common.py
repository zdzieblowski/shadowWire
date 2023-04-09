import os

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

class tools:
  def isFile(self, path):
    return os.path.isfile(path)

  def isDir(self, path):
    return os.path.isdir(path)

  def mkDir(self, path):
    os.mkdir(path)

  def rmFile(self, path):
    os.remove(path)

  def rmDir(self, path):
    os.rmdir(path)

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

    key = rsa.generate_private_key(public_exponent = 65537, key_size = 4096)

    # ADD KEYFILE ENCRYPTION
    f = open(config.private_key, "xb")
    f.write(key.private_bytes(encoding = serialization.Encoding.PEM, format = serialization.PrivateFormat.TraditionalOpenSSL, encryption_algorithm = serialization.NoEncryption()))
    f.close()

    f = open(config.public_key, "xb")
    f.write(key.public_key().public_bytes(encoding = serialization.Encoding.PEM, format = serialization.PublicFormat.SubjectPublicKeyInfo))
    f.close()

    print("keys generated")
    print(key)

  def generatePublicKey(self, config, key):
    f = open(config.public_key, "xb")
    f.write(key.public_key().public_bytes(encoding = serialization.Encoding.PEM, format = serialization.PublicFormat.SubjectPublicKeyInfo))
    f.close()

    print("public key generated")
    print(key.public_key())

  ###

  def importKeys(self, key_file):
    with open(key_file, "rb") as key_data:
      return serialization.load_pem_private_key(key_data.read(), password = None)

  ###

  def purgeAll(self, config):
    print("purging")
    if self.isDir(config.alias_storage):
      for a, (b, c) in enumerate(config.data["directories"].items()):
        temp_dir = os.path.join(config.alias_storage, c["path"])
        for d, (e, f) in enumerate(c["files"].items()):
          temp_file = os.path.join(temp_dir, f)
          #print(temp_file)
          if self.isFile(temp_file):
            self.rmFile(temp_file)
        if self.isDir(temp_dir):
          self.rmDir(temp_dir)
      self.rmDir(config.alias_storage)

  ###

  def askGate(self, question, default, function, attributes):
    ask = input(question + (" [Y/n] " if default == "Y" else " [y/N] ")).upper()

    if ask in ["Y","N",""]:
      let_pass = ["Y",""] if default == "Y" else ["Y"]

      if ask in let_pass:
        function(attributes)
      else:
        print("exiting")
        exit()
    else:
      print("invalid input\nexiting")
      exit()
