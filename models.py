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
					cls.create(
								file_name=row['File'],
								debate_name=row['File'].split('.')[0],
								order=row['Order'],
								party=row['Party'],
								friendly_name=row['Friendly Name'],
								city=row['City'],
								state=row['State'],
								location=row['Location'],
								debate_date=row['Date']
								)
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
				cls.create(
							name=name,
							debate=debate_id,
							mapped_name=cls.get_mapped_name(name)
							)
		except IntegrityError:
			raise ValueError("Speaker exists")


	@classmethod
	def get_speakers(cls, file_name, use_mapped_name=True):
		"""
		Get a list of all the speakers in a specific debate text file

		:params : file_name name of file to limit speakers by
		:ret : speaker_list list of speaker names
		"""
		try:
			if use_mapped_name:
				speaker_list = [speaker.mapped_name for speaker in cls.select() if speaker.debate.file_name == file_name]
				speaker_list = list(set(speaker_list))
				return speaker_list
			else:
				speaker_list = [speaker.name for speaker in cls.select() if speaker.debate.file_name == file_name]
				speaker_list = list(set(speaker_list))
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
	def get_mapped_name(cls, name):
		"""
		Map all Speaker.name to a friendly version to eliminate typos

		:params : name Speaker name with typos
		:ret : mapped_name Speaker name without typos
		"""
		replacement_dict ={
			' LOOK BACK': '',
			' OPEN GRAPHIC': '',
			' OPEN INTERACTIVE GRAPHIC': '',
			' OUR ANALYSIS': '',
			'. COOPER': 'COOPER',
			'ALEXIS': 'KULASH',
			'ALEXIS KULASH, DRAKE UNIVERSITY STUDENT': 'KULASH',
			'ANNOUNCER': '',
			'ARNOLD WOODS, PRESIDENT, DES MOINES NAACP': 'WOODS',
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
			'BRETT ROSENGREN, STUDENT': 'ROSENGREN',
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
			'DEBORAH PLUMMER': 'PLUMMER',
			'DICK GOODSON, CHAIRMAN, DES MOINES COMMITTEE ON FOREIGN RELATIONS': 'GOODSON',
			'DICKERSON': '',
			'DINAN': '',
			'ELECTION 2016': '',
			'END​': '',
			'EPPERSON': '',
			'FIONNA': 'FIORINA',
			'FIORINA': '',
			'FRANCHESCA RAMSEY': 'RAMSEY',
			'FRANTA': '',
			'FROM OUR ADVERTISERS': '',
			'GARRET': '',
			'GARRETT': 'GARRET',
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
			'JENNA BISHOP, DRAKE UNIVERSITY LAW SCHOOL STUDENT': 'BISHOP',
			'JOHN DICKERSON': 'DICKERSON',
			'JORGE RAMOS': 'RAMOS',
			'JOSH JACOB, COLLEGE STUDENT': 'JACOB',
			'JOY LASSEN': 'LASSEN',
			'JUL 13': '',
			'KAISCH': 'KASICH',
			'KARL': '',
			'KASICH': '',
			'KATHIE OBRADOVICH': 'OBRADOVICH',
			'KELLY': '',
			'KEVIN COONEY': 'COONEY',
			'LASSEN': '',
			'LEMON': '',
			'LEVESQUE': '',
			'LIVE COVERAGE': '',
			'LOPEZ': '',
			'LOUIS': '',
			'MADDOW': '',
			'MAJOR GARRETT': 'GARRETT',
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
			'NANCY CORDES': 'CORDES',
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
			'SEAN COLLISON': 'COLLISON',
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
			if replacement_dict[name] and replacement_dict[name] != '':
				return replacement_dict[name]
			else:
				return name
		except Exception as e:
			return e


	# @classmethod
	# def get_role(cls, mapped_name):
	# 	"""
	# 	Map a Speaker.mapped_name to a role:
	# 									CANDIDATE,
	# 									MODERATOR,
	# 									AUDIENCE MEMBER,
	# 									OTHER
	#
	# 	:params : name Speaker name to map to role
	# 	:ret : role Speaker role
	# 	"""
	# 	replacement_dict ={
	# 		'COOPER': 'MODERATOR',
	# 		'KULASH': 'AUDIENCE MEMBER',
	# 		'ANNOUNCER': '',
	# 		'WOODS': 'AUDIENCE MEMBER',
	# 		'ARRASAS': 'MODERATOR',
	# 		'AUDIENCE': '',
	# 		'AUDIENCE MEMBER': 'AUDIENCE MEMBER',
	# 		'BAIER': '',
	# 		'BAKER': '',
	# 		'BARTIROMO': '',
	# 		'BASH': '',
	# 		'BISHOP': '',
	# 		'BLITZER': '',
	# 		'ROSENGREN': 'AUDIENCE MEMBER',
	# 		'BROWNLEE': '',
	# 		'BUSH': '',
	# 		'CARSON': '',
	# 		'CAVUTO': '',
	# 		'CELESTE': '',
	# 		'CHAFEE': '',
	# 		'CHRISTIE': '',
	# 		'CLINTON': '',
	# 		'COLLISON': '',
	# 		'COOPER': '',
	# 		'CRAMER': '',
	# 		'CRAWFORD': '',
	# 		'CRUZ': '',
	# 		'CUBA': '',
	# 		'CUOMO': '',
	# 		'PLUMMER': 'AUDIENCE MEMBER',
	# 		'GOODSON': 'AUDIENCE MEMBER',
	# 		'DICKERSON': '',
	# 		'DINAN': '',
	# 		'EPPERSON': '',
	# 		'FIORINA': '',
	# 		'RAMSEY': '',
	# 		'FRANTA': '',
	# 		'GARRET': '',
	# 		'GOODSON': '',
	# 		'HAM': '',
	# 		'HANNITY': '',
	# 		'HARMAN': '',
	# 		'HARWOOD': '',
	# 		'HEWITT': '',
	# 		'HOLT': '',
	# 		'HUCKABEE': '',
	# 		'IFILL': '',
	# 		'BISHOP': 'AUDIENCE MEMBER',
	# 		'DICKERSON': '',
	# 		'JORGE RAMOS': 'RAMOS',
	# 		'JACOB': 'AUDIENCE MEMBER',
	# 		'LASSEN': '',
	# 		'KARL': '',
	# 		'KASICH': '',
	# 		'OBRADOVICH': '',
	# 		'KELLY': '',
	# 		'COONEY': '',
	# 		'LASSEN': '',
	# 		'LEMON': '',
	# 		'LEVESQUE': '',
	# 		'LOPEZ': '',
	# 		'LOUIS': '',
	# 		'MADDOW': '',
	# 		'GARRETT': '',
	# 		'MALE': 'AUDIENCE MEMBER',
	# 		'MCELVEEN': '',
	# 		'MILLER': '',
	# 		'MITCHELL': '',
	# 		'MODERATOR': '',
	# 		'MORE': '',
	# 		'MUIR': '',
	# 		'CORDES': '',
	# 		"O'CONNOR": '',
	# 		"O'MALLEY": '',
	# 		"O'REILLY": '',
	# 		'PAUL': '',
	# 		'PERRY': '',
	# 		'PLUMMER': '',
	# 		'QUICK': '',
	# 		'QUINTANILLA': '',
	# 		'RADDATZ': '',
	# 		'RAMOS': '',
	# 		'RITCHIE': '',
	# 		'ROSENGREN': '',
	# 		'RUBIO': '',
	# 		'SALINAS': '',
	# 		'SANDERS': '',
	# 		'SANTELLI': '',
	# 		'COLLISON': '',
	# 		'SMITH': '',
	# 		'STEPHANOPOULOS': '',
	# 		'STRASSEL': '',
	# 		'TALKER': '',
	# 		'TAPPER': '',
	# 		'TODD': '',
	# 		'TRUMP': '',
	# 		'TUMULTY': '',
	# 		'UNIDENTIFIABLE MALE': 'AUDIENCE MEMBER',
	# 		'UNIDENTIFIED FEMALE': 'AUDIENCE MEMBER',
	# 		'UNIDENTIFIED MALE': 'AUDIENCE MEMBER',
	# 		'WALKER': '',
	# 		'WALLACE': '',
	# 		'WEBB': '',
	# 		'WILKINS': '',
	# 		'WOODRUFF': ''
	# 	}
	# 	try:
	# 		if replacement_dict[name] and replacement_dict[name] != '':
	# 			return replacement_dict[name]
	# 		else:
	# 			return 'OTHER'
	# 	except Exception as e:
	# 		return e


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


	@classmethod
	def get_speaker_text(cls, speaker_name, use_mapped_name=True):
		try:
			if use_mapped_name:
				speaker_text = [(st.order, st.speaker_text, st.speaker.mapped_name, st.debate.friendly_name) for st in cls.select() if st.speaker.mapped_name == speaker_name]
				return speaker_text
			else:
				speaker_text = [(st.order, st.speaker_text, st.speaker.mapped_name, st.debate.friendly_name) for st in cls.select() if st.speaker.speaker_name == speaker_name]
				return speaker_text
		except Exception as e:
			return e


# class SpeakerDebateStats(Model):
# 	"""
# 	Class to represent speakers stats for an individual debate
# 	"""
# 	text = CharField(null=False)
# 	count_times_spoken = IntegerField(null=False)
# 	count_unique_words = IntegerField(null=False)
# 	count_total_words = IntegerField(null=False)
# 	avg_words_spoken = IntegerField(null=False)
# 	first_spoken = IntegerField(null=False)
# 	last_spoken = IntegerField(null=False)
# 	debate = ForeignKeyField(Debate, related_name='speaker_debate_stats_debate')
# 	speaker = ForeignKeyField(Speaker, related_name='speaker_debate_stats_speaker')
#
#
# 	@classmethod
# 	def get_speaker_debate_stats(cls, speaker_name, debate_name):
# 		try:
# 			with DATABASE.transaction():
# 				speaker_id = Speaker.get(Speaker.mapped_name == cls.last_name).id
# 				cls.update(speaker=speaker_id)
# 		except IntegrityError:
# 			raise ValueError("speaker text already exists")
#
#
# class SpeakerTotalStats(Model):
# 	"""
# 	Class to represent speakers stats for all debates in a given year
# 	"""
# 	last_name = CharField(null=False)
# 	role = IntegerField(null=False)
# 	speaker = ForeignKeyField(Speaker, related_name='speaker_speaker_role')
#
#
# 	@classmethod
# 	def get_mapped_speaker(cls):
# 		try:
# 			with DATABASE.transaction():
# 				speaker_id = Speaker.get(Speaker.mapped_name == cls.last_name).id
# 				cls.update(speaker=speaker_id)
# 		except IntegrityError:
# 			raise ValueError("speaker text already exists")


# class SpeakerRole(Model):
# 	"""
# 	Class to represent candidates vs. moderators
# 	Need some sort of scrubbing and/or replacement dict
# 	to map from the speaker class
# 	"""
# 	last_name = CharField(null=False)
# 	role = IntegerField(null=False)
# 	speaker = ForeignKeyField(Speaker, related_name='speaker_speaker_role')
#
#
# 	@classmethod
# 	def get_mapped_speaker(cls):
# 		try:
# 			with DATABASE.transaction():
# 				speaker_id = Speaker.get(Speaker.mapped_name == cls.last_name).id
# 				cls.update(speaker=speaker_id)
# 		except IntegrityError:
# 			raise ValueError("speaker text already exists")


class Interjection(Model):
	"""
	Class to represent interjections?
	"""
	pass


def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Debate, Speaker, SpeakerText], safe=True)
	DATABASE.close()
