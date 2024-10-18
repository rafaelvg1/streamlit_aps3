from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import os
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId
from dotenv import *


app = Flask(__name__)
load_dotenv(".cred")
app.config["MONGO_URI"] = os.getenv("MONGO_URI","localhost")

mongo = PyMongo(app)




@app.route('/usuario', methods=['POST'])
def post_usuario():
    
    data = request.json
    obrigatorio = ["nome", "cpf", "data_nascimento"]
    
    for objeto in obrigatorio:
        if objeto not in data:
            return {"erro": f"{objeto} é obrigatório"}, 400
        if objeto == "data_nascimento" and data["data_nascimento"]=="":
            return {"erro": f"{objeto} é obrigatório"}, 400

    
    # Verificar se o CPF já existe no banco de dados
    cpf_existente = mongo.db.usuarios.find_one({"cpf": data["cpf"]})
    
    if cpf_existente:
        return {"erro": "CPF já está cadastrado"}, 400

  
    result = mongo.db.usuarios.insert_one(data)

    return {"id": str(result.inserted_id)}, 201 

@app.route('/usuario', methods=["GET"])
def get_usuarios():
    filtro = {}
    projecao = {"_id" :0}
    dados_usuarios = mongo.db.usuarios.find(filtro,projecao)

    resp = {
        "usuarios": list( dados_usuarios )}
    return resp,200

@app.route('/usuario/<id>', methods=["GET"])
def get_usuario_por_id(id):
    try:
        
        filtro = {"_id": ObjectId(id)}

        projecao = {"_id": 0}  

        usuario = mongo.db.usuarios.find_one(filtro, projecao)

        return {"usuario":f"{str(usuario)}"}, 200

    except Exception as erro:
        return {"erro": f"Erro ao buscar usuário: {str(erro)}"}, 400



@app.route("/usuario/<id>", methods=["DELETE"])
def delete_usuario_por_id(id):
    try:
        filtro={"_id":ObjectId(id)}
        
        usuario=mongo.db.usuarios.delete_one(filtro)
        return {"sucesso": "Sucesso ao deletar usuário!"},200

    except Exception as erro:
            return {"erro":F"Erro ao deletar o usuário: {str(erro)}"}, 400

@app.route("/usuario/<id>", methods=["PUT"])
def put_usuario_por_id(id):
    try:
        filtro={"_id":ObjectId(id)}   
        dados_atualizados=request.json
        

        usuario = mongo.db.usuarios.update_one(filtro, {"$set": dados_atualizados})
        return {"sucesso":"sucesso ao atualizar o usuario"},200
    except Exception as erro:
        return {"erro":f"erro ao atualizar usuário: {str(erro)}"}, 400

# buscar bicicleta por id
@app.route('/bikes/<id_bike>', methods=['GET'])
def get_bike(id_bike):
    bike = mongo.db.bikes.find_one({"_id":ObjectId(id_bike)}, {"_id": 0})  
    if bike is None:
        return {"erro": "Bicicleta não encontrada"}, 404

    return jsonify(bike), 200

# adicionar uma nova bicicleta
@app.route('/bikes', methods=['POST'])
def criar_bike():
    data = request.json

    if "marca" not in data or "modelo" not in data or "cidade" not in data or "status" not in data:
        return {"erro": "Todos os campos (marca, modelo, cidade, status) são obrigatórios"}, 400
    
    if data["status"] not in ["disponivel", "em uso"]:
        return {"erro": "Status inválido. Deve ser 'disponivel' ou 'em uso'."}, 400

    result = mongo.db.bikes.insert_one(data)

    return {"id": str(result.inserted_id)}, 201

# atualizar bicicleta
@app.route('/bikes/<id_bike>', methods=['PUT'])
def update_bike(id_bike):
    data = request.json

    if mongo.db.bikes.find_one({"_id": id_bike}) is None:
        return {"erro": "Bicicleta não encontrada"}, 404

    mongo.db.bikes.update_one({"_id": id_bike}, {"$set": data})

    return {"mensagem": "Bicicleta atualizada com sucesso."}, 200

# deletar bicicleta
@app.route('/bikes/<id_bike>', methods=['DELETE'])
def delete_bike(id_bike):

    
    result = mongo.db.bikes.delete_one({"_id": id_bike})

    if result.deleted_count == 0:
        return {"erro": "Bicicleta não encontrada"}, 404

    return {"mensagem": "Bicicleta deletada com sucesso."}, 200

# listar todas as bicicletas
@app.route('/bikes', methods=['GET'])
def get_all_bikes():

    filtro = {}
    projecao = {"_id" : 0}
    dados_bikes = mongo.db.bikes.find(filtro, projecao)

    resp = {
        "bicicletas": list( dados_bikes )

    }

    return resp, 200

@app.route("/emprestimo", methods=["GET"])
def get_todos_empretimos():
    try:
        filtro={}
        projecao={"id_usario":1,"_id":1,"id_bicicleta":1}

        emprestimo=mongo.db.emprestimos.find_one(filtro,projecao)
        return {"empretimos":f"{list(emprestimo)}"}
    except Exception as erro:
        return {"erro":f"erro ao listar emprestimos:{str(erro)}"}
    
