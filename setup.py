from sqlalchemy.sql.schema import MetaData
import create
import tables
from sqlalchemy import DDL
from insert import Insert
metadata = MetaData()
class Setup():
	def __init__(self, engine):
		self.engine = engine
		self.conduct = tables.Conduct()
		self.grades = tables.Grades()
		self.students = tables.Students()
		self.sections = tables.Section()
		self.insert = Insert(self.engine)
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
					NEW.TOTAL = NEW.MATH + NEW.SCIENCE + NEW.ENGLISH + NEW.AP + NEW.TLE + NEW.MAPEH + NEW.FILIPINO;
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
		create.create_func(self.engine, self.sections.__table__, DDL(
			"""
			CREATE OR REPLACE FUNCTION random_between(low INT ,high INT) 
			RETURNS INT AS
			$$
			BEGIN
			RETURN floor(random()* (high-low + 1) + low);
			END;
			$$ language 'plpgsql' STRICT;
			"""
		))

		create.create_func(self.engine, self.sections.__table__, DDL(
			"""
				CREATE OR REPLACE FUNCTION random_words(section_names varchar(50) array) RETURNS VARCHAR AS $$
				BEGIN
				RETURN section_names[random_between(1,ARRAY_LENGTH(section_names, 1))];
				END;
				$$
				LANGUAGE 'plpgsql';
			"""
		))

		create.create_func(self.engine, self.sections.__table__, DDL(
			"""
				CREATE OR REPLACE FUNCTION get_sections() RETURNS TRIGGER AS $$
				BEGIN
				IF NEW.GRADE = 10 THEN
					NEW.section_name = random_words(ARRAY['Aether', 'Uranium', 'Infinity']);
				ELSIF NEW.GRADE = 9 THEN
					NEW.section_name = random_words(ARRAY['Tony', 'Loki', 'Ragnarok']);
				ELSIF NEW.GRADE = 8 THEN
					NEW.section_name = random_words(ARRAY['Faith', 'Lead', 'Integrity']);
				ELSE NEW.section_name = random_words(ARRAY['Socrates', 'Plato', 'Aristotle']);
				END IF;
				RETURN NEW;
				END;
				$$
				LANGUAGE 'plpgsql';
			"""

		))

		create.create_trigger(self.engine, self.students.__table__, DDL(
			"""
			CREATE TRIGGER add_section BEFORE INSERT ON STUDENTS
			FOR EACH ROW EXECUTE PROCEDURE get_sections();
			"""
		))

		create.create_func(self.engine, self.sections.__table__, DDL(
			"""
				CREATE FUNCTION number_students() RETURNS TRIGGER AS $$
				DECLARE
				number_of_students record;
				BEGIN
				SELECT COUNT(student_id) into number_of_students FROM STUDENTS WHERE section_name = NEW.section_name;
				NEW.number_of_students :=  CAST(TRANSLATE(CAST(number_of_students AS TEXT), '()', '') AS INTEGER);
				RETURN NEW;
				END;
				$$
				LANGUAGE 'plpgsql';
			"""
		))
		create.create_func(self.engine, self.sections.__table__, DDL(
			"""
				CREATE FUNCTION students_number_students() RETURNS TRIGGER AS $$
				DECLARE
				student_number record;
				BEGIN
				UPDATE sections SET number_of_students = (SELECT COUNT(student_id) FROM  STUDENTS WHERE section_name = NEW.SECTION_NAME)
				WHERE section_name = NEW.SECTION_NAME;
				RETURN NEW;
				END;
				$$
				LANGUAGE 'plpgsql';
			"""
		))

		create.create_trigger(self.engine, self.sections.__table__, DDL(
			"""
				CREATE TRIGGER get_studentnumbers BEFORE INSERT OR UPDATE ON SECTIONS
				FOR EACH ROW EXECUTE PROCEDURE number_students();
			"""
		))
		create.create_trigger(self.engine, self.sections.__table__, DDL(
			"""
				CREATE TRIGGER get_studentnumbers_students BEFORE INSERT OR UPDATE ON STUDENTS 
				FOR EACH ROW EXECUTE PROCEDURE students_number_students();
			"""
		))
		
		create.create_trigger(self.engine, self.conduct.__table__, DDL(
			"""
				CREATE OR REPLACE FUNCTION get_conduct_total() RETURNS TRIGGER AS $$
				BEGIN
				NEW.TOTAL = NEW.FAITH + NEW.INTEGRITY + NEW.COLLABORATION + NEW.ENTERPRISE + NEW.SERVICE;
				NEW.TOTAL = NEW.TOTAL::integer /5;
				RETURN NEW;
				END;
				$$ LANGUAGE 'plpgsql';
			"""
		))

		create.create_func(self.engine, self.conduct.__table__, DDL(

			"""
				CREATE TRIGGER get_conduct_total BEFORE INSERT OR UPDATE ON CONDUCT
				FOR EACH ROW EXECUTE PROCEDURE get_conduct_total();
			"""
		))
		create.create_trigger(self.engine, self.conduct.__table__, DDL(
			"""
				CREATE OR REPLACE FUNCTION change_total() RETURNS TRIGGER AS $$
				BEGIN
				IF NEW.TOTAL::integer >= 97 THEN 
				NEW.TOTAL = 'A+';
				ELSIF NEW.TOTAL::integer >= 95 THEN
				NEW.TOTAL = 'A';
				ELSIF NEW.TOTAL::integer >= 90 THEN
				NEW.TOTAL = 'A-';
				ELSIF NEW.TOTAL::integer >= 85 THEN 
				NEW.TOTAL = 'B+';
				ELSIF NEW.TOTAL::integer >= 80 THEN
				NEW.TOTAL = 'B';
				ELSIF NEW.TOTAL::integer >= 75 THEN
				NEW.TOTAL = 'B-';
				ELSIF NEW.TOTAL::integer >= 70 THEN 
				NEW.TOTAL = 'C+';
				ELSIF NEW.TOTAL::integer >= 65 THEN 
				NEW.TOTAL = 'C';
				ELSIF NEW.TOTAL::integer >= 60 THEN
				NEW.TOTAL = 'C-';
				ELSE NEW.TOTAL = 'F';
				END IF;
				RETURN NEW;
				END;
				$$ LANGUAGE 'plpgsql';
		"""
		))
		create.create_func(self.engine, self.conduct.__table__, DDL(
			"""
				CREATE TRIGGER change_conduct_total AFTER INSERT OR UPDATE ON CONDUCT
				 FOR EACH ROW EXECUTE PROCEDURE change_total();
			"""
		))


		table_paths = [
					'/mnt/c/Users/Ryan Arcillas/Documents/Scripts/Projects/StudentDatabase/sql_data/teaching.sql',
					'/mnt/c/Users/Ryan Arcillas/Documents/Scripts/Projects/StudentDatabase/sql_data/gender.sql',
					'/mnt/c/Users/Ryan Arcillas/Documents/Scripts/Projects/StudentDatabase/sql_data/teachers.sql',
					'/mnt/c/Users/Ryan Arcillas/Documents/Scripts/Projects/StudentDatabase/sql_data/grade_level.sql',
					'/mnt/c/Users/Ryan Arcillas/Documents/Scripts/Projects/StudentDatabase/sql_data/sections.sql',
					'/mnt/c/Users/Ryan Arcillas/Documents/Scripts/Projects/StudentDatabase/sql_data/students.sql',
					'/mnt/c/Users/Ryan Arcillas/Documents/Scripts/Projects/StudentDatabase/sql_data/grades.sql',
					'/mnt/c/Users/Ryan Arcillas/Documents/Scripts/Projects/StudentDatabase/sql_data/conduct.sql'
		]
		for table_path in table_paths:
			self.insert.read_file(table_path)