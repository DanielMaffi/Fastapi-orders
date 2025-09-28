import requests

header = {
    "Authorization": "Bearer <TOKEN_AQUI>"
}

requisicao = requests.get("http://127.0.0.1:8000/auth/refresh", headers=header)
print(requisicao)
print(requisicao.json())