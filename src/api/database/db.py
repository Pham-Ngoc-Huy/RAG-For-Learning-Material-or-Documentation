from databases import Database
from sqlalchemy import MetaData, create_engine

DATABASE_URL = "sqlite:///./users.db"
# explain the syntax of the DATABASE_URL
# the `sqlliet:///` prefix indicates that we are using SQLite as the database engine at the `relative path`
# `./users.db` indicates that the database file is located in the current working directory and name is "users.db"
database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL)
