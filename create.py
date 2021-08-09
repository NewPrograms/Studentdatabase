# This is the class to be used for the settings.

# class for setting up the database
from sqlalchemy import event
from sqlalchemy.engine import create_engine
def createdb(engine, database_name):
	conn = engine.connect()
	conn.execute("commit")
	conn.execute("CREATE DATABASE {}".format(database_name))
	conn.close()


def create_func(table, func ):
	event.listen(table, 'after_create',func.execute_if(dialect='postgresql'))

def create_trigger(table, trigger):
	event.listen(table, 'after_craete', trigger.execute_if(dialect = 'postgresql'))