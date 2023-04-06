import json
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
