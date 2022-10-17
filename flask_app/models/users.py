from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash

import re
EMAIL_REGEX =re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    def validar_usuario(formulario):
        es_valido = True
        if len(formulario['first_name']) <3:
            flash('Nombre debe tener al menos 3 carácteres', 'registro' )
            es_valido = False

        if len(formulario['last_name']) <3:
            flash('Apellido debe tener al menos 3 carácteres', 'registro' )
            es_valido = False

    #valiar password
        if len(formulario['password']) <8:
            flash('Contraseña debe tener al menos 6 carácteres', 'registro' )
            es_valido = False

    #validar las dos contraseñas
        if formulario['password'] != formulario['confirm_password']:
            flash('Contraseñas No coinciden', 'registro' )
            es_valido = False
    
    #Consulta a sql si exixte correo
        if not EMAIL_REGEX.match(formulario['email']):
            flash('Email inválido', 'registro')
            es_valido = False
    
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('log_reg').query_db(query, formulario)
        if len(results) >=1:
            flash('Email registrado previamente', 'registro')
            es_valido = False

        return es_valido

    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s,  %(password)s)"
        result = connectToMySQL('citas').query_db(query, formulario)
        return result


#parte de login
    @classmethod
    def get_by_email(cls, formulario):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('citas').query_db(query, formulario)
        if len(result) < 1:
            return False
        else:
            user = cls(result[0])
            return user

    @classmethod
    def get_by_id(cls, formulario):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('citas').query_db(query, formulario)
        user = cls(result[0])
        return user