@app.route("/emprestimo/usuario/<id_usuario>/bikes/<id_bike>", methods=["POST"])
def post_emprestimo(id_bike,id_usuario):
    try:
        data_aluguel=request.json
        filtro_bike={"_id":ObjectId(id_bike)}
        projecao_bike={"_id":1,"status":1}
        filtro_usuario={"_id":ObjectId(id_usuario)}
        projecao_usuario={"_id":1}
        id_usuario = mongo.db.usuarios.find_one(filtro_usuario, projecao_usuario)
        id_bike=mongo.db.bikes.find_one(filtro_bike,projecao_bike)
        if id_bike["status"]=="em uso":
            return{"erro":"bicicleta está indisponível para locação"}
        if id_usuario is None:
            return{"erro": "Usuario não encontrado"}
        if id_bike is None:
            return {"erro": "Bike não encontrada"}, 404
        dados={"id_bike":id_bike["_id"],"data_aluguel":data_aluguel["data_aluguel"],"id_usuario":id_usuario["_id"]}
        emprestimo=mongo.db.emprestimos.insert_one(dados)
        old_values = { "status": "disponivel" }
        new_values = { "$set": { "status": "em uso" } }
        update_status=mongo.db.bikes.update_one(old_values,new_values)
        return{"sucesso":"sucesso ao realizar o empréstimo"}
    except Exception as erro:
        return{"erro":f"erro ao realizar o empréstimo:{str(erro)}"}
@app.route("/emprestimo/bikes", methods=["GET"])
def get_todos_emprestimos():
    try:
        filtro = {}
        # Ajuste a projeção para incluir o _id e outros campos
        projecao = {"_id": 1, "id_bike": 1, "data_aluguel": 1, "id_usuario": 1}
        
        # Use find para retornar todos os empréstimos
        emprestimos = mongo.db.emprestimos.find(filtro, projecao)
        
        # Converta o cursor retornado pelo find em uma lista, e os ObjectIds em strings
        emprestimos_list = []
        for emprestimo in emprestimos:
            # Verifique e converta todos os ObjectIds para string
            if "_id" in emprestimo:
                emprestimo["_id"] = str(emprestimo["_id"])
            if "id_bike" in emprestimo and isinstance(emprestimo["id_bike"], ObjectId):
                emprestimo["id_bike"] = str(emprestimo["id_bike"])
            if "id_usuario" in emprestimo and isinstance(emprestimo["id_usuario"], ObjectId):
                emprestimo["id_usuario"] = str(emprestimo["id_usuario"])
            
            emprestimos_list.append(emprestimo)
        
        return {"emprestimos": emprestimos_list}, 200
    except Exception as erro:
        return {"erro": f"Erro ao listar os empréstimos: {str(erro)}"}, 400
    
@app.route("/emprestimo/<id_emprestimo>", methods=["DELETE"])
def delete_emprestimo(id_emprestimo):
    try:
        filtro={"_id":ObjectId(id_emprestimo)}
        mongo.db.emprestimos.delete_one(filtro)
        return {"sucesso":"emprestimo deletado com sucesso"}
    except Exception as erro:
        return {"erro":f"erro ao deletar o emprestimo:{str(erro)}"}
@app.route("/emprestimo/usuario/<id_usuario>")
def get_emprestimo_por_usuario(id_usuario):
    try:
        # Filtro para buscar o empréstimo pelo ID do usuário
        filtro = {"id_usuario": ObjectId(id_usuario)}

        # Busca o empréstimo correspondente
        emprestimo = mongo.db.emprestimos.find_one(filtro)

        # Verifica se o empréstimo foi encontrado
        if emprestimo is None:
            return {"erro": "Empréstimo não encontrado"}, 404

        # Converte os ObjectIds para string
        if "_id" in emprestimo:
            emprestimo["_id"] = str(emprestimo["_id"])
        if "id_bike" in emprestimo and isinstance(emprestimo["id_bike"], ObjectId):
            emprestimo["id_bike"] = str(emprestimo["id_bike"])
        if "id_usuario" in emprestimo and isinstance(emprestimo["id_usuario"], ObjectId):
            emprestimo["id_usuario"] = str(emprestimo["id_usuario"])

        return {"emprestimo": emprestimo}, 200
    except Exception as erro:
        return {"erro": f"Erro ao buscar empréstimo: {str(erro)}"}, 400
@app.route("/emprestimo/bikes/<id_bike>")
def get_emprestimo_por_bike(id_bike):
    try:
        # Filtro para buscar o empréstimo pelo ID do usuário
        filtro = {"id_bike": ObjectId(id_bike)}

        # Busca o empréstimo correspondente
        emprestimo = mongo.db.emprestimos.find_one(filtro)

        # Verifica se o empréstimo foi encontrado
        if emprestimo is None:
            return {"erro": "Empréstimo não encontrado"}, 404

        # Converte os ObjectIds para string
        if "_id" in emprestimo:
            emprestimo["_id"] = str(emprestimo["_id"])
        if "id_bike" in emprestimo and isinstance(emprestimo["id_bike"], ObjectId):
            emprestimo["id_bike"] = str(emprestimo["id_bike"])
        if "id_usuario" in emprestimo and isinstance(emprestimo["id_usuario"], ObjectId):
            emprestimo["id_usuario"] = str(emprestimo["id_usuario"])

        return {"emprestimo": emprestimo}, 200
    except Exception as erro:
        return {"erro": f"Erro ao buscar empréstimo: {str(erro)}"}, 400

if __name__ == '__main__':
    app.run(debug=True)