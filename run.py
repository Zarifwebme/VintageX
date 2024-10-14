from app.models import db
from app.routes import app
from flask_migrate import Migrate

app.config.from_object('config.Config')
db.init_app(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
