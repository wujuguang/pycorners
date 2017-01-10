from __future__ import unicode_literals, print_function

from sqlalchemy.engine import create_engine

from sqlalchemy.orm import sessionmaker, scoped_session
from envcfg.json.demo import DEBUG, MYSQL_CONNECTION_STRING

debug = bool(DEBUG)
db_engine = create_engine(
    MYSQL_CONNECTION_STRING, echo=debug, pool_recycle=180)
db_session = scoped_session(sessionmaker(bind=db_engine))()

if __name__ == '__main__':
    print(DEBUG)
    print(MYSQL_CONNECTION_STRING)
