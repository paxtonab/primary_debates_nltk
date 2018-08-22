import debate_parser
import models
import interjection_utils


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
            models.Speaker.create_speaker(speaker)
            models.SpeakerDebate.create_speaker(speaker, file_name)

        # loop through all interjections and populate table
        interjection_list = interjection_utils.get_cleaned_interjection_list(interjection_list)
        for interjection in interjection_list:
            models.Interjection.create_interjection(interjection)


def initialize_speakers_text():
    # get file names
    file_list = models.Debate.get_debates()

    # loop through files and get speakers and text
    for file_name in file_list:
        # read the file
        file_text = debate_parser.open_file(file_name)

        # get the speakers for specific file
        speaker_list = models.SpeakerDebate.get_speakers(file_name, False)

        # get the parsed text with new speakers
        parsed_text = debate_parser.split_on_speaker(speaker_list, file_text)

        for pt in parsed_text:
            models.SpeakerText.create_speaker_text(pt['text'], pt['order'], pt['speaker'], file_name)


def initialize_text_interjections():
    # get speaker_text
    speaker_text = models.SpeakerText.select()

    # get interjection pattern
    interjection_pattern = models.Interjection.get_interjection_pattern()
    mapped_interjections = models.Interjection.get_unique_mapped_interjections()

    # loop through speaker_text and create interjection_text
    for st in speaker_text:
        # read the file
        models.TextInterjection.create_text_interjection(st.speaker_text, st.id, interjection_pattern, mapped_interjections)


def main():
    initialize_debates()
    initialize_speakers()
    initialize_speakers_text()
    initialize_text_interjections()
