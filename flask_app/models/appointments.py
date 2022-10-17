from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime 

class Appointment:
    def __init__(self, data):
        self.id = data['id']
        self.tasks = data['tasks']
        self.date = data['date']
        self.status = data['status']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @staticmethod
    def valida_appointment(formulario):
        es_valido = True

        if formulario['tasks'] == '':
            flash('Tareas no puede quedar vacío', 'citas' )
            es_valido = False

        if formulario['status'] == '':
            flash('Elige un estado', 'citas' )
            es_valido = False

        if formulario['date'] =='':
            flash('Ingrese una fecha', 'citas' )
            es_valido = False
        else: 
            fecha_obj = datetime.strptime(formulario['date'] , '%Y-%m-%d')
            hoy =datetime.now()
            if hoy > fecha_obj:
                flash('La fecha debe ser futura', 'citas' )
                es_valido = False

        return es_valido

    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO appointments (tasks, date, status, user_id) VALUES (%(tasks)s, %(date)s, %(status)s, %(user_id)s)"
        result = connectToMySQL('citas').query_db(query, formulario)
        return result

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM  appointments WHERE DATE(date) >=DATE(NOW());"
        results = connectToMySQL('citas').query_db(query)
        appointments =[]

        for appointment in results:
            appointments.append(cls(appointment))
        return appointments

    @classmethod
    def get_by_date(cls):
        query = "SELECT * FROM  appointments WHERE DATE(date) < DATE(NOW());"
        results = connectToMySQL('citas').query_db(query)
        dates=[]

        for date in results:
            dates.append(cls(date))
        return dates

        
    @classmethod
    def get_by_id(cls, formulario):
        query="SELECT * FROM appointments WHERE id = %(id)s"
        result= connectToMySQL('citas').query_db(query, formulario)
        appointment=cls(result[0])
        return appointment

    @classmethod
    def update(cls,formulario):
        query = "UPDATE appointments SET tasks=%(tasks)s, date=%(date)s, status=%(status)s, user_id=%(user_id)s WHERE id=%(id)s"
        result= connectToMySQL('citas').query_db(query, formulario)
        return result

    @classmethod
    def delete(cls, formulario):
        query = "DELETE FROM appointments WHERE id = %(id)s"
        result = connectToMySQL('citas').query_db(query, formulario)
        return result



#if formulario['date'] =='':
#            flash('Ingrese una fecha', 'citas' )
#            es_valido = True
#        else: 
#            fecha_obj = datetime.strptime(formulario['date'] , '%Y-%m-%d')
#            hoy =datetime.now()
#            if hoy < fecha_obj:
#                flash('La fecha debe ser en pasado', 'appointment' )
#               es_valido = False
