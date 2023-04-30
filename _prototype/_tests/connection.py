import requests

url = "http://localhost:60606/read"
myobj = {"key": "value"}

x = requests.post(url, json = myobj)

print(x.text)
