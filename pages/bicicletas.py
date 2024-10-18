from front import *

BASE_URL = "http://127.0.0.1:5000"

# Função para adicionar um novo usuário
def post_bikes(BASE_URL, modelo, marca, cidade,status):
    data = {
        "modelo": modelo,
        "marca": marca,
        "cidade": cidade,
        "status":status
    }
    
    url = f"{BASE_URL}/bikes"
    
    response = requests.post(url, json=data)
    
    if response.status_code == 201:
        st.success("Bicicleta adicionada com sucesso!")
    elif response.status_code == 400:
        st.error(f"Erro: {response.json()['erro']}")
    else:
        st.error(f"Erro desconhecido: {response.text}")

# Função para listar usuários
def get_bikes(BASE_URL):
    url = f"{BASE_URL}/bikes"
    response = requests.get(url)
    
    if response.status_code == 200:
        bikes = response.json()["bicicletas"]
        return bikes
    else:
        st.error("Erro ao buscar bicicleta")
        return []

# Função para atualizar um usuário
def put_bikes(id_bike, BASE_URL, modelo_put, marca_put, cidade_put,status_put):
    url = f"{BASE_URL}/usuario/{id_bike}"
    data = {
        "modelo": modelo_put,
        "marca": marca_put,
        "cidade": cidade_put,
        "status":status_put
    }
    response = requests.put(url, json=data)
    if response.status_code == 201:
        st.success("Usuário atualizado com sucesso!")
    elif response.status_code == 400:
        st.error(f"Erro: {response.json()['erro']}")
    else:
        st.error(f"Erro desconhecido: {response.text}")

# Interface do Streamlit
st.title("Adicione uma bicicleta!")

# Inputs para capturar os valores do usuário
modelo = st.text_input("Digite aqui o modelo", key="modelo_add")
marca = st.text_input("Digite aqui a marca", key="marca_add")
cidade = st.text_input("Digite aqui a cidade", key="cidade_add")
status = st.text_input("Digite o status de disponibilidade", key="status_add")

# Botão para adicionar o usuário
if st.button("Adicionar Bicicleta"):
    post_bikes(BASE_URL, modelo, marca, cidade, status)

# Atualizar usuário
st.title("Atualize as bicicletas")
id_bike = st.text_input("Digite aqui o ID da bicicleta", key="id_bike_put")
marca_put = st.text_input("Digite aqui a marca da bicicleta", key="marca_put")
cidade_put = st.text_input("Digite aqui a cidade", key="cidade_put")
modelo_put = st.text_input("Digite aqui o modelo", key="modelo_put")
status_put = st.text_input("Digite aqui o status de disponibilidade da bicicleta", key="status_put")
# Botão para atualizar o usuário
if st.button("Atualizar Usuário"):
    put_bikes(id_bike, BASE_URL, modelo_put, marca_put, cidade_put,status_put)
# Listar usuários
st.title("Lista de bicicletas")
if st.button("Listar biciletas!"):
    usuarios = get_bikes(BASE_URL)
    st.write("Resultados da Pesquisa")
    st.dataframe(usuarios)