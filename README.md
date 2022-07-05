Aryan scraper
============
### WORK IN PROGRESS

This is one of multiple tools I'm working on as a _Black Mirror_-style proof-of-concept tool to demonstrate the ongoing harm of racial profiling, and how it may be perpetuated by face recognition and machine learning.

This repository shows a series of scripts I used to:

- [x] scrape the names of the SS high command from the Wikipedia page `scrape-names.py` and output them as a .csv
- [x] use them to create folders `create-named-folders.py`
- [x] finds portraits of their faces with serpapi/google search image api `scraper.py`
- [x] extracts metadata for each name and saves it all as a .json file `wiki.py`
- [x] some elementary face extraction in `haar_cascade.py`

## About

AryScraper is the scraper that created the male and female face "Aryan" data sets using photos of Holocaust perpetrators and the SS high command. Note: This whole exercise is arcane and not rooted in science but the interest was to use AI to see if we could perform some hyperblic "categorization" or averaging on samples of self-proclaimed "Aryans".

Such gestures in public take after "tactical media" or "tactical technology".

Although images here were compiled from publicly available sources, the dataset nor model is available here to prevent harmful misuse.

## Folder Structure

```
.
├── Makefile
├── .github               // github actions
├── README.md
├── requirements.txt
├── __pycache__
├── test
├── automate_scraping.py
├── create_folders.py
├── haar_cascade.py
├── names.py
├── scrape_names.py
├── scraper.py
├── ss-ranks.csv
├── util.py
├── wiki.py
├── men                   // images of male faces
└── women                 // images of female faces
```
