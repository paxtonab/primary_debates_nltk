import csv
import datetime
import json
import re

from collections import Counter
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
	name = CharField(unique=True)
	role = CharField(null=True)
	# full_name = CharField(null=True)
	# party = CharField(null=True)

	class Meta:
		database = DATABASE
		order_by = ('role','name',)


	@classmethod
	def create_speaker(cls, name):
		try:
			name = cls.get_mapped_name(name)
			role = cls.get_role(name)
			with DATABASE.transaction():
				cls.create(
							name=name,
							role=role
							)
		except IntegrityError:
			pass


	@classmethod
	def get_all_speakers(cls):
		"""
		Get a list of all the speakers

		:ret : speaker_list list of speaker names
		"""
		speaker_list = [speaker.name for speaker in cls.select()]
		return speaker_list


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


	@classmethod
	def get_role(cls, name):
		"""
		Map a Speaker.name to a role:
										CANDIDATE,
										MODERATOR,
										AUDIENCE,
										OTHER

		:params : name Speaker name to map to role
		:ret : role Speaker role
		"""
		replacement_dict ={
			'COOPER': 'MODERATOR',
			'KULASH': 'AUDIENCE',
			'ANNOUNCER': '',
			'WOODS': 'AUDIENCE',
			'ARRASAS': 'MODERATOR',
			'AUDIENCE': 'AUDIENCE',
			'AUDIENCE MEMBER': 'AUDIENCE',
			'BAIER': '',
			'BAKER': '',
			'BARTIROMO': '',
			'BASH': 'MODERATOR',
			'BISHOP': '',
			'BLITZER': 'MODERATOR',
			'ROSENGREN': 'AUDIENCE',
			'BROWNLEE': '',
			'BUSH': 'CANDIDATE',
			'CARSON': 'CANDIDATE',
			'CAVUTO': '',
			'CELESTE': '',
			'CHAFEE': '',
			'CHRISTIE': 'CANDIDATE',
			'CLINTON': 'CANDIDATE',
			'COLLISON': '',
			'COOPER': 'MODERATOR',
			'CRAMER': '',
			'CRAWFORD': '',
			'CRUZ': 'CANDIDATE',
			'CUBA': '',
			'CUOMO': 'CANDIDATE',
			'PLUMMER': 'AUDIENCE',
			'GOODSON': 'AUDIENCE',
			'DICKERSON': '',
			'DINAN': '',
			'EPPERSON': '',
			'FIORINA': 'CANDIDATE',
			'RAMSEY': '',
			'FRANTA': '',
			'GARRET': '',
			'GOODSON': '',
			'HAM': '',
			'HANNITY': 'MODERATOR',
			'HARMAN': '',
			'HARWOOD': '',
			'HEWITT': '',
			'HOLT': '',
			'HUCKABEE': 'CANDIDATE',
			'IFILL': '',
			'BISHOP': 'AUDIENCE',
			'DICKERSON': '',
			'JORGE RAMOS': '',
			'JACOB': 'AUDIENCE',
			'LASSEN': '',
			'KARL': '',
			'KASICH': 'CANDIDATE',
			'OBRADOVICH': '',
			'KELLY': '',
			'COONEY': '',
			'LASSEN': '',
			'LEMON': '',
			'LEVESQUE': '',
			'LOPEZ': '',
			'LOUIS': '',
			'MADDOW': 'MODERATOR',
			'GARRETT': '',
			'MALE': 'AUDIENCE',
			'MCELVEEN': '',
			'MILLER': '',
			'MITCHELL': '',
			'MODERATOR': 'MODERATOR',
			'MORE': '',
			'MUIR': '',
			'CORDES': '',
			"O'CONNOR": 'MODERATOR',
			"O'MALLEY": 'CANDIDATE',
			"O'REILLY": 'MODERATOR',
			'PAUL': '',
			'PERRY': 'CANDIDATE',
			'PLUMMER': '',
			'QUICK': '',
			'QUINTANILLA': '',
			'RADDATZ': '',
			'RAMOS': '',
			'RITCHIE': '',
			'ROSENGREN': '',
			'RUBIO': 'CANDIDATE',
			'SALINAS': '',
			'SANDERS': 'CANDIDATE',
			'SANTELLI': '',
			'COLLISON': '',
			'SMITH': '',
			'STEPHANOPOULOS': '',
			'STRASSEL': '',
			'TALKER': '',
			'TAPPER': '',
			'TODD': '',
			'TRUMP': 'CANDIDATE',
			'TUMULTY': '',
			'UNIDENTIFIABLE MALE': 'AUDIENCE',
			'UNIDENTIFIED FEMALE': 'AUDIENCE',
			'UNIDENTIFIED MALE': 'AUDIENCE',
			'WALKER': '',
			'WALLACE': '',
			'WEBB': '',
			'WILKINS': '',
			'WOODRUFF': ''
		}
		try:
			if replacement_dict[name] and replacement_dict[name] != '':
				return replacement_dict[name]
			else:
				return 'OTHER'
		except Exception as e:
			return e


