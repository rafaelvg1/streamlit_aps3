import streamlit as st  # Streamlit é utilizado para criar interfaces web 
import pandas as pd  
import requests  # Requests é utilizado para fazer requisições HTTP (GET, POST, etc.)
import requests
import streamlit as st

BASE_URL = "http://127.0.0.1:5000"

# Função para adicionar um novo usuário
def post_usuario(BASE_URL, nome, cpf, data_nascimento):
    data = {
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento
    }
    
    url = f"{BASE_URL}/usuario"
    
    response = requests.post(url, json=data)
    
    if response.status_code == 201:
        st.success("Usuário adicionado com sucesso!")
    elif response.status_code == 400:
        st.error(f"Erro: {response.json()['erro']}")
    else:
        st.error(f"Erro desconhecido: {response.text}")

# Função para listar usuários
def get_usuarios(BASE_URL):
    url = f"{BASE_URL}/usuario"
    response = requests.get(url)
    
    if response.status_code == 200:
        usuarios = response.json()["usuarios"]
        return usuarios
    else:
        st.error("Erro ao buscar usuários")
        return []

# Função para atualizar um usuário
def put_usuarios(id_usuario, BASE_URL, nome_put, cpf_put, data_nascimento_put):
    url = f"{BASE_URL}/usuario/{id_usuario}"
    data = {
        "nome": nome_put,
        "cpf": cpf_put,
        "data_nascimento": data_nascimento_put
    }
    response = requests.put(url, json=data)
    if response.status_code == 201:
        st.success("Usuário atualizado com sucesso!")
    elif response.status_code == 400:
        st.error(f"Erro: {response.json()['erro']}")
    else:
        st.error(f"Erro desconhecido: {response.text}")

# Interface do Streamlit
st.title("Adicione um usuário!")

# Inputs para capturar os valores do usuário
nome = st.text_input("Digite aqui seu nome completo", key="nome_add")
cpf = st.text_input("Digite aqui seu CPF", key="cpf_add")
data_nascimento = st.text_input("Digite aqui sua data de nascimento", key="data_nascimento_add")

# Botão para adicionar o usuário
if st.button("Adicionar Usuário"):
    post_usuario(BASE_URL, nome, cpf, data_nascimento)

# Atualizar usuário
st.title("Atualize os usuários")
id_usuario = st.text_input("Digite aqui o ID do usuário", key="id_usuario_put")
nome_put = st.text_input("Digite aqui seu nome completo", key="nome_put")
cpf_put = st.text_input("Digite aqui seu CPF", key="cpf_put")
data_nascimento_put = st.text_input("Digite aqui sua data de nascimento", key="data_nascimento_put")

# Botão para atualizar o usuário
if st.button("Atualizar Usuário"):
    put_usuarios(id_usuario, BASE_URL, nome_put, cpf_put, data_nascimento_put)
# Listar usuários
st.title("Lista de usuários")
if st.button("Listar usuários!"):
    usuarios = get_usuarios(BASE_URL)
    st.write("Resultados da Pesquisa")
    st.dataframe(usuarios)








    


