import requests
import json

url = "http://127.0.0.1:8080/calculate"
data = {"expression": "10 * 5 - 2"}
headers = {'Content-type': 'application/json'}
response = requests.post(url, data=json.dumps(data), headers=headers)
print(response.json())