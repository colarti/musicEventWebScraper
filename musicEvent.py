import requests
import selectorlib as sl
from send_message import send_msg
import time
import sqlite3 as sql



URL = 'https://programmer100.pythonanywhere.com/tours/'


info = sql.connect('data.db')


def scrape(url):
    ''' Scrape the page source from url'''
    response = requests.get(url)
    src = response.text

    return src

def extract(source):
    extractor = sl.Extractor.from_yaml_file('extract.yaml')
    value = extractor.extract(source)['tours']
    return value


def send_email(value):
    send_msg(value)


def save_value(value):
    with open('data.txt', 'a') as f:
        f.write(value + '\n')
    
    print(f'Saved to file: {value}')


def open_file():
    data = list()
    try:
        with open('data.txt', 'r') as f:
            for line in f.readlines():
                data.append(line.removesuffix('\n'))
    except:
        pass

    return data


def read_db(text_form):
    global info

    event = text_form.split(',')
    event = [item.strip() for item in event]
    band, city, date = event

    cursor = info.cursor()
    cursor.execute('SELECT * FROM events WHERE band=? AND city=? AND date=?', (band, city, date))
    results = cursor.fetchall()

    print(f'READ_DB: {results}')

    return results


def write_db(value):
    global info

    event = value.split(',')
    event = [item.strip() for item in event]
    print(f'event: {event}')
    band, city, date = event

    cursor = info.cursor()
    cursor.execute('INSERT INTO events VALUES(?,?,?)', (band, city, date))
    info.commit()

    print(f'WRITE_DB...')




if __name__ == '__main__':
    while True:
        text = scrape(URL)
        # print(text)

        value = extract(text)
        print(f'EXTRACTED: {value}')

        # data = open_file()        #using csv/text file
        # print(f'data: {data}')
        
        if value != 'No upcoming tours':
            results = read_db(value)
            if len(results) == 0:
                send_email(value)
                # save_value(value) #using csv/text file

                write_db(value)
            else:
                print(f'Event already exists')
                
        

        time.sleep(10)