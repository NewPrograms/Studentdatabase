# This will be the main file where the setup will be accessed and all of the data 
# Will be inputed to the database
# The visualization may also happen here.
from setup import Setup
from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg2://nia:09092004ni@localhost:5432/studentdatabase')
setup = Setup(engine)
setup.__setup__()