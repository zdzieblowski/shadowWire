import requests

url = "http://localhost:60606/read"

try:
  # port is open
  query = {"height": 0}
  req = requests.post(url, json = query)

  if req.status_code == 200:
    # all worked
    print("{0} {1} ".format(req.elapsed, req.text))
  else:
    print(req.status_code)

  #print(req.__dict__)
except Exception as e:
  #port is closed
  print(e)
