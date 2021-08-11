from sqlalchemy.sql.schema import MetaData
import create
import tables
from sqlalchemy import DDL
from sqlalchemy import create_engine
metadata = MetaData()
class Setup():
	def __init__(self, engine):
		self.engine = engine
		self.conduct = tables.Conduct()
		self.grades = tables.Grades()

	def __setup__(self):
		# This is for the creating the triggers		
		tables.base.metadata.create_all(self.engine)
		create.create_func(self.engine, self.conduct.__table__, DDL(
			"""
				CREATE OR REPLACE FUNCTION get_mapeh() RETURNS TRIGGER AS $$
				BEGIN
					NEW.MAPEH= NEW.MUSIC + NEW.ARTS + NEW.PE + NEW.HEALTH;
					NEW.MAPEH = NEW.MAPEH/4;
					RETURN NEW;
				END;
				$$ LANGUAGE 'plpgsql' ;
			"""
				

	  			))
		create.create_trigger(self.engine, self.grades.__table__, DDL(
			"""
				CREATE TRIGGER mapeh BEFORE INSERT ON grades
				FOR EACH ROW EXECUTE PROCEDURE get_mapeh();
		
			"""
		))
		# total trigger
		create.create_func(self.engine, self.grades.__table__, DDL(
			"""
				CREATE OR REPLACE FUNCTION get_total() RETURNS TRIGGER AS $$
				BEGIN
					NEW.TOTAL = NEW.MATH + NEW.SCIENCE + NEW.ENGLISH + NEW.AP + NEW.TLE + NEW.MAPEH + NEW.FLIPINO;
					NEW.TOTAL = NEW.TOTAL/7;
					RETURN NEW;
					END; 
				$$ LANGUAGE 'plpgsql';
			"""

				))
		create.create_trigger(self.engine, self.grades.__table__, DDL(
			"""
				CREATE TRIGGER total BEFORE INSERT ON grades
				FOR EACH ROW EXECUTE PROCEDURE get_total();
			"""
		))


		# trigger for conduct
		create.create_func(self.engine, self.conduct.__table__, DDL(
			"""
				CREATE OR REPLACE FUNCTION conduct_total() RETURNS TRIGGER AS $$
				BEGIN
					NEW.TOTAL = NEW.FAITH + NEW.INTEGRITY + NEW.ENTERPRISE + NEW.SERVICE + NEW.COLLABORATION;
					NEW.TOTAL = NEW.TOTAL/5;
					RETURN NEW;
					END;
				$$ LANGUAGE 'plpgsql';
			"""
	))
		create.create_trigger(self.engine, self.conduct.__table__, DDL(
			"""
				CREATE TRIGGER total_conduct BEFORE INSERT ON CONDUCT
				FOR EACH ROW EXECUTE PROCEDURE conduct_total();
			"""
		))

