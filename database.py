"""Database engine & session creation."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import credentials


# read data
hostname = credentials.hostname
dbname = credentials.dbname
uname = credentials.uname
pwd = credentials.pwd

engine = create_engine(f"mysql+pymysql://{uname}:{pwd}@{hostname}/{dbname}")

Session = sessionmaker(bind=engine)
session = Session()