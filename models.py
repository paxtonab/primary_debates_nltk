import csv
import datetime
import json

from peewee import *

DATABASE = SqliteDatabase('debates.db')


class Debate(Model):
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


	@classmethod
	def get_debates(cls):
		"""
		:ret : file_list list of debate file names
		"""
		try:
			file_list = [debate.file_name for debate in cls.select()]
			return file_list
		except Exception as e:
			return e


class Speaker(Model):
	name = CharField(null=False)
	debate = ForeignKeyField(Debate, related_name='debate_speaker')

	class Meta:
		database = DATABASE
		order_by = ('debate','name',)


	@classmethod
	def create_speaker(cls, name, file_name):
		try:
			debate_id = Debate.get(Debate.file_name == file_name).id
			with DATABASE.transaction():
				cls.create(name=name, debate=debate_id)
		except IntegrityError:
			raise ValueError("Speaker exists")


	@classmethod
	def get_speakers(cls, file_name):
		"""
		:params : file_name name of file to limit speakers by
		:ret : speaker_list list of speaker names
		"""
		try:
			speaker_list = [speaker.name for speaker in cls.select() if speaker.debate.file_name == file_name]
			return speaker_list
		except Exception as e:
			return e


class SpeakerText(Model):
	speaker_text = CharField(null=False)
	order = IntegerField(null=False)
	speaker = ForeignKeyField(Speaker, related_name='speaker_speaker_text')
	debate = ForeignKeyField(Debate, related_name='debate_speaker_text')

	class Meta:
		database = DATABASE
		order_by = ('debate','speaker','order',)


	@classmethod
	def create_speaker_text(cls, speaker_text, order, speaker_name, file_name):
		try:
			with DATABASE.transaction():
				debate_id = Debate.get(Debate.file_name == file_name).id
				speaker_id = Speaker.get(Speaker.name == speaker_name, Speaker.debate == debate_id).id
				cls.create(speaker_text=speaker_text, order=order, speaker=speaker_id, debate=debate_id)
		except IntegrityError:
			raise ValueError("speaker text already exists")


class Candidate(Model):
	"""
	Class to represent candidates vs. moderators
	Need some sort of scrubbing and/or replacement dict
	to map from the speaker class
	"""
	pass


def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Debate, Speaker, SpeakerText], safe=True)
	DATABASE.close()
