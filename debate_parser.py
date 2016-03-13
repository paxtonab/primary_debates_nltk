from nltk.corpus import stopwords

import nltk
import re


# conda create -n nlp python=3 anaconda
# source activate nlp
# source deactivate


def open_file(file_name):
    file = open(file_name)
    text = file.read()
    return text

def get_speakers(text):
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
        if i.find('(') != -1:
            interjection_list.append(i)

    # remove any interjections from speaker_list
    for i in interjection_list:
        if i in speaker_list:
            speaker_list.remove(i)

    return speaker_list, interjection_list


def split_on_speaker(speaker_list, text):
    # split text on each speaker in speaker_list
    delimiters = speaker_list
    pattern = '|'.join(map(re.escape, delimiters))
    pattern = '('+pattern+')'
    speaker_text = re.split(pattern, text)

    # set up variables to loop through each item in speaker_text sequentially
    # unless there is a way to get item in list and then get the item at item index + 1?
    # .next() type of command for list ... w/e it's called... iteration?
    i = 0
    parsed_text = []

    # because of how the text is structured each item that is a speaker
    # will have the speaker's text immediately following it i.e. i+1
    while i < len(speaker_text) - 1:
        if speaker_text[i] in speaker_list:
            parsed_text.append({'speaker':speaker_text[i], 'text':speaker_text[i+1]})
        i += 1

    return parsed_text


def speaker_stats(speaker_list, parsed_text):
    speaker_stat_list = []

    for i in speaker_list:
        speaker_stat_list.append({
            'speaker':i,
            'text':'',
            'count':0,
            'count_unique_words':0,
            'count_words_spoken':0,
            'avg_words_spoken':0,
            # add additional stats here
            'fd':[]
        })

    for i in parsed_text:
        for item in speaker_stat_list:
            if item['speaker'] == i['speaker']:
                item['count'] += 1
                item['text'] = item['text']+i['text']
                tokens = nltk.word_tokenize(i['text'])
                nltk_text = nltk.Text(tokens)
                nltk_text_scrubbed = [w for w in nltk_text if w.isalpha()]
                item['count_words_spoken'] += len(nltk_text_scrubbed)

    # nltk processing of text
    for item in speaker_stat_list:
        # create tokens
        tokens = nltk.word_tokenize(item['text'])
        # create NLTK text
        nltk_text = nltk.Text(tokens)
        # scrub punctuations
        nltk_text_scrubbed = [w for w in nltk_text if w.isalpha()]
        # create frequency distribution
        fd = nltk.FreqDist(nltk_text_scrubbed)
        # get unique words
        item['count_unique_words'] = len(fd)
        # get average word count
        try:
            item['avg_words_spoken'] = item['count_words_spoken']/item['count']
        except ZeroDivisionError:
            item['avg_words_spoken'] = 0

        #scrub stopwords for plotting and redo fd then append as list
        sw = stopwords.words('english')
        nltk_text_scrubbed = [w.lower() for w in nltk_text if w.isalpha() and w.lower() not in sw]
        fd = nltk.FreqDist(nltk_text_scrubbed)
        fd_items = fd.items()
        fd_list = []
        for fd_item in fd_items:
            fd_list.append(fd_item)

        item['fd'] = fd_list


    return speaker_stat_list


def main():
    file_list = [
            '9_republican_debate.txt',
            '8_republican_debate.txt',
            '7_republican_debate.txt',
            '6_republican_debate.txt',
            '5_republican_debate.txt',
            '4_republican_debate.txt',
            '3_republican_debate.txt',
            '2_republican_debate.txt',
            '1_republican_debate.txt'
            ]

    moderator_list = [
                'KELLY',
                'BAIER',
                'WALLACE',
                'TAPPER',
                'HEWITT',
                'BASH',
                'BLITZER',
                'RADDATZ',
                'QUINTANILLA',
                'QUICK',
                'HARWOOD',
                'BAKER',
                'CAVUTO',
                'BARTIROMO',
                'KELLY',
                'MUIR',
                'DICKERSON',
                'GARRETT',
                'STRASSEL'
            ]

    candidate_list = [
                'TRUMP',
                'CRUZ',
                'RUBIO',
                'KASICH',
                'CARSON',
                'BUSH',
                'WALKER',
                'HUCKABEE',
                'PAUL',
                'CHRISTIE',
                'FIORINA'
            ]

    for file in file_list:
        text = open_file(file)
        speaker_list, interjection_list = get_speakers(text)
        parsed_text = split_on_speaker(speaker_list, text)
        speaker_stat_list = speaker_stats(speaker_list, parsed_text)

        with open('debate_main.csv','a') as main:
            for i in speaker_stat_list:
                if i['speaker'] in candidate_list:
                    main.write(
                        i['speaker']+','
                        +str(i['count'])+','
                        +str(i['count_unique_words'])+','
                        +str(i['count_words_spoken'])+','
                        +str(i['avg_words_spoken'])+','
                        +file
                        +'\n'
                    ) # add other stats here... like all text: +','+i['text'])

        with open('debate_fd.csv','a') as fd:
            for i in speaker_stat_list:
                if i['speaker'] in candidate_list:
                    for dist in i['fd']:
                        (key, value) = dist
                        fd.write(
                            i['speaker']+','
                            +str(key)+','
                            +str(value)+','
                            +file
                            +'\n'
                        ) # add other stats here... like all text: +','+i['text'])

main()
