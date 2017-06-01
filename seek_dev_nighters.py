import requests
import pytz
from datetime import datetime


def load_attempts():
    url_attempts = 'https://devman.org/api/challenges/solution_attempts/'
    response_dict = requests.get(url_attempts).json()
    number_of_pages = response_dict['number_of_pages']
    for page in range(1, number_of_pages):
        params = {
            'page': page
        }
        response_dict = requests.get(url_attempts, params=params).json()
        records = response_dict['records']
        for record in records:
            yield {
                'username': record['username'],
                'timestamp': record['timestamp'],
                'timezone': record['timezone'],
            }


def get_midnighters_names():
    return {
        record['username'] for record in load_attempts()
        if record['timestamp'] is not None and
        0 < datetime.fromtimestamp(record['timestamp'], pytz.timezone(record['timezone'])).hour < 4
    }


def show_midnighters(midnighters_names):
    header = 'Users who sends tasks after midnight before early morning'
    print(header)
    print('-' * len(header))
    for name in midnighters_names:
        print(name)


if __name__ == '__main__':
    midnighters_names = get_midnighters_names()
    show_midnighters(midnighters_names)
