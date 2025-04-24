import trivia_client

# Intenta registrar un usuario
name="kevin"
password="pass"
url="http://localhost:80"
print(trivia_client.registerUser(url,name,password))


# Inicia sesión con usuario
print(trivia_client.openSession(url,name,password))

# Actualiza puntaje del usuario
score=1000
print(trivia_client.updateScore(url,name,password,score))

# Obtiene puntaje del usuario
print(trivia_client.getScore(url,name,password))

# Obtiene lista de usuarios conectados
print(trivia_client.getList(url,name,password))

# Obtiene pregunta de la categoría 0
cat=0
print(trivia_client.getQuestion(url,name,password,cat))

# Cierra sesión con usuario
print(trivia_client.closeSession(url,name,password))
