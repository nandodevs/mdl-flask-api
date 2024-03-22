import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from cachetools import cached

app = Flask(__name__)

def scrape_doramas(url_template, page):
    url = url_template.format(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    return [
        {
            'title': item.find('h3').text.strip(),
            'image': item.find('img')['src'],
            'year': item.find('span').text.strip(),
            'link': item.find('a')['href']
        }
        for item in soup.find_all('article', class_='item movies')
    ]

@app.route('/api/doramas/legendado', methods=['GET'])
@cached(cache={})
def get_legendado_doramas():
    
    page = request.args.get('page', default=1, type=int)
    url_template = 'https://doramasonline.org/br/generos/legendado/page/{}/'
    doramas = scrape_doramas(url_template, page)
    return jsonify(doramas)

@app.route('/api/doramas/dublado', methods=['GET'])
@cached(cache={})
def get_dublado_doramas():
    page = request.args.get('page', default=1, type=int)
    url_template = 'https://doramasonline.org/br/generos/dublado/page/{}/'
    doramas = scrape_doramas(url_template, page)
    return jsonify(doramas)

if __name__ == '__main__':
    app.run(debug=True)
