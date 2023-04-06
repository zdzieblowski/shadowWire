import json
import os

class configuration:

  def __init__(self, config_path, config_alias):

    with open(config_path) as config_file:
      self.data = json.load(config_file)

      self.storage = os.path.join(os.path.expanduser("~"), self.data["main_storage"])
      self.alias_storage = os.path.join(self.storage, config_alias)

      app_store = self.data["directories"]["app_storage"]
      key_store = self.data["directories"]["key_storage"]

      self.app_storage = os.path.join(self.alias_storage, app_store["path"])
      self.key_storage = os.path.join(self.alias_storage, key_store["path"])

      self.private_key = os.path.join(self.key_storage, key_store["files"]["private_keyfile"])
      self.public_key = os.path.join(self.key_storage, key_store["files"]["public_keyfile"])

      self.ecc_curve = self.data["ecc_curve"]
