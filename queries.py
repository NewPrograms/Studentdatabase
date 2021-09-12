from sqlalchemy.sql.expression import label, union_all
from sqlalchemy.sql.selectable import subquery
from tables import Grades, Section, GradeLevel, Students
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, column
class QueryData:

	def __init__(self, engine):
		self.engine = engine
		Session = sessionmaker(bind=engine)
		self.session = Session()
	def students_avg_grade(self,tb_column):
		# The instance method only accepts arguments that are instances
		# of the StudentClass.
		avg_grades = {}
		for instance in (self.session.query(tb_column.label('key'), 
						func.avg(Grades.total).label('avg_grade'))
						.select_from(Students, Grades)
						.filter(Grades.student_id == Students.student_id)
						.group_by(tb_column)
						):
			# remove DECIMAL and remove the brackets
			avg_grades[instance.key] = float(instance.avg_grade)
		return avg_grades

	def count_students(self, table, tb_column):
		total = {}
		for instance in (self.session.query(tb_column.label('key'), 
						func.count(table.student_id).label('total_count'))
						.select_from(table)
						.group_by(tb_column)
						):
			# remove DECIMAL and remove the brackets
			total[instance.key] = instance.total_count
		return total

	def get_table_columns(self, table, tb_col_name, tb_column):
		total_num = {}
		for instance in (self.session.query(tb_col_name.label('key'), tb_column.label('value'))
						.select_from(table)):
			total_num[instance.key] = int(instance.value)
		return total_num


	def get_avg(self, table, tb_column, tb_column2 ):
		total = {}
		for instance in (self.session.query(tb_column.label('key'), 
						func.avg(tb_column2).label('total_count'))
						.select_from(table)
						.group_by(tb_column)
						):
			# remove DECIMAL and remove the brackets
			total[instance.key] = float(instance.total_count)
		return total
	
	def count_starting_letters(self):
		total = {}
		single_letter = (self.session.query(
					func.chr(func.generate_series(65, 65)).label('letter')
					).subquery())
			
		letters = (self.session.query(Students.student_id.label('student_id'),
					func.chr(func.generate_series(66, 90)).label('letter')
					).select_from(Students).subquery())
		non_recur_series = (
							self.session.query(single_letter.c.letter.label('letter')
							, func.count(Students.student_id).label('count'))
							.select_from(single_letter, Students).filter(
								Students.first_name.like('%' + single_letter.c.letter + '%')
								).group_by(single_letter.c.letter)
							)
		recur_series = (
						self.session.query(letters.c.letter.label('letter'), 
						func.count(Students.student_id).label('count'))
						.select_from(Students).join(letters, Students.student_id == letters.c.student_id)
						.filter(Students.first_name.like('%' + letters.c.letter + '%')
						).group_by(letters.c.letter))
		cte = union_all(non_recur_series, recur_series).cte(recursive=True)
		for instance in self.session.query(cte):
			total[instance.letter] = instance.count
		
		return total

	def extended_grade_avg(self,section_name, name):
		queried = {}
		subquery = (self.session.query(Students.student_id).select_from(Students)
					.filter(section_name == name)).subquery()
		queries = (self.session.query(
					func.avg(Grades.math).label('math'),
					 func.avg(Grades.science).label('science'), 
					func.avg(Grades.english).label('english'), 
					func.avg(Grades.filipino).label('filipino'), 
					func.avg(Grades.tle).label('tle'), 
					func.avg(Grades.ap).label('tle'),
					func.avg(Grades.music).label('music'),
					 func.avg(Grades.arts).label('arts'),
					func.avg(Grades.pe).label('pe'), 
					func.avg(Grades.health).label('health')
					).select_from(Grades, subquery)
					.filter(Grades.student_id == subquery.c.student_id))
		for instance in queries:
			for x, y in zip(instance.keys(), instance): 
				queried[x] = y
		
		return queried
