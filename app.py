from flask import Flask
from models import db
import secrets
# from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)


    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
    app.secret_key = secrets.token_hex(16)
    # migrate=Migrate(app,db)

    db.init_app(app)


    with app.app_context():

        db.create_all()
        
        import app_data
        import routes
        

    return app

app = create_app()

if __name__ =="__main__":
    
    app.run(debug=True ,port=8000)