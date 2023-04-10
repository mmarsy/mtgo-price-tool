import requests
import zipfile
import io
import os


def import_card_definitions():
    r = requests.get('https://www.goatbots.com/download/card-definitions.zip?', stream=True)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(path='data')


def update_prices():
    list_of_files = os.listdir('data')
    for file in list_of_files:
        if 'price-history-' in file:
            os.remove(f'data/{file}')

    r = requests.get('https://www.goatbots.com/download/price-history.zip?', stream=True)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(path='data')


def test():
    import_card_definitions()


if __name__ == '__main__':
    test()
