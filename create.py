# This is the class to be used for the settings.

# class for setting up the database
from sqlalchemy import event
from sqlalchemy.engine import create_engine

def createdb(engine, database_name):
	conn = engine.connect()
	conn.execute("commit")
	conn.execute("CREATE DATABASE {}".format(database_name))
	conn.close()


def create_func(engine, table, func ):
	event.listen(table, 'after_create',func.execute(engine))

def create_trigger(engine, table, trigger):
	event.listen(table, 'after_create', trigger.execute(engine))