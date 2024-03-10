"""
Permet de réinitialiser la base de données locale.
"""

import requests


url = 'http://localhost:5000/resetdb'
data = {'secret': 'Acgfi9^Ziy!$zpY39CRg4Ww7ZjbmHHwdnbkYYbVen6HN*&ZiY9y$QDU8fB$ED*8tBR!BAwUwA^STjcgXPkUY*oUe*S9YY@D$WEfuK4gA%vDC$mE7&j9tH&Js#6yJJ88D'}

response = requests.post(url, json=data)

print(response.status_code)
print(response.text)