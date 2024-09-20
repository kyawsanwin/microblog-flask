import uuid


SECRET_KEY = str(uuid.uuid4())
SQLALCHEMY_DATABASE_URI = "sqlite:///project.db"
