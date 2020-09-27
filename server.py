from app.main import create_app, db
from flask_migrate import Migrate

app = create_app("development")
migrate = Migrate(app, db)

@app.route("/")
def home():
    return "Welcome!"