from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker
from typing import Union, Optional


class SQLDatabase:
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)

    def execute_query(self, query):
        with self.Session() as session:
            if isinstance(query, str):
                query = text(query)  # Convert string query to SQL text
            result = session.execute(query)
            return result.fetchall()

class SQLDatabaseLoader:
    def __init__(self, query: Union[str, select], db: SQLDatabase, fetch_mode: Optional[str] = "all"):
        self.query = query
        self.db = db
        self.fetch_mode = fetch_mode

    def load_data(self):
        if self.fetch_mode == "all":
            return self.db.execute_query(self.query)
        else:
            raise ValueError("Unsupported fetch mode")
