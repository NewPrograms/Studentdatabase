from sqlalchemy import create_engine, Table, Column, MetaData
from sqlalchemy.orm import declarative_base, relation,relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.types import Integer, String
engine = create_engine('postgresql+psycopg2://nia:09092004ni@localhost:5432/studentdatabase')
base = declarative_base()

class Subject_teaching(base):
	__tablename__ 	= 'subject_teaching'

	name = Column(String, primary_key=True, nullable=False)
	
	teacher = relationship(
				'Teachers',
			 	back_populates='subject_teaching', uselist = False
				 )
class Gender(base):
	__tablename__ = 'gender'

	name = Column(String, primary_key=True, nullable=False)
	teacher = relationship('Teachers', back_populates='gender', uselist=False)
	student = relationship('Students', back_populates='gender_name', uselist=False)
class Teachers(base):
	__tablename__ = 'teachers'

	teacher_id = Column(String, primary_key = True, nullable = False)
	first_name = Column(String, nullable = False)
	middle_name = Column(String, nullable = False)
	last_name = Column(String, nullable = False)
	age = Column(Integer, nullable = False)
	subject = Column(String, ForeignKey('subject_teaching.name'))
	gender_name = Column(String, ForeignKey('gender.name'))
	address = Column(String, nullable=False)
	# This is the relationships
	subject_teaching = relationship('Subject_teaching', back_populates= 'teacher')
	gender = relationship('Gender', back_populates='teacher')
	grade_level = relationship('GradeLevel', back_populates='teacher', uselist=False)		
	section = relationship('Section', back_populates='adviser', uselist=False)	
class GradeLevel(base):
	__tablename__ = 'grade_level'

	grade_level = Column(Integer, primary_key=True)
	head =  Column(String, ForeignKey('teachers.teacher_id'))

	teacher =  relationship('Teachers', back_populates= 'grade_level')
	sections = relationship('Section', back_populates='grade_level')
	students = relationship('Students', back_populates='grade_level', uselist=False)
	cashier = relationship('Cashier', back_populates='grade_level', uselist= False)
class Section(base):
	__tablename__ = 'sections'

	section_name = Column(String, primary_key=True)
	number_of_students = Column(Integer, nullable=False)
	class_adviser = Column(String, ForeignKey('teachers.teacher_id'), nullable=False)
	grade = Column(Integer, ForeignKey('grade_level.grade_level'), nullable = False)

	adviser =  relationship('Teachers', back_populates= 'section')
	grade_level = relationship('GradeLevel', back_populates='sections')
	students = relationship('Students', back_populates='section')
	cashier = relationship('Cashier', back_populates='section' )

class Students(base):
	__tablename__ = 'students'

	student_id = Column(String, primary_key = True, nullable = False)
	first_name = Column(String, nullable = False)
	middle_initial = Column(String, nullable = False)
	last_name = Column(String, nullable = False)
	age = Column(Integer, nullable = False)
	address = Column(String, nullable = False)
	grade = Column(Integer,ForeignKey('grade_level.grade_level'), nullable = False)
	gender = Column(String, ForeignKey('gender.name'))
	section_name  = Column(String, ForeignKey('sections.section_name'))

	# This is the relationships
	grade_level = relationship('GradeLevel', back_populates='students')
	section = relationship('Section', back_populates = 'students')
	gender_name =  relationship('Gender', back_populates= 'student')
	grades = relationship('Grades', back_populates='student', uselist=False)
	conduct = relationship('Conduct', back_populates='student', uselist=False)
	cashier = relationship('Cashier', back_populates='student', uselist=False)
class Grades(base):
	__tablename__ = 'grades'
#make all grade values integer
	student_id = Column(String,ForeignKey('students.student_id'), primary_key = True, nullable = False)
	english = Column(Integer, nullable=False)
	math = Column(Integer, nullable=False)
	filipino = Column(Integer, nullable=False)
	science = Column(Integer, nullable=False)
	ap= Column(Integer, nullable=False)
	tle = Column(Integer, nullable=False)
	mapeh = Column(Integer, nullable=False)
	music = Column(Integer, nullable=False)
	arts = Column(Integer, nullable=False)
	pe = Column(Integer, nullable=False)
	health= Column(Integer, nullable=False)
	total = Column(Integer, nullable=False)

	student =  relationship('Students', back_populates= 'grades')



class Conduct(base):
	__tablename__ = 'conduct'

	student_id = Column(String,ForeignKey('students.student_id'),primary_key=True, nullable = False)
	faith = Column(String, nullable = False)
	integrity = Column(String, nullable = False)
	collaboration = Column(String, nullable = False)
	enterprise = Column(String, nullable = False)
	service = Column(String, nullable = False)

	student =  relationship('Students', back_populates= 'conduct')

class Cashier(base):
	__tablename__ = 'cashier'

	student_id = Column(String, ForeignKey('students.student_id'), primary_key=True)
	grade=Column(Integer, ForeignKey('grade_level.grade_level'))
	section_name  = Column(String, ForeignKey('sections.section_name'))
	paid = Column(String, nullable=False)	

	grade_level = relationship('GradeLevel', back_populates='cashier')
	section = relationship('Section', back_populates = 'cashier')
	student = relationship('Students', back_populates='cashier')
