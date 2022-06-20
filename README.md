Aryan scraper
============

Run virtualenv
`source ./venv/bin/activate`

I have a fascination with WW2 history and how evil people may get into power.
This is a silly exercise to:
- [x] scrape the names of the SS high command from the Wikipedia page `scrape-names.py` as a CSV
- [x] use them to create folders `create-named-folders.py`
- [x] finds portraits of their faces with serpapi/google search image api `scraper.py`
- [x] extracts metadata for each name and saves it all as a JSON file `wiki.py`

## About

AryScraper is the scraper that created the male and female face "Aryan" data sets using photos of Holocaust perpetrators and the SS high command. Note: the whole exercise is arcane and not rooted in science. 

## Presumed Folder Structure

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