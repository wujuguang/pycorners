from sqlalchemy.engine import create_engine

from sqlalchemy.orm import sessionmaker, scoped_session

db_engine = create_engine('', echo=True, pool_recycle=180)
db_session = scoped_session(sessionmaker(bind=db_engine))()
