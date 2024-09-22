import requests
import os
from lxml import html
import json


def get_url(url, filename,pr):
    if not os.path.exists(filename):

        # fetch the page if it doesn't exist
        page = requests.get(url, params=pr)

        # save the page to a file
        with open(filename, 'w', encoding='UTF8') as f:
            f.write(page.text)

    else:
        page = requests.get(url, params=pr)
            
    return page
