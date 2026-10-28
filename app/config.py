import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://inventory_user:inventory_password@localhost:5432/inventory_db"
)
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_THIS_DEVELOPMENT_SECRET_BEFORE_DEPLOYMENT")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
