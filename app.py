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
def series_dublado():
    series = []

    # URL da página com a lista de séries dubladas
    url = 'https://doramasonline.org/br/generos/dublado/'

    # Fazendo a requisição HTTP
    response = requests.get(url)

    # Verificação de sucesso
    if response.status_code == 200:
        # Criando um objeto BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Iterando sobre os itens de séries encontrados na página
        for item in soup.find_all('article', class_='item movies'):
            # Capturando o link da imagem
            image_link = item.find('img')['src']

            # Capturando o título
            title = item.find('h3').text.strip()

            # Capturando o link do dorama
            dorama_link = item.find('a')['href']

            # Fazendo uma nova requisição HTTP para obter mais informações sobre o dorama
            dorama_response = requests.get(dorama_link)

            # Verificação de sucesso
            if dorama_response.status_code == 200:
                # Criando um novo objeto BeautifulSoup para a página do dorama
                dorama_soup = BeautifulSoup(dorama_response.content, 'html.parser')

                # Capturando o link do vídeo
                video_link = None
                video_element = dorama_soup.find('video')
                if video_element:
                    video_link = video_element.get('src')

                # Capturando a tab de episódios e informações
                tabs = dorama_soup.find('ul', class_='smenu idTabs')

                # Iterando sobre as tabs
                tabs_info = {}
                if tabs:
                    for tab in tabs.find_all('li'):
                        tab_title = tab.text.strip()
                        tab_link = tab.find('a')['href']
                        tabs_info[tab_title] = tab_link

                # Capturando as informações da tab Episódios
                # Verificar se as informações de episódios estão presentes
                    episodes_section = dorama_soup.find('div', id='episodes')
                    if episodes_section:
                        # Extrair os detalhes dos episódios
                        episodios = episodes_section.find_all('li')
                        for episodio in episodios:
                            imagem_episodio = episodio.find('img').get('src')
                            numero_episodio = episodio.find('div', class_='numerando').text.strip()
                            titulo_episodio = episodio.find('div', class_='episodiotitle').find('a').text.strip()
                            link_episodio = episodio.find('div', class_='episodiotitle').find('a').get('href')
                            # Aqui você pode fazer o que quiser com as informações dos episódios, como adicionar a uma lista ou processá-las de outra forma
                    else:
                        print("Erro: não foi possível encontrar as informações de episódios para o dorama")

                    # Adicionando as informações à lista de séries
                    series.append({
                        'image': image_link,
                        'title': title,
                        'dorama_link': dorama_link,
                        'video_link': video_link,
                        'tabs_info': tabs_info,
                        'season_title': season_title,
                        'season_year': season_year,
                        'episodes': episodes
                    })
                else:
                    print(f"Erro: não foi possível encontrar as informações de episódios para o dorama {title}")
            else:
                print(f"Erro ao acessar a página do dorama: {dorama_link}")

    else:
        return json.dumps({"error": f"Erro ao acessar o site: {response.status_code}"})

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
    app.run()