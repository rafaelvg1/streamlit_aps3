from front import *

BASE_URL = "https://aps-3.onrender.com/"

# Função para adicionar um novo usuário
def post_emprestimos(BASE_URL, data_aluguel,id_usuario,id_bike):
    data = {
        "data_aluguel": data_aluguel
    }
    
    url = f"{BASE_URL}/emprestimo/usuario/{id_usuario}/bikes/{id_bike}"
    
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
st.title("Faça um emprestimo!")

# Inputs para capturar os valores do usuário
id_bike = st.text_input("Digite aqui ID da bicicleta", key="id_bike_add")
id_usuario = st.text_input("Digite aqui o ID do usuário", key="id_usuario_add")
data_aluguel= st.text_input("Digite aqui a data do alguel", key="data_aluguel_add")


# Botão para adicionar o usuário
if st.button("Fazer Empréstimo"):
    post_emprestimos(BASE_URL, id_bike, id_usuario, data_aluguel)

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