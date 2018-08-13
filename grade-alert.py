import requests
import sys
import bs4
import re
import json
import pickle
from pathlib import Path
from lxml import html
from config import credentials, api_key

def login_session(USERNAME, PASSWORD):
    """Return logged in requests session"""
    LOGIN_URL = "https://cas.usherbrooke.ca/login?"
    session_requests = requests.session()
    tree = html.fromstring(session_requests.get(LOGIN_URL).text)
    payload = {
        "username": USERNAME, 
        "password": PASSWORD,
        "lt": list(set(tree.xpath("//input[@name='lt']/@value")))[0],
        "execution": list(set(tree.xpath("//input[@name='execution']/@value")))[0],
        "_eventId": list(set(tree.xpath("//input[@name='_eventId']/@value")))[0]
    }
    session_requests.post(LOGIN_URL, data=payload)

    return session_requests


def fetch_grades(session, url):
    response = session.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    script = soup.findAll("script")[3]
    p = re.compile(r'var\s+data\s+=\s+(\[.*\]);')
    found = p.findall(script.text)
    parsed_json = json.loads(found[0])

    return set([(d['controle'], d['tee']) for d in parsed_json[:-1] if d['tee'] != '--'])


def notify(message):
    url = 'https://www.nimrod-messenger.io/api/v1/message'
    payload = { 'api_key' : api_key, 'message' : message }
    requests.post(url, json=payload)


def main():
    URL = "http://www.gel.usherbrooke.ca/s6i/e18/doc/evaluations/notesEtu.php"
    # URL = "http://localhost:5000"
    session = login_session(credentials['username'], credentials['password'])

    old_grades_path = Path('old_grades')
    if old_grades_path.exists():
        with Path('old_grades').open(mode='rb') as f:
            old_grades = pickle.load(f)
    else:
        old_grades = set()
    
    new_grades = fetch_grades(session, URL)

    for change in new_grades - old_grades:
        print(change)
        notify("New grade: " + change[0] + " !")
    
    with Path('old_grades').open(mode='wb') as f:
        pickle.dump(new_grades, f)
    

if __name__ == '__main__':
    sys.exit(main())