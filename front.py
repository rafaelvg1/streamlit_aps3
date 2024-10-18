import streamlit as st  # Streamlit é utilizado para criar interfaces web 
import pandas as pd  
import requests  # Requests é utilizado para fazer requisições HTTP (GET, POST, etc.)

# Base URL da API do backend (Flask)
BASE_URL = "https://aps-3.onrender.com/"
# Definimos a base URL onde o backend está rodando (localmente no endereço 127.0.0.1 na porta 5000).
# Todas as requisições da aplicação serão enviadas para esse endpoint (ou serviço), concatenando o recurso desejado.

# Função genérica para fazer requisições ao backend
def fazer_requisicao(endpoint, method="GET", params=None, data=None):
    # Constrói a URL completa concatenando o endpoint específico com a base URL
    url = f"{BASE_URL}/{endpoint}"

    # Monta a requisição de acordo com o método HTTP fornecido
    try:
        if method == "GET":
            response = requests.get(url, params=params)
            # Método GET: Envia os parâmetros da requisição (params) como query strings na URL.
            # Exemplo: /imoveis?tipo_imovel=Casa&preco_min=200000&preco_max=1000000

        elif method == "POST":
            response = requests.post(url, json=data)
            # Método POST: Envia os dados no corpo da requisição em formato JSON para criar novos recursos no backend.
            # Exemplo: POST /imoveis para criar um novo imóvel, enviando os detalhes no corpo da requisição.

        elif method == "PUT":
            response = requests.put(url, json=data)
            # Método PUT: Envia os dados no corpo da requisição em formato JSON para atualizar um recurso existente.

        elif method == "DELETE":
            response = requests.delete(url, params=params)
            # Método DELETE: Envia parâmetros na URL para deletar um recurso específico no backend.

        else:
            st.error("Método HTTP não suportado.")
            # Caso um método HTTP não suportado seja passado, exibe um erro no frontend do Streamlit.

        # Verifica o status HTTP da resposta
        if response.status_code == 200:
            return response.json()  # Resposta 200 (OK): Retorna o corpo da resposta como um JSON (dicionário Python).
        elif response.status_code == 404:
            st.warning("⚠️ Recurso não encontrado.")
            # Se o status for 404 (Not Found), exibe um aviso de que o recurso não foi encontrado.
        elif response.status_code == 500:
            st.error("⚠️ Erro interno do servidor.")
            # Se o status for 500 (Internal Server Error), exibe um erro genérico de servidor.
        else:
            st.error(f"⚠️ Erro: {response.status_code} - {response.text}")
            # Para outros códigos de status, exibe um erro genérico mostrando o código e a mensagem da resposta.

        return None  # Se não houver sucesso, retorna None para indicar falha.

    except Exception as e:
        st.error(f"⚠️ Erro de conexão: {e}")
        # Captura e exibe exceções, como erros de conexão ou outros problemas ao tentar fazer a requisição.
        return None

# Título e subtítulo da interface do aplicativo Streamlit
st.title("Painel de Controle das Bicicletas")



if st.button(""):
    st.switch_page("pages/usuarios.py")
    st.switch_page("pages/bicicletas.py")
    st.switch_page("pages/emprestimos.py")







