# This is the class to be used for the settings.

# class for setting up the database
from sqlalchemy import event
from sqlalchemy.engine import create_engine

def createdb(engine, database_name):
	conn = engine.connect()
	conn.execute("commit")
	conn.execute("CREATE DATABASE {}".format(database_name))
	conn.close()

def create_ddl(engine, table, ddl):
	event.listen(table, 'after_create', ddl.execute(engine))