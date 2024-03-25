from flask import Flask, json
import requests
from bs4 import BeautifulSoup
from cachetools import cached

app = Flask(__name__)

@app.route('/api/doramas-stars', methods=['GET'])
@cached(cache={})
def get_doramas():
    # Lista para armazenar os resultados
    dramas = []

    # Iterar sobre as 20 primeiras páginas
    for page in range(1, 21):
        # URL do site
        url = f"https://br.mydramalist.com/shows/top?page={page}"

        # Requisição HTTP
        response = requests.get(url)

        # Verificação de sucesso
        if response.status_code == 200:
            # Criação do objeto BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")

            # Busca por elementos que contêm os dados
            bloco_dramas = soup.find_all("a", class_="block")

            # Iterar sobre os dados encontrados
            for bloco in bloco_dramas:
                # Extrair informações
                linkDorama = bloco['href']
                
                # Utilizando o atributo data-src para obter a imagem
                link_imagem_elemento = bloco.find("img", class_="img-responsive")
                linkImagem = link_imagem_elemento['data-src'].replace("s.jpg", "c.jpg") if link_imagem_elemento else ""

                titulo_elemento = bloco.find_next("h6", class_="text-primary title")
                nomeDorama = titulo_elemento.text.strip() if titulo_elemento else ""

                classificacao_elemento = bloco.find_next("span", class_="p-l-xs score")
                classificacaoValor = classificacao_elemento.text.strip() if classificacao_elemento else ""

                # Adicionar os dados à lista de dramas
                drama = {
                    "imagem": linkImagem,
                    "titulo": nomeDorama,
                    "link": linkDorama,
                    "classificacao": classificacaoValor
                }
                dramas.append(drama)

        else:
            return json({"error": f"Erro ao acessar o site: {response.status_code}"})

    # Retorna os resultados como JSON em UTF-8
    return json.dumps(dramas, ensure_ascii=False)


@app.route('/api/series/dublado/', methods=['GET'])
@cached(cache={})
def series_dublado():
    # Lista para armazenar os resultados
    series = []

    # Iterar sobre as 20 primeiras páginas
    for page in range(1,8):
        # URL do site
        url = f'https://doramasonline.org/br/generos/dublado/page/{page}/'

        # Requisição HTTP
        response = requests.get(url)

        # Verificação de sucesso
        if response.status_code == 200:
            # Criação do objeto BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")
            

            # Iterar sobre os itens encontrados na página
            for item in soup.find_all('article', class_='item movies'):
                title = item.find('h3').text.strip()
                image = item.find('img')['src']
                link = item.find('a')['href']
                year_element = item.find('span')

                # Verificar se o campo 'Year' não está vazio antes de adicionar à lista
                if year_element:
                    year = year_element.text.strip()
                    series.append({'title': title, 'image': image, 'year': year, 'link': link})

        else:
            return json.dumps({"error": f"Erro ao acessar o site: {response.status_code}"})

    # Retorna os resultados como JSON em UTF-8
    return json.dumps(series, ensure_ascii=False)

@app.route('/api/series/legendado/', methods=['GET'])
@cached(cache={})
def series_legendado():
    # Lista para armazenar os resultados
    series_legendado = []

    # Iterar sobre as 20 primeiras páginas
    for page in range(1, 25):
        # URL do site
        url = f'https://doramasonline.org/br/generos/legendado/page/{page}/'

        # Requisição HTTP
        response = requests.get(url)

        # Verificação de sucesso
        if response.status_code == 200:
            # Criação do objeto BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")
            

            # Iterar sobre os itens encontrados na página
            for item in soup.find_all('article', class_='item movies'):
                title = item.find('h3').text.strip()
                image = item.find('img')['src']
                link = item.find('a')['href']
                year_element = item.find('span')

                # Verificar se o campo 'Year' não está vazio antes de adicionar à lista
                if year_element:
                    year = year_element.text.strip()
                    series_legendado.append({'title': title, 'image': image, 'year': year, 'link': link})

        else:
            return json.dumps({"error": f"Erro ao acessar o site: {response.status_code}"})

    # Retorna os resultados como JSON em UTF-8
    return json.dumps(series_legendado, ensure_ascii=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0')