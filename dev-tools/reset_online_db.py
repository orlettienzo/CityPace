"""
Permet de réinitialiser la base de données du site en ligne.
"""

import requests

input("ATTENTION: cette opération va réinitialiser la base de données en ligne. Appuyez sur Entrée pour continuer.")

with open('mobility/secret.txt', 'r', encoding='utf-8') as file:
    secret = file.read().strip()

url = 'https://g25.linfo1002.ovh/resetdb'
data = {'secret': secret}

response = requests.post(url, json=data, timeout=5)

print(response.status_code)
print(response.text)
