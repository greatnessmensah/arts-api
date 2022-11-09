from api import create_app
from api import db

app = create_app()

db.init_app(app)
with app.app_context(): 
    db.create_all()


if __name__ == "__main__":
    app.run()