from flask import Flask, jsonify, request
import boto3
import json
import os
from boto3.dynamodb.conditions import Key

app = Flask(__name__)

# Creazione della risorsa DynamoDB
dynamodb = boto3.resource('dynamodb')
# Nome della tabella DynamoDB ottenuto dalle variabili di ambiente
table_name = os.environ.get('DYNAMODB_TABLE', 'Users')
# Connessione alla tabella specificata
table = dynamodb.Table(table_name)

@app.route('/createUser', methods=['POST'])
def create_user():
    # Recupera i dati dalla richiesta JSON
    data = request.json
    user_id = data.get('user_id')
    name = data.get('name')

    # Verifica che i campi obbligatori siano presenti
    if not user_id or not name:
        return jsonify({"error": "Please provide user_id and name"}), 400

    # Inserisce l'utente nella tabella DynamoDB
    table.put_item(Item={'user_id': user_id, 'name': name})
    return jsonify({"message": "User created successfully"}), 201

@app.route('/getUserById/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    # Recupera l'utente dalla tabella DynamoDB tramite user_id
    response = table.get_item(Key={'user_id': user_id})
    item = response.get('Item')

    # Verifica se l'utente esiste
    if not item:
        return jsonify({"error": "User not found"}), 404

    return jsonify(item), 200

if __name__ == "__main__":
    app.run(debug=True)
