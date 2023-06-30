from sqlalchemy.sql.expression import null
from .database import Base
from sqlalchemy import String,Boolean,Integer,Column,Text,Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import *
from geoalchemy2 import Geometry


# class Pred(Base):
# 	__tablename__ = 'pred_data'
# 	id =  Column(Integer, primary_key=True, index=True)
# 	id_trap = Column(VARCHAR)
# 	pred_time = Column(DATE)
# 	type = Column(Integer)
# 	h1 = Column(Float)
# 	h2 = Column(Float)
# 	h3 = Column(Float)
# 	h4 = Column(Float)
# 	ph1 = Column(Float)

# 	def __repr__(self):
# 		return f"<Spot_id={self.id_trap} type={self.type}>"
	
class Municipios(Base):
	__tablename__ = 'municipio'
	id_dera =  Column(Integer, primary_key=True, index=True)
	cod_mun = Column(VARCHAR)
	nombre = Column(VARCHAR)
	provincia = Column(VARCHAR)

	def __repr__(self):
		return f"<id_dera={self.id_dera} cod_mun={self.cod_mun}>"  
