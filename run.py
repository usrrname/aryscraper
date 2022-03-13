from pathlib import Path
from scraper import scrape_images
import os

folders =  Path('./data-set/')

for entry in os.listdir(folders):
    print(entry)
    if os.path.isdir(entry):
        os.chdir(entry)
        print(os.getcwd())
        query = entry.replace('_', ' ')
        os.chdir('..')
  