class SpeakerDebate(Model):
	name = CharField(null=False)
	debate = ForeignKeyField(Debate, related_name='speaker_debate_debate_fk')
	mapped_name = CharField(null=True)
	speaker = ForeignKeyField(Speaker, related_name='speaker_debate_speaker_fk')

	class Meta:
		database = DATABASE
		order_by = ('debate','name',)


	@classmethod
	def create_speaker(cls, name, file_name):
		try:
			mapped_name = Speaker.get_mapped_name(name)
			debate_id = Debate.get(Debate.file_name == file_name).id
			speaker_id = Speaker.get(Speaker.name == mapped_name).id
			with DATABASE.transaction():
				cls.create(
							name=name,
							debate=debate_id,
							mapped_name=mapped_name,
							speaker=speaker_id
							)
		except IntegrityError:
			raise ValueError("Speaker exists")


	@classmethod
	def get_all_speakers(cls):
		"""
		Get a list of all the speakers

		:ret : speaker_list list of speaker names
		"""
		speaker_list = [speaker.mapped_name for speaker in cls.select()]
		speaker_list = list(set(speaker_list))
		return speaker_list


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


class SpeakerText(Model):
	speaker_text = CharField(null=False)
	clean_text = CharField(null=True)
	order = IntegerField(null=False)
	speaker_debate = ForeignKeyField(SpeakerDebate, related_name='speaker_debate_speaker_text')

	class Meta:
		database = DATABASE
		order_by = ('speaker_debate','order',)


	@classmethod
	def create_speaker_text(cls, speaker_text, order, speaker_name, file_name, interjection_pattern):
		try:
			with DATABASE.transaction():
				debate_id = Debate.get(Debate.file_name == file_name).id
				speaker_debate_id = SpeakerDebate.get(SpeakerDebate.name == speaker_name, SpeakerDebate.debate == debate_id).id
				cls.create(
							speaker_text=speaker_text,
							clean_text=cls.get_clean_text(speaker_text, interjection_pattern),
							order=order,
							speaker_debate=speaker_debate_id
							)
		except IntegrityError:
			raise ValueError("speaker text already exists")

	@classmethod
	def get_clean_text(cls, text, interjection_pattern):
	   text = text.replace('.\n','. ')
	   text = text.replace('?\n','. ')
	   text = text.replace('\n','')
	   text = text.replace(': ','')
	   text = text.replace('\\','')
	   text = re.sub(interjection_pattern, '', text)
	   text = text.strip()
	   return text

	@classmethod
	def get_speaker_text(cls, speaker_name):
		speaker_name = speaker_name.strip().upper()
		try:
			speaker_text = [{'order': st.order, 'text': st.speaker_text, 'speaker': st.speaker_debate.speaker.name, 'debate': st.speaker_debate.debate.friendly_name} for st in cls.select() if st.speaker_debate.speaker.name == speaker_name]
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
	interjection = CharField(unique=True)

	class Meta:
		database = DATABASE
		order_by = ('interjection',)


	@classmethod
	def create_interjection(cls, interjection):
		try:
			with DATABASE.transaction():
				cls.create(
						   interjection=interjection
						   )
		except IntegrityError:
			pass

	@classmethod
	def get_interjections(cls):
		try:
			interjections = [i.interjection for i in cls.select()]
			return interjections
		except Exception as e:
			return e

	@classmethod
	def get_interjection_pattern(cls):
		"""
		Get a list of interjections to use as delimiters for analyzing text
		"""
		delimiters = cls.get_interjections()
		pattern = '|'.join(map(re.escape, delimiters))
		pattern = '('+pattern+')'
		return pattern


	@classmethod
	def get_mapped_interjection(cls, interjection):
		"""
		Map all interjections to a condensed list:
		{
			'OTHER': 0,
			'AUDIENCE_LAUGHTER': 0,
			'AUDIENCE_APPLAUSE': 0,
			'CANDIDATE_CROSSTALK': 0,
			'AUDIENCE_MIXED': 0,
			'AUDIENCE_BOOING': 0,
			'CANDIDATE_SPANISH': 0,
			'DEBATE_BELL': 0,
			'MEDIA': 0,
			'UNKNOWN': 0,
			'CANDIDATE_STALLING': 0
		}
		"""
		interjection_dict = {
			'(4)': 'OTHER',
			'(APPLAUSE CHEERING)': 'AUDIENCE_APPLAUSE',
			'(APPLAUSE)': 'AUDIENCE_APPLAUSE',
			'(AUDIENCE BOOING)': 'AUDIENCE_BOOING',
			'(AUDIENCE BOOS)': 'AUDIENCE_BOOING',
			'(AUDIENCE REACTION)': 'AUDIENCE_MIXED',
			'(AUDIENCE)': 'AUDIENCE_MIXED',
			'(AUDIO GAP)': 'UNINTELLIGIBLE',
			'(BEGIN VIDEO CLIP)': 'MEDIA',
			'(BEGIN VIDEOTAPE)': 'MEDIA',
			'(BELL BRINGING)': 'DEBATE_BELL',
			'(BELL RING)': 'DEBATE_BELL',
			'(BELL RINGING)': 'DEBATE_BELL',
			'(BELL RINGS)': 'DEBATE_BELL',
			'(BELL SOUND)': 'DEBATE_BELL',
			'(BOOING)': 'AUDIENCE_BOOING',
			'(BOOS)': 'AUDIENCE_BOOING',
			'(BREAK)': 'MEDIA',
			'(BUZZER NOISE)': 'DEBATE_BELL',
			'(CHEERING AND APPLAUSE)': 'AUDIENCE_APPLAUSE',
			'(CHEERING)': 'AUDIENCE_APPLAUSE',
			'(CLOSE VIDEO CLIP)': 'MEDIA',
			'(COMMERCIAL BREAK)': 'MEDIA',
			'(COMMERCIAL NOT TRANSCRIBED)': 'MEDIA',
			'(COMMERCIAL)': 'MEDIA',
			'(CROSS TALK)': 'CANDIDATE_CROSSTALK',
			'(CROSSTALK)': 'CANDIDATE_CROSSTALK',
			'(DOUBLE BELL RINGS)': 'DEBATE_BELL',
			'(END VIDEO CLIP)': 'MEDIA',
			'(END VIDEOTAPE)': 'MEDIA',
			'(INAUDIBLE)': 'UNINTELLIGIBLE',
			'(Inaudible)': 'UNINTELLIGIBLE',
			'(LAUGH)': 'AUDIENCE_LAUGHTER',
			'(LAUGHING)': 'AUDIENCE_LAUGHTER',
			'(LAUGHTER AND APPLAUSE)': 'AUDIENCE_LAUGHTER',
			'(LAUGHTER)': 'AUDIENCE_LAUGHTER',
			'(LAUGHTER, BOOING)': 'AUDIENCE_LAUGHTER',
			'(LONG PAUSE)': 'CANDIDATE_STALLING',
			'(MIX OF APPLAUSE AND BOOING)': 'AUDIENCE_MIXED',
			'(MOMENT OF SILENCE)': 'MEDIA',
			'(MUSIC PLAYING, "AMERICA" BY SIMON & GARFUNKEL)': 'MEDIA',
			'(MUSIC)': 'MEDIA',
			'(OFF MIKE)': 'CANDIDATE_CROSSTALK',
			'(OVERTALK)': 'CANDIDATE_CROSSTALK',
			'(SINGING)': 'MEDIA',
			'(SPEAKING IN SPANISH)': 'CANDIDATE_SPANISH',
			'(SPEAKING SPANISH)': 'CANDIDATE_SPANISH',
			'(STAR SPANGLED BANNER)': 'MEDIA',
			'(THEME MUSIC)': 'MEDIA',
			'(THROAT CLEAR)': 'CANDIDATE_STALLING',
			'(UNINTEL)': 'UNINTELLIGIBLE',
			'(UNKNOWN)': 'UNINTELLIGIBLE',
			'(Video Intro)': 'MEDIA',
			'(Video ends)': 'MEDIA',
			'(c)': 'OTHER',
			'(in Spanish)': 'CANDIDATE_SPANISH',
			'(inaudible)': 'UNINTELLIGIBLE',
			'(k)': 'OTHER',
			'(oh)': 'OTHER',
			'(ph)': 'OTHER',
			'(sic)': 'UNINTELLIGIBLE',
			'(thousand)': 'OTHER',
			'(through translator)': 'OTHER',
			'(unintel)': 'UNINTELLIGIBLE'
		}

		try:
			return interjection_dict[interjection]
		except KeyError:
			return 'OTHER'

	@classmethod
	def get_unique_mapped_interjections(cls):
		mapped_interjections = [Interjection.get_mapped_interjection(i) for i in Interjection.get_interjections()]
		return mapped_interjections



