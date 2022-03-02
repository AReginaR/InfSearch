import requests
from bs4 import BeautifulSoup


# getting list of urls from a text file
def get_urls_from_file(filename):
    text_file = open(filename, 'r')
    urls_set = set()

    for line in text_file.readlines():
        urls_set.add(line[:-1])

    return list(urls_set)


links = get_urls_from_file('winx_list.tx')

counter = 1
result = open('index.txt', 'w+')

for link in links:
    print(f'link number {counter}: start')
    response = requests.get(link)
    response.encoding = 'UTF-8'
    url = response.text
    soup = BeautifulSoup(url, features="html.parser")
    soup.prettify()
    link_filename = f'link{counter}.html'
    with open(f'pages/{link_filename}', 'w+', encoding='utf-8') as file:
        file.write(str(soup))
    result.write(f'{counter}. {link}' + '\n')
    print(f'link number {counter}: done')
    counter += 1