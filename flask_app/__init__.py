from flask import Flask

app = Flask(__name__) 

app.secret_key="Llave secreta" #se utiliza para session