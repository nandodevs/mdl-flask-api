import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

def scrape_doramas(url_template, total_pages):
    doramas = []

    for page_num in range(1, total_pages + 1):
        url = url_template.format(page_num)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        for item in soup.find_all('article', class_='item movies'):
            dorama = {}
            dorama['title'] = item.find('h3').text.strip()
            dorama['image'] = item.find('img')['src']
            dorama['year'] = item.find('span').text.strip()
            dorama['link'] = item.find('a')['href']
            doramas.append(dorama)

    return doramas

@app.route('/api/doramas/legendado', methods=['GET'])
def get_legendado_doramas():
    url_template = 'https://doramasonline.org/br/generos/legendado/page/{}/'
    total_pages = 25
    doramas = scrape_doramas(url_template, total_pages)
    return jsonify(doramas)

@app.route('/api/doramas/dublado', methods=['GET'])
def get_dublado_doramas():
    url_template = 'https://doramasonline.org/br/generos/dublado/page/{}/'
    total_pages = 25
    doramas = scrape_doramas(url_template, total_pages)
    return jsonify(doramas)

if __name__ == '__main__':
    app.run(debug=True)
