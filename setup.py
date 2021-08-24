from sqlalchemy.sql.schema import MetaData
import create
import tables
from sqlalchemy import DDL
from insert import Insert
metadata = MetaData()
func_statements = {
		'calculateMapeh()': 
			"""
				 RETURNS TRIGGER AS $$
				BEGIN
					NEW.MAPEH= NEW.MUSIC + NEW.ARTS + NEW.PE + NEW.HEALTH;
					NEW.MAPEH = NEW.MAPEH/4;
					RETURN NEW;
				END;
				$$ LANGUAGE 'plpgsql' ;
			""",
		'calculateTotal()':
			"""
				RETURNS TRIGGER AS $$
				BEGIN
					NEW.TOTAL = NEW.MATH + NEW.SCIENCE + NEW.ENGLISH + NEW.AP + NEW.TLE + NEW.MAPEH + NEW.FILIPINO;
					NEW.TOTAL = NEW.TOTAL/7;
					RETURN NEW;
					END; 
				$$ LANGUAGE 'plpgsql';
			""",
		'getRandomNumber(low INT ,high INT)':"""
			RETURNS INT AS
			$$
			BEGIN
			RETURN floor(random()* (high-low + 1) + low);
			END;
			$$ language 'plpgsql' STRICT;
		""",
		'getRandomWords(sectionNames varchar(50) array)':"""
			RETURNS VARCHAR AS $$
			BEGIN
			RETURN sectionNames[getRandomNumber(1,ARRAY_LENGTH(sectionNames, 1))];
			END;
			$$
			LANGUAGE 'plpgsql';
		""",
		'getSections()':
			"""
				RETURNS TRIGGER AS $$
				BEGIN
				IF NEW.GRADE = 10 THEN
					NEW.section_name = getRandomWords(ARRAY['Aether', 'Uranium', 'Infinity']);
				ELSIF NEW.GRADE = 9 THEN
					NEW.section_name = getRandomWords(ARRAY['Tony', 'Loki', 'Ragnarok']);
				ELSIF NEW.GRADE = 8 THEN
					NEW.section_name = getRandomWords(ARRAY['Faith', 'Lead', 'Integrity']);
				ELSE NEW.section_name = getRandomWords(ARRAY['Socrates', 'Plato', 'Aristotle']);
				END IF;
				RETURN NEW;
				END;
				$$
				LANGUAGE 'plpgsql';
			""",
		'CountStudents()':
			"""
				RETURNS TRIGGER AS $$

				BEGIN
				UPDATE sections SET number_of_students = (SELECT COUNT(student_id) FROM  STUDENTS WHERE section_name = NEW.SECTION_NAME)
				WHERE section_name = NEW.SECTION_NAME;
				RETURN NEW;
				END;
				$$
				LANGUAGE 'plpgsql';
			""",

			"""CalculateConductTotal(
					faith integer, service integer,
					enterprise integer, collaboration integer,
					integrity integer )""":
					"""
						RETURNS INTEGER AS $$
						DECLARE 
						total integer;
						BEGIN
						TOTAL = FAITH + INTEGRITY + COLLABORATION + ENTERPRISE + SERVICE;
						TOTAL = TOTAL::integer /5;
						RETURN TOTAL;
						END;
						$$ LANGUAGE 'plpgsql';
					""",
			'ChangeConductTotal()':
			"""
				RETURNS TRIGGER AS $$
				DECLARE
				total_val integer;
				BEGIN
				total_val = CalculateConductTotal(
											CAST(CAST(NEW.FAITH AS VARCHAR) AS INTEGER), 
											CAST(CAST(NEW.INTEGRITY AS VARCHAR) as INTEGER),
											CAST(CAST(NEW.ENTERPRISE AS VARCHAR) AS  INTEGER), 
											CAST(CAST(NEW.SERVICE AS VARCHAR) AS INTEGER),
											CAST(CAST(NEW.COLLABORATION AS VARCHAR) AS INTEGER)
											);
				IF total_val >= 97 THEN 
				NEW.TOTAL = 'A+';
				ELSIF total_val >= 95 THEN
				NEW.TOTAL = 'A';
				ELSIF total_val::integer >= 90 THEN
				NEW.TOTAL = 'A-';
				ELSIF total_val>= 85 THEN 
				NEW.TOTAL = 'B+';
				ELSIF total_val>= 80 THEN
				NEW.TOTAL = 'B';
				ELSIF total_val>= 75 THEN
				NEW.TOTAL = 'B-';
				ELSIF total_val>= 70 THEN 
				NEW.TOTAL = 'C+';
				ELSIF total_val>= 65 THEN 
				NEW.TOTAL = 'C';
				ELSIF total_val>= 60 THEN
				NEW.TOTAL = 'C-';
				ELSE NEW.TOTAL = 'F';
				END IF;
				RETURN NEW;
				END;
				$$ LANGUAGE 'plpgsql';
		""",
		'InsertPaymentStatus()':
			"""
				RETURNS TRIGGER AS $$
				BEGIN
				INSERT INTO CASHIER(STUDENT_ID, grade, section_name, paid)
				VALUES (
						NEW.student_id, 
						NEW.grade, 
						NEW.section_name, 
						getRandomWords(ARRAY['FULLY PAID', 'PARTIALLY PAID', 'NOT PAID'
						]));
				RETURN NEW;
				END;
				$$ LANGUAGE 'plpgsql';
			"""
		
}

triggers_statements = {
			"calcMapeh ": """
					BEFORE INSERT ON grades
					FOR EACH ROW EXECUTE PROCEDURE calculateMapeh();
					""",
			"calcTotal":
				"""
					BEFORE INSERT ON grades
					FOR EACH ROW EXECUTE PROCEDURE calculateTotal();
				""",
			"AddSection":
				"""
					BEFORE INSERT ON STUDENTS
					FOR EACH ROW EXECUTE PROCEDURE getSections();
				""",
			"StudentsCount":
				"""
					BEFORE INSERT OR UPDATE ON STUDENTS 
					FOR EACH ROW EXECUTE PROCEDURE CountStudents(); 
				""",
			"GetChangedTotal":
				"""
					 BEFORE INSERT OR UPDATE ON CONDUCT
					 FOR EACH ROW EXECUTE PROCEDURE ChangeConductTotal();
					
				""",
			"AddPaymentStatus":
				"""
					AFTER INSERT ON students 
					FOR EACH ROW EXECUTE PROCEDURE InsertPaymentStatus();
				"""

}
class Setup():
	def __init__(self, engine):
		self.engine = engine
		self.conduct = tables.Conduct()
		self.grades = tables.Grades()
		self.students = tables.Students()
		self.sections = tables.Section()
		self.cashier = tables.Cashier()
		self.insert = Insert(self.engine)
	def __setup__(self):
		# This is for the creating the triggers		
		tables.base.metadata.create_all(self.engine)
		for key, value in zip(func_statements.keys(), func_statements.values()):
			create.create_ddl(self.engine, self.conduct.__table__, DDL("""
      CREATE OR REPLACE FUNCTION {} {}
					""".format(key, value)
	 	 			))
		for key, value in zip(triggers_statements.keys(), triggers_statements.values()):
			create.create_ddl(self.engine, self.grades.__table__, DDL(
				"""
					CREATE TRIGGER {} {}

				""".format(key, value)
			))
		# total trigger
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
