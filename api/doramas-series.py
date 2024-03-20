import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)

def scrape_doramas(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    doramas = []

    for item in soup.find_all('article', class_='item movies'):
        dorama = {}
        dorama['title'] = item.find('h3').text.strip()
        dorama['image'] = item.find('img')['src']
        dorama['year'] = item.find('span').text.strip()
        dorama['link'] = item.find('a')['href']
        doramas.append(dorama)

    return doramas

@app.route('/doramas/legendado', methods=['GET'])
def get_legendado_doramas():
    url = 'https://doramasonline.org/br/generos/legendado/'
    doramas = scrape_doramas(url)
    return jsonify(doramas)

@app.route('/doramas/dublado', methods=['GET'])
def get_dublado_doramas():
    url = 'https://doramasonline.org/br/generos/dublado/'
    doramas = scrape_doramas(url)
    return jsonify(doramas)

if __name__ == '__main__':
    app.run(debug=True)
