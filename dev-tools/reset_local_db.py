"""
Permet de réinitialiser la base de données locale.
"""

import requests

with open('mobility/secret.txt', 'r', encoding='utf-8') as file:
    secret = file.read().strip()

url = 'http://localhost:5000/resetdb'
data = {'secret': secret}

response = requests.post(url, json=data, timeout=5)

print(response.status_code)
print(response.text)
