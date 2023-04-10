import requests
import zipfile
import io
import os


def update_prices():
    list_of_files = os.listdir('data')
    for file in list_of_files:
        if 'price-history-' in file:
            os.remove(f'data/{file}')

    r = requests.get('https://www.goatbots.com/download/price-history.zip?', stream=True)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(path='data')


def test():
    update_prices()


if __name__ == '__main__':
    test()
