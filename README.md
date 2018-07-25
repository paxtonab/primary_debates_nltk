# 2016 Presidential Primary Debates Text Analysis
A basic python script to parse transcripts of the 2016 Presidential Primary Debates and load into a SQLite database that can be used for further text analysis.
## Overview
Uses built in python types to transform text from csv's into parsed text that is loaded into a database to allow for basic aggregate stats, clustering and sentiment analysis. The primary package for creating aggregate stats is NLTK, creating frequency distributions per debate candidate, unique words spoken, etc.
## Setup

## TODO:
1. Refactor database initialization of `__main__`
1. Refactor `get_role` and `get_mapped_name` class methods
1. Remove `interjections` from `SpeakerText.text` and create counts for each interjection
1. Refactor `debate_stats` to load values into the database
1. Create data visualizations of `debate_stats`
1. Add clustering for topic extraction
1. Develop predictive models to determine speaker based off of text
