import os

class tools:

  def ynq(self, question, function):
    gen = input(question + " [y/N] ").upper()
    if gen in ("Y","N",""):
      if gen == "Y":
        function()
      else:
        print("exiting")
        exit()
    else:
      print("invalid input\nexiting")
      exit()

  def gen_dirs(self, config):
    def generate_directories():
      for index, (key, value) in enumerate(config.data["directories"].items()):
        temp_path = os.path.join(config.alias_storage, value["path"])
        if not os.path.isdir(temp_path):
          os.mkdir(temp_path)

    if not os.path.isdir(config.storage):
      os.mkdir(config.storage)
      generate_directories()
    else:
      if not os.path.isdir(config.alias_storage):
        os.mkdir(config.alias_storage)
        generate_directories()
      else:
        generate_directories()
