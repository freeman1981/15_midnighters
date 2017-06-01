import requests
import pytz
from datetime import datetime


def load_attempts():
    url_attemts = 'https://devman.org/api/challenges/solution_attempts/'
    response_dict = requests.get(url_attemts).json()
    number_of_pages = response_dict['number_of_pages']
    for page in range(1, number_of_pages):
        params = {
            'page': page
        }
        response_dict = requests.get(url_attemts, params=params).json()
        records = response_dict['records']
        for record in records:
            yield {
                'username': record['username'],
                'timestamp': record['timestamp'],
                'timezone': record['timezone'],
            }


def show_midnighters():
    header = 'Users who sends tasks after midnight before early morning'
    print(header)
    print('-' * len(header))
    username_set = set()
    for record in load_attempts():
        timestamp = record['timestamp']
        if timestamp is None:
            continue
        time_zone = pytz.timezone(record['timezone'])
        date_time = datetime.fromtimestamp(timestamp, time_zone)
        if 0 < date_time.hour < 4 and record['username'] not in username_set:
            print(record['username'])
            username_set.add(record['username'])

if __name__ == '__main__':
    show_midnighters()
