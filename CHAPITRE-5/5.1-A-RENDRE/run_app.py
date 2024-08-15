from contents.settings import app
from contents.db import get_db_connection, create_tables

if __name__ == "__main__":
  get_db_connection()
  create_tables()
  app.run(debug=True)
