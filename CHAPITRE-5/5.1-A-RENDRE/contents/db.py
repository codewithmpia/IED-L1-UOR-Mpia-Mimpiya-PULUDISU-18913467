import mysql.connector
from .utils import get_env_vars
from flask import abort

def get_db_connection():
    """
    Renvoie une connexion à la base de données MySQL.
    Si une erreur se produit lors de la connexion, une exception est levée.
    """
    try:
        # Création de la connexion à la base de données
        conn = mysql.connector.connect(
            host=get_env_vars("DATABASE_HOST", "localhost"),
            user=get_env_vars("DATABASE_USER", "root"),
            password=get_env_vars("DATABASE_PASSWORD", "Mpia251095,;"),
            database=get_env_vars("DATABASE_NAME", "blog"),
        )
        return conn
    
    except mysql.connector.Error as e:
        raise e
       

def create_tables():
    """
    Crée les tables nécessaires dans la base de données.
    """
    conn = get_db_connection()
    if conn is None:
        return
    cursor = conn.cursor()
    try:
        # Création de la table posts
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id INT AUTO_INCREMENT PRIMARY KEY, 
                title VARCHAR(255), 
                author VARCHAR(255) DEFAULT 'admin', 
                resume TEXT,
                content TEXT, 
                image VARCHAR(255),
                views INT DEFAULT 0,
                link VARCHAR(255),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
                publish BOOLEAN DEFAULT 0
            )
            """
        )
        # Création de la table comments
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS comments (
                id INT AUTO_INCREMENT PRIMARY KEY, 
                post_id INT,
                author VARCHAR(255), 
                email VARCHAR(255),
                message TEXT, 
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
                active BOOLEAN DEFAULT 1,
                FOREIGN KEY (post_id) REFERENCES posts(id)
            )
            """
        )
        # Validation des changements
        conn.commit()
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
