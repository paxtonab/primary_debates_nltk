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
	mapped_name = CharField(null=True)

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
		Get a list of all the speakers in a specific debate text file

		:params : file_name name of file to limit speakers by
		:ret : speaker_list list of speaker names
		"""
		try:
			speaker_list = [speaker.name for speaker in cls.select() if speaker.debate.file_name == file_name]
			return speaker_list
		except Exception as e:
			return e


	@classmethod
	def get_speakers_debates(cls, speaker_name, use_mapped_name=True):
		"""
		Get all the debates a speaker was present in

		:params : speaker_name name of speaker to get debates for
		:params : use_mapped_name bool of whether to query with mapped_name or speaker_name
		:ret : speaker_list list of speaker names
		"""
		try:
			if use_mapped_name:
				debate_list = [speaker.debate.debate_name for speaker in cls.select().where(cls.mapped_name == speaker_name)]
			else:
				debate_list = [speaker.debate.debate_name for speaker in cls.select().where(cls.name == speaker_name)]
			return debate_list
		except Exception as e:
			return e


	@classmethod
	def get_mapped_names(cls):
		"""
		Map all Speaker.name to a friendly version to eliminate typos

		:params : file_name name of file to limit speakers by
		:ret : speaker_list list of speaker names
		"""
		replacement_dict ={
			' LOOK BACK': '',
			' OPEN GRAPHIC': '',
			' OPEN INTERACTIVE GRAPHIC': '',
			' OUR ANALYSIS': '',
			'. COOPER': 'COOPER',
			'ALEXIS': 'ALEXIS KULASH, DRAKE UNIVERSITY STUDENT',
			'ALEXIS KULASH, DRAKE UNIVERSITY STUDENT': '',
			'ANNOUNCER': '',
			'ARNOLD WOODS, PRESIDENT, DES MOINES NAACP': '',
			'ARRARAS': 'ARRASAS',
			'ARRASAS': '',
			'AUDIENCE': '',
			'AUDIENCE MEMBER': '',
			'BAIER': '',
			'BAKER': '',
			'BARITROMO': 'BARTIROMO',
			'BARTIROMO': '',
			'BASH': '',
			'BERNIE SANDERS': 'SANDERS',
			'BISHOP': '',
			'BLITZER': '',
			'BRETT ROSENGREN, STUDENT': 'BRETT ROSENGREN, STUDENT',
			'BROWNLEE': '',
			'BUSH': '',
			'CARSON': '',
			'CAVUTO': '',
			'CELESTE': '',
			'CHAFEE': '',
			'CHRISTIE': '',
			'CLINTON': '',
			'COLLISON': '',
			'COOPER': '',
			'CRAMER': '',
			'CRAWFORD': '',
			'CRUZ': '',
			'CRUZ ': 'CRUZ',
			'CUBA': '',
			'CUOMO': '',
			'CURZ': 'CRUZ',
			'DEBORAH PLUMMER': '',
			'DICK GOODSON, CHAIRMAN, DES MOINES COMMITTEE ON FOREIGN RELATIONS': '',
			'DICKERSON': '',
			'DINAN': '',
			'ELECTION 2016': '',
			'END​': '',
			'EPPERSON': '',
			'FIONNA': 'FIORINA',
			'FIORINA': '',
			'FRANCHESCA RAMSEY': '',
			'FRANTA': '',
			'FROM OUR ADVERTISERS': '',
			'GARRET': '',
			'GARRETT': '',
			'GOODSON': '',
			'GRAPHIC': '',
			'HAM': '',
			'HANNITY': '',
			'HARMAN': '',
			'HARWOOD': '',
			'HEWITT': '',
			'HILLARY CLINTON': 'CLINTON',
			'HOLT': '',
			'HUCKABEE': '',
			'IFILL': '',
			'INTERACTIVE GRAPHIC': '',
			'JENNA BISHOP, DRAKE UNIVERSITY LAW SCHOOL STUDENT': '',
			'JOHN DICKERSON': '',
			'JORGE RAMOS': '',
			'JOSH JACOB, COLLEGE STUDENT': '',
			'JOY LASSEN': '',
			'JUL 13': '',
			'KAISCH': 'KASICH',
			'KARL': '',
			'KASICH': '',
			'KATHIE OBRADOVICH': '',
			'KELLY': '',
			'KEVIN COONEY': '',
			'LASSEN': '',
			'LEMON': '',
			'LEVESQUE': '',
			'LIVE COVERAGE': '',
			'LOPEZ': '',
			'LOUIS': '',
			'MADDOW': '',
			'MAJOR GARRETT': '',
			'MALE': '',
			"MARTIN O'MALLEY": "O'MALLEY",
			'MCELVEEN': '',
			'MEGAN': 'KELLY',
			'MEGYN': 'KELLY',
			'MILLER': '',
			'MITCHELL': '',
			'MODERATOR': '',
			'MORE': '',
			'MUIR': '',
			'NANCY CORDES': '',
			'NEWS ANALYSIS': '',
			'NEWS CLIPS': '',
			"O'CONNOR": '',
			"O'MALLEY": '',
			"O'REILLY": '',
			"O’MALLEY": "O'MALLEY",
			'PAUL': '',
			'PERRY': '',
			'PLUMMER': '',
			'QUESTION': '',
			'QUICK': '',
			'QUINTANILLA': '',
			'RADDATZ': '',
			'RAMOS': '',
			'RELATED COVERAGE': '',
			'RITCHIE': '',
			'ROSENGREN': '',
			'RUBIO': '',
			'SALINAS': '',
			'SANDERFS': 'SANDERS',
			'SANDERS': '',
			'SANTELLI': '',
			'SEAN COLLISON': '',
			'SMITH': '',
			'STEPHANOPOULOS': '',
			'STRASSEL': '',
			'TALKER': '',
			'TAPPER': '',
			'TAPPER ': 'TAPPER',
			'TODD': '',
			'TRUMO': 'TRUMP',
			'TRUMP': '',
			'TUMULTY': '',
			'UNIDENTIFIABLE MALE': '',
			'UNIDENTIFIED FEMALE': '',
			'UNIDENTIFIED MALE': '',
			'WALKER': '',
			'WALKRE': 'WALKER',
			'WALLACE': '',
			'WALLCE': 'WALLACE',
			'WALLLACE': 'WALLACE',
			'WEBB': '',
			'WILKINS': '',
			'WOODRUFF': '',
			'[ APPLAUSE ]': '',
			'​​CRUZ': '​​CRUZ',
			'‘ QUICK': 'QUICK',
		}
		try:
			debate_list = [speaker.debate.debate_name for speaker in cls.select().where(cls.name == speaker_name)]
			return debate_list
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


class Interjection(Model):
	"""
	Class to represent interjections?
	"""
	pass


def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Debate, Speaker, SpeakerText], safe=True)
	DATABASE.close()
