from nltk.corpus import stopwords

import models
import nltk
import re


# conda create -n nlp python=3 anaconda
# source activate nlp
# source deactivate


def open_file(file_name):
    """
    Basic function to read a text file into memory

    :param : file_name path to text file

    :ret : text in memory of
    """
    file = open(file_name)
    text = file.read()
    return text


def get_speakers(text):
    """
    Extract Speaker names from Text based on capitalization
    and colons i.e. each Speaker's name is formatted like:

    `SPEAKER: What they speaker said.`

    Remove all audience reactions (i.e. Applause, Laughter)
    from the list of Speaker names and build separate list of Interjections
    Interjections are generally formmatted like:

    `(INTERJECTION)`

    :param : text path to text file

    :ret : speaker_list list of individuals who spoke during the debat
    :ret : interjection_list list of audience reactions
    """
    # split file on line breaks
    line_list = text.split('\n')
    temp_list = []
    speaker_list = []
    interjection_list = []

    # split each item on : to give us (speaker : text) list
    for i in line_list:
        temp_list.append(i.split(':'))

    # get list of unique speakers based on upper case
    for i in temp_list:
        if i[0].isupper() and i[0] not in speaker_list:
            speaker_list.append(i[0])

    # create interjection_list for (APPLAUSE), etc. based on '('
    for i in speaker_list:
        if i.find('(') != -1 or i.find(')') != -1: # or i.find(' ') != -1:
            interjection_list.append(i)

    # remove any interjections from speaker_list
    for i in interjection_list:
        if i in speaker_list:
            speaker_list.remove(i)

    return speaker_list, interjection_list


def split_on_speaker(speaker_list, text):
    """
    Split text on each speaker's name in speaker_list
    to group each individual's responses during each debate

    :param : speaker_list list of speaker's names
    :param : text of the debate

    :ret : parsed_text list of dict that contains speaker name order of text, etc.
    """
    # each speaker's name is used to split the text
    # format them into a regex pattern for split
    delimiters = speaker_list
    pattern = '|'.join(map(re.escape, delimiters))
    pattern = '('+pattern+')'

    # split the text using the new delimiters
    speaker_text = re.split(pattern, text)

    # set up variables to loop through each item in speaker_text sequentially
    # unless there is a way to get item in list and then get the item at item index + 1?
    # .next() type of command for list ... w/e it's called... iteration?
    i = 0
    parsed_text = []

    # add a variable to know the order of speakers
    speaking_order = 0

    # add a variable to track the index of the last item added to parsed_text
    parsed_text_index = 0

    # because of how the text is structured each item that is a speaker
    # will have the speaker's text immediately following it i.e. i+1
    while i < len(speaker_text) - 1:
        if speaker_text[i] in speaker_list:
            # check to see if prior speaker is same, and then add to prior text as opposed to increment
            if len(parsed_text) > 0:
                if parsed_text[parsed_text_index]['speaker'] == speaker_text[i]:
                    parsed_text[parsed_text_index]['text'] += speaker_text[i+1]
                else:
                    # increment order everytime successfully identified as a speaker
                    speaking_order += 1
                    parsed_text.append({
                        'speaker':speaker_text[i],
                        'text':speaker_text[i+1],
                        'order': speaking_order
                    })

                    if len(parsed_text) > 0:
                        parsed_text_index = len(parsed_text) - 1

            else:
                speaking_order += 1
                parsed_text.append({
                    'speaker':speaker_text[i],
                    'text':speaker_text[i+1],
                    'order': speaking_order
                })
        i += 1

    return parsed_text
