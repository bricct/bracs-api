from app.schema import *
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from app.utils import load_app_config

if __name__ == "__main__":
    app_config = load_app_config()
    engine = create_engine(app_config['database_uri'])

    session = scoped_session(sessionmaker())
    session.configure(bind=engine, autoflush=False, expire_on_commit=False)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
