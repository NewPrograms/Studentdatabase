import create
import tables
from sqlalchemy import DDL


class Setup():
	def __init__(self):
		self.conduct = tables.Conduct()
		self.grades = tables.Grades()

	def __setup__(self):

		# This is for the creating the triggers
		create.create_func(self.grades, DDL(
				"CREATE FUNCTION get_mapeh() RETURNS TRIGGER AS $$"
				"BEGIN"
				"""
					NEW.MAPEH= NEW.MUSIC + NEW.ARTS + NEW.PE + NEW.HEALTH;
				"""
				"NEW.MAPEH = NEW.MAPEH/4;"
				"RETURN NEW;"
				"END; $$ LANGUAGE 'plpgsql'"

	  			))
		create.create_trigger(self.grades, DDL(
			"CREATE TRIGGER mapeh BEFORE INSERT ON grades"
			"FOR EACH ROW EXECUTE PROCEDURE get_mapeh();"
		))
		# total trigger
		create.create_func(self.grades, DDL(
				"CREATE FUNCTION get_total() RETURNS TRIGGER AS $$"
				"BEGIN"
				"""
					NEW.TOTAL = NEW.MATH + NEW.SCIENCE + NEW.ENGLISH + NEW.AP + NEW.TLE + NEW.MAPEH + NEW.FLIPINO;
					"""
				"NEW.TOTAL = NEW.TOTAL/7;"
				"RETURN NEW;"
				"END; $$ LANGUAGE 'plpgsql'"

				))
		create.create_trigger(self.grades, DDL(
			"CREATE TRIGGER total BEFORE INSERT ON grades"
			"FOR EACH ROW EXECUTE PROCEDURE get_total();"
		))


		# trigger for conduct
		create.create_func(self.conduct, DDL(
			"CREATE OR REPLACE FUNCTION conduct_total() RETURNS TRIGGER AS $$"
			"BEGIN"
			"NEW.TOTAL = NEW.FAITH + NEW.INTEGRITY + NEW.ENTERPRISE + NEW.SERVICE + NEW.COLLABORATION;"
			"NEW.TOTAL = NEW.TOTAL/5"
			"RETURN NEW;"
			"END;"
			"LANGUAGE; $$ LANGUAGE 'plpgsql';"
	))
		create.create_trigger(self.conduct, DDL(
			"CREATE TRIGGER total_conduct BEFORE INSERT ON CONDUCT"
			"FOR EACH ROW EXECUTE PROCEDURE conduct_total()"
		))

 
create.createdb(engine, 'studentdatabase')
tables.base.metadata.create_all(tables.engine)