# This will be the main file where the setup will be accessed and all of the data 
# Will be inputed to the database
# The visualization may also happen here.
from queries import QueryData
from sqlalchemy.sql.expression import except_all
from setup import Setup
from tables import GradeLevel, Students, Section, GradeLevel, Cashier
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly import offline
import plotly

import visualizer
engine = create_engine(
					'postgresql+psycopg2://nia:09092004ni@localhost:5432/studentdatabase', 
					pool_size = 20, 
					max_overflow=0
					)
try:
	setup = Setup(engine)
	setup.__setup__()
except:
	queries = QueryData(engine)
	print(queries.students_avg_grade(Students.age))
	print(queries.students_avg_grade(Students.grade))
	print(queries.students_avg_grade(Students.section_name))
	print(queries.get_table_columns(Section,Section.section_name, Section.number_of_students))

	print(queries.get_table_columns(GradeLevel,GradeLevel.grade_level, GradeLevel.student_total))
	print(queries.count_students(Students, Students.gender))
	print(queries.count_students(Cashier, Cashier.paid))
	print(queries.count_students(Students, Students.age))
	print(queries.get_avg(Students, Students.grade, Students.age))
	print(queries.count_starting_letters())

	section_names = {}								
	for name in queries.get_table_columns(Section, Section.section_name, Section.number_of_students).keys():
		section_names[name]= queries.extended_grade_avg(Students.section_name, name)
	
	grade_lvl = {}
	for num in queries.get_table_columns(GradeLevel,GradeLevel.grade_level, GradeLevel.student_total).keys():
		grade_lvl[num] = queries.extended_grade_avg(Students.grade, num)

	print('\n Section_name:', section_names)
	

	print('\n GradeLevel:', grade_lvl)

	print("\n\n\n--------------------------------------------\n\n\n")
	
	for x, y in zip(grade_lvl.keys(), grade_lvl.values()):

		for w, z in zip(y.keys(), y.values()):
			print("{}: {}".format(w, z))

visualizer.subplot("Grade Level", grade_lvl)
"""
	updatemenus = list([
    dict(active=-1,
         buttons=list([   
            dict(label = 'Average Grades of Students According to their Grade Level',
                 method = 'update',
                 args = [{'visible': [True, False]},
                         {'title': 'Grade Level'}]),
		
            dict(label = '"Average Grades of Students According to their Sections"',
                 method = 'update',
                 args = [{'visible': [False, True]},
                         {'title': 'Sections'}])]))])

	layout = dict(title='graph', showlegend=False,
              updatemenus=updatemenus)

	fig = dict(data=data, layout=layout)

	plotly.offline.plot(fig, auto_open=False, show_link=False)
	"""