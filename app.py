import debate_parser
import models


def initialize_debates():
    # create database and initialize debates
    models.initialize()
    models.Debate.initialize_debates()


def initialize_speakers():
    # get file names
    file_list = models.Debate.get_debates()

    # loop through files and get speakers and text
    for file_name in file_list:
        # read the file
        file_text = debate_parser.open_file(file_name)
        # get list of speakers and list of Interjections
        # todo: do something with interjection_list
        speaker_list, interjection_list = debate_parser.get_speakers(file_text)

        # loop through all speakers and populate table
        for speaker in speaker_list:
            models.Speaker.create_speaker(speaker, file_name)


def initialize_speakers_text():
    # get file names
    file_list = models.Debate.get_debates()

    # loop through files and get speakers and text
    for file_name in file_list:
        # read the file
        file_text = debate_parser.open_file(file_name)

        # get the speakers for specific file
        speaker_list = models.Speaker.get_speakers(file_name)

        # get the parsed text with new speakers
        parsed_text = debate_parser.split_on_speaker(speaker_list, file_text)

        for pt in parsed_text:
            models.SpeakerText.create_speaker_text(pt['text'], pt['order'], pt['speaker'], file_name)