class TextInterjection(Model):
	speaker_text_id = ForeignKeyField(SpeakerText, related_name='speaker_text_interjection_text_fk')
	audience_applause = IntegerField(null=False, default=0)
	audience_booing = IntegerField(null=False, default=0)
	audience_laughter = IntegerField(null=False, default=0)
	audience_mixed = IntegerField(null=False, default=0)
	candidate_crosstalk = IntegerField(null=False, default=0)
	candidate_spanish = IntegerField(null=False, default=0)
	candidate_stalling = IntegerField(null=False, default=0)
	debate_bell = IntegerField(null=False, default=0)
	media = IntegerField(null=False, default=0)
	unintelligible = IntegerField(null=False, default=0)
	other = IntegerField(null=False, default=0)

	class Meta:
		database = DATABASE
		order_by = ('speaker_text',)


	@classmethod
	def create_text_interjection(cls, speaker_text, speaker_text_id, interjection_pattern, mapped_interjections):
		# expected default is below dict of unique values from interjections
		# {'OTHER': 0, 'AUDIENCE_LAUGHTER': 0, 'AUDIENCE_APPLAUSE': 0, 'CANDIDATE_CROSSTALK': 0, 'AUDIENCE_MIXED': 0, 'AUDIENCE_BOOING': 0, 'CANDIDATE_SPANISH': 0, 'DEBATE_BELL': 0, 'MEDIA': 0, 'UNKNOWN': 0, 'CANDIDATE_STALLING': 0}
		# create a default dict and map text_interjections values to it
		text_interjections = cls.get_text_interjections(interjection_pattern, text=speaker_text)
		if text_interjections:
			default = {k:0 for k in mapped_interjections}
			context = {**default, **text_interjections}

			with DATABASE.transaction():
				cls.create(
							speaker_text_id=speaker_text_id,
							audience_applause=context['AUDIENCE_APPLAUSE'],
							audience_booing=context['AUDIENCE_BOOING'],
							audience_laughter=context['AUDIENCE_LAUGHTER'],
							audience_mixed=context['AUDIENCE_MIXED'],
							candidate_crosstalk=context['CANDIDATE_CROSSTALK'],
							candidate_spanish=context['CANDIDATE_SPANISH'],
							candidate_stalling=context['CANDIDATE_STALLING'],
							debate_bell=context['DEBATE_BELL'],
							media=context['MEDIA'],
							unintelligible=context['UNINTELLIGIBLE'],
							other=context['OTHER']
							)

	@classmethod
	def get_text_interjections(cls, interjection_pattern, text):
		interjection_list = re.findall(interjection_pattern, text)
		if len(interjection_list) > 0:
			interjection_list = [Interjection.get_mapped_interjection(interjection) for interjection in interjection_list]
			interjection_count = Counter(interjection_list)
			return interjection_count
		else:
			return None


def initialize():
	DATABASE.connect()
	DATABASE.create_tables([Debate, Speaker, SpeakerDebate, SpeakerText, Interjection, TextInterjection], safe=True)
	DATABASE.close()
