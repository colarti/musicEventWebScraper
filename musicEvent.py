import requests
import selectorlib as sl


URL = 'https://programmer100.pythonanywhere.com/tours/'

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
    print(f'Email Sent: {value}')
    save_value(value)


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


if __name__ == '__main__':
    text = scrape(URL)
    # print(text)

    value = extract(text)
    print(f'VALUES: {value}')

    data = open_file()
    print(f'data: {data}')
    if value != 'No upcoming tours' and value not in data:
        send_email(value)