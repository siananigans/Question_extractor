import sys
sys.path.append('..')
import time
import os
import requests


def time_test(text, size):
    endpoint = 'http://questionextractor-env.eba-mqvb3tex.eu-west-1.elasticbeanstalk.com/extract/'
    num = 10

    j = {
        'text': text,
        'num': num
    }

    start = time.time()
    response = requests.post(endpoint, j)
    end = time.time()

    time_taken = end - start
    print('Response with file size ' + str(size) + 'Bytes took ' + str(time_taken) + ' seconds with response code '+ str(response.status_code))


def main():
    directory = "../test_files/Load_Testing/"

    for file in os.listdir(directory):
        size = os.path.getsize(directory+file)
        f = open(directory+file, 'r')
        text = f.read()
        time_test(text, size)


if __name__ == '__main__':
    main()
