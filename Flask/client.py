import requests
headers = {'Content-Type': 'application/json'}
# URL = 'http://app:5000/ads/'
URL = 'http://127.0.0.1:5001/ads/'
# URL = 'http://localhost:1234/ads/'
# URL ="http://172.30.0.3:5000/ads/"
response = requests.post(URL, json={'header': 'salt_3', 'description': '1234', 'owner': 'max'})
print(response.status_code)
print(response.text)

# response = requests.delete('http://127.0.0.1:5000/ads/1')
# print(response.status_code)
# print(response.text)

response = requests.get(f'{URL}1')
print(response.status_code)
print(response)
