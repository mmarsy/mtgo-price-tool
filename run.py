import os


def main():
    path = __file__[:__file__.find('\\run.py')]
    os.system(f'cd {path}')
    os.system('python main.py')


if __name__ == '__main__':
    main()
