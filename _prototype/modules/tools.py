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
