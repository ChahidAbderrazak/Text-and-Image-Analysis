import os

from ensure import ensure_annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils.common_utils import load_env_variables

os.environ["GIT_PYTHON_REFRESH"] = "quiet"




@ensure_annotations
def setup_database(database_type: str = "PostgreSQL") -> dict:
    # searching/load for the env files
    load_env_variables()
    if database_type == "MySQL":
        # getting the MySQL  credentials
        database_credentials = {
            "username": os.getenv("MYSQL_USER"),
            "password": os.getenv("MYSQL_PASSWORD"),
            "database": os.getenv("MYSQL_DATABASE"),
            "host": os.getenv("MySQL_CNTNR_IP"),
        }
        return database_credentials
    elif database_type == "PostgreSQL":
        database_credentials = {
            "username": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
            "database": os.getenv("POSTGRES_DATABASE"),
            "host": os.getenv("POSTGRES_CNTNR_IP"),
            "port": os.getenv("POSTGRES_HOST_PORT"),
        }
        return database_credentials
    else:
        raise f" datatabse type {database_type} is not define"


@ensure_annotations
def get_create_table_query(table_name):

    create_table_query = f"""
                CREATE TABLE {table_name} (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100),
                        description TEXT,
                        price DECIMAL(10, 2)
                        );
                """
    return create_table_query
