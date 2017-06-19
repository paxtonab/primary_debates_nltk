import csv
import datetime
import json

from peewee import *

DATABASE = SqliteDatabase('debates.db')


class Debates(Model):
	file_name = CharField(unique=True)
	order = IntegerField(null=False)
	party = CharField(null=False)
	friendly_name=CharField(null=True)
	city = CharField(null=False)
	state = CharField(null=False)
	location = CharField(null=False)
	debate_date = DateTimeField(null=False)

	class Meta:
		database = DATABASE
		order_by = ('party','order',)

	@classmethod
	def initialize_debates(cls):
		with DATABASE.transaction():
			debate_file = open('debates.csv', 'r')
			fieldnames = ("Party","Order","File","Friendly Name","City","State","Location","Date")
			reader = csv.DictReader(debate_file, fieldnames)
			next(reader)
			for row in reader:
				try:
					cls.create(file_name=row['File'],order=row['Order'],party=row['Party'],friendly_name=row['Friendly Name'],city=row['City'],state=row['State'],location=row['Location'],debate_date=row['Date'])
					#cls.create(file_name=debate_json['File'],order=debate_json['Order'],party=debate_json['Party'],friendly_name=debate_json['Friendly Name'],city=debate_json['City'],state=debate_json['State'],location=debate_json['Location'],debate_date=debate_json['Date'])
				except IntegrityError:
					raise ValueError("Workout exists.")


# class Speaker(Model):
# 	name = CharField(null=False)
# 	party = CharField(null=False)
# 	title = CharField(null=False)
#
# 	class Meta:
# 		database = DATABASE
# 		order_by = ('party','name',)
#
# 	@classmethod
# 	def create_workout(cls, set_1):
# 		try:
# 			with DATABASE.transaction():
# 				cls.create(set_1=set_1)
# 		except IntegrityError:
# 			raise ValueError("Workout exists.")
#
#
# class ParsedText(Model):
# 	speaker = CharField(null=False)
# 	spoken = CharField(null=False)
# 	order = CharField(null=False)
# 	debate = CharField(null=False)
#
# 	class Meta:
# 		database = DATABASE
# 		order_by = ('speaker','order',)
#
# 	@classmethod
# 	def create_workout(cls, set_1):
# 		try:
# 			with DATABASE.transaction():
# 				cls.create(set_1=set_1)
# 		except IntegrityError:
# 			raise ValueError("Workout exists.")
#
#
#
# class ParsedText(Model):
# 	name = CharField()
# 	description = CharField(null=True)
# 	created = DateTimeField(default=datetime.datetime.now)
#
# 	class Meta:
# 		database = DATABASE
# 		order_by = ('name',)
#
# 	@classmethod
# 	def create_exercise(cls, name, description=None):
# 		try:
# 			with DATABASE.transaction():
# 				cls.create(
# 					name=name,
# 					description=description,
# 				)
# 		except IntegrityError:
# 			raise ValueError("Exercise exists.")
#
#
# class Relationship(Model):
# 	user_id = ForeignKeyField(User, related_name='user_id')
# 	workout_id = ForeignKeyField(Workout, related_name ='workout_id')
# 	created = DateTimeField(default=datetime.datetime.now)
#
# 	class Meta:
# 		database = DATABASE
# 		indexes = (
# 			(('user_id', 'workout_id'), True),
# 		)
#
#
# class Tracked(Model):
# 	relationship_id = CharField(null=True)#ForeignKeyField(Relationship, related_name='relationship_id')
# 	exercise_id = CharField(null=True)#ForeignKeyField(Exercise, related_name='exercise_id')
# 	created = DateTimeField(default=datetime.datetime.now)
# 	rounds = IntegerField(null=True)
# 	weight = IntegerField(null=True)
# 	week = IntegerField(null=True)
#
# 	class Meta:
# 		database = DATABASE
#
# 	@classmethod
# 	def create_tracked(cls, relationship_id, exercise):
# 		try:
# 			exercise_lookup = Exercise.get(Exercise.name**exercise)
# 		except DoesNotExist:
# 			pass
# 		else:
# 			Tracked.create(
# 				relationship_id = relationship_id,
# 				exercise_id = exercise_lookup.id
# 			)


def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Debates], safe=True)
	DATABASE.close()
