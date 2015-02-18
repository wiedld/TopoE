from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
# from sqlalchemy.orm import relationship, backref, scoped_session


Base = declarative_base()

#######################################################################

##  STEP1 = make the db file and metadata.  In python shell:
# -i model.py  >  create_engine  >  Base.metadata.create

##  STEP 2 = Perform seeding.
ENGINE = None 
Session = None
# function connect() at bottom...before main.
## in python shell:  -i model.py > s=connect() >  

##  STEP 3 = setup threading.
##  remove step2 code.   import on line 5.  Insert below.
# ENGINE = create_engine("sqlite:///generators.db", echo=True)
# session = scoped_session(sessionmaker(bind=ENGINE, autocommit=False, autoflush=False))
# Base.query = session.query_property()

######################################################################


##  This table is based on the most recent generator data (Nov 2014), and therefore has the most complete dataset.  Have this be the central database, because it lists ALL GENERATORS.
# Static data from the EIA923 csv files. Generator production.
class ProdGen(Base):
	__tablename__ = "ProdGens"
	id = Column(Integer, primary_key=True)
	plant_id = Column(String(15))
	chp = Column(String(5))
	plant_name = Column(String(100))	# plant names are not novel.  cannot be key.
	operator_name = Column(String(100))
	operator_id = Column(String(15))
	state = Column(String(2))
	census_region = Column(String(15))
	nerc_region = Column(String(15))
	naics = Column(String(15))
	sector_eia_id = Column(String(15))
	sector_name = Column(String(15))
	prime_mover = Column(String(15))
	fuel_type = Column(String(15))
	aer_fuel_type = Column(String(15))

	jan_fuel_consumed = Column(Float)
	feb_fuel_consumed = Column(Float)
	mar_fuel_consumed = Column(Float)
	apr_fuel_consumed = Column(Float)
	may_fuel_consumed = Column(Float)
	jun_fuel_consumed = Column(Float)
	jul_fuel_consumed = Column(Float)
	aug_fuel_consumed = Column(Float)
	sep_fuel_consumed = Column(Float)
	oct_fuel_consumed = Column(Float)
	nov_fuel_consumed = Column(Float)
	dec_fuel_consumed = Column(Float)

	jan_mwh_gen = Column(Float)
	feb_mwh_gen = Column(Float)
	mar_mwh_gen = Column(Float)
	apr_mwh_gen = Column(Float)
	may_mwh_gen = Column(Float)
	jun_mwh_gen = Column(Float)
	jul_mwh_gen = Column(Float)
	aug_mwh_gen = Column(Float)
	sep_mwh_gen = Column(Float)
	oct_mwh_gen = Column(Float)
	nov_mwh_gen = Column(Float)
	dec_mwh_gen = Column(Float)




# Static data from the EIA860 csv file. Generator location.
# TODO: FIND LOCATION FOR 10 GENERATORS IN 923, MISSING FROM 860.
class StatsGen(Base):
	__tablename__ = "StatsGens"
	id = Column(Integer, primary_key=True)
	utility_id = Column(String(15))
	utility_name = Column(String(50))
	plant_name = Column(String(100))	# plant names are not novel.  cannot be key.
	state = Column(String(15))
	county = Column(String(30))
	status = Column(String(15))
	nameplate_MW = Column(Float)
	summer_MW = Column(Float)
	winter_MW = Column(Float)
	start_mo = Column(DateTime)
	fuel_1 = Column(String(10))
	fuel_2 = Column(String(10))
	fuel_3 = Column(String(10))
	fuel_4 = Column(String(10))
	fuel_5 = Column(String(10))
	fuel_6 = Column(String(10))
	multi_fuel = Column(String(1))
	interconnected = Column(String(1))
	synchronized = Column(String(1))


######################################################################

def connect():
	global ENGINE
	global Session
	ENGINE = create_engine("sqlite:///generators.db", echo=True)
	Session = sessionmaker(bind=ENGINE)
	return Session()

def main():
	"""For future use."""
	pass

if __name__ == "__main__":
	main()