import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import webbrowser


def extract_price(content):
    pattern = re.compile(r'\d+KZT')
    match = re.search(pattern, content)
    try:
        match = match.group()
        match = match.replace('KZT', '')
        match = int(match)
    except AttributeError:
        match = float('inf')
    return match


if __name__ == '__main__':
    ref = input('Please paste your link below:\n')
    response = requests.get(ref)
    soup = BeautifulSoup(response.content, 'html.parser')
    buttons = soup.find_all('button')
    text = []
    buttons_filtered = ''
    for button in buttons:
        button_text = button.get_text().replace('\xa0', '')
        if 'KZT' in button_text:
            price = extract_price(button_text)
            if 2200 > price > 0:
                text.append(button_text)
                buttons_filtered += '\n' + str(button)
                pprint(text)

    new_html = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
    {buttons_filtered}
    </body>
    </html>
    '''

    with open('new_html.html', 'w') as f:
        f.write(new_html)

    webbrowser.open('http://localhost:8000/new_html.html')

    with TCPServer(('', 8000), SimpleHTTPRequestHandler) as httpd:
        httpd.serve_forever()
