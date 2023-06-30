from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

myhost = os.environ.get("HOST")
myport = os.environ.get("PORT")
mybd = os.environ.get("BD")

SessionLocal = any

#engine= create_engine("postgresql://7PkwHDkCYpwjUP625xYJ:vP2whxwQS78]PH}n.*(X@pruebaapi.crsfqfthjuif.eu-west-1.rds.amazonaws.com/ec2ceapifmc",
#    echo=True
#)
try:
	engine= create_engine("postgresql://postgres:postgres@"+myhost+":"+myport+"/"+mybd, pool_pre_ping=True,
	    echo=True
	)

	Base = declarative_base()

	SessionLocal = sessionmaker(bind=engine)

except:
	SessionLocal.rollback()
