import csv
import datetime
import json

from peewee import *

DATABASE = SqliteDatabase('debates.db')


class Debates(Model):
	file_name = CharField(unique=True)
	debate_name = CharField(null=False)
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
					cls.create(file_name=row['File'],debate_name=row['File'].split('.')[0],order=row['Order'],party=row['Party'],friendly_name=row['Friendly Name'],city=row['City'],state=row['State'],location=row['Location'],debate_date=row['Date'])
				except IntegrityError:
					raise ValueError("Debate exists {}".format(row['File'].split('.')[1]))


class Speaker(Model):
	name = CharField(null=False)
	debate = ForeignKeyField(Debates, related_name='debate_speaker')

	class Meta:
		database = DATABASE
		order_by = ('debate','name',)

	@classmethod
	def create_speaker(cls, name, file_name):
		try:
			debate_id = Debates.get(Debates.file_name == file_name).id
			with DATABASE.transaction():
				cls.create(name=name, debate=debate_id)
		except IntegrityError:
			raise ValueError("Speaker exists")


class SpeakerText(Model):
	speaker_text = CharField(null=False)
	order = IntegerField(null=False)
	speaker = ForeignKeyField(Speaker, related_name='speaker_speaker_text')
	debate = ForeignKeyField(Debates, related_name='debate_speaker_text')

	class Meta:
		database = DATABASE
		order_by = ('debate','speaker','order',)

	@classmethod
	def create_speaker_text(cls, speaker_text, order, speaker_name, file_name):
		try:
			with DATABASE.transaction():
				debate_id = Debates.get(Debates.file_name == file_name).id
				speaker_id = Speaker.get(Speaker.name == speaker_name, Speaker.debate == debate_id).id
				cls.create(speaker_text=speaker_text, order=order, speaker=speaker_id, debate=debate_id)
		except IntegrityError:
			raise ValueError("speaker text already exists")
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
	DATABASE.create_tables([Debates, Speaker, SpeakerText], safe=True)
	DATABASE.close()
