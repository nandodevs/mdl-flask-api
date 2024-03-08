from flask import Flask, json
import requests
from bs4 import BeautifulSoup
from cachetools import cached

app = Flask(__name__)

@app.route('/api/top-dramas', methods=['GET'])
@cached(cache={})
def get_top_dramas():
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
                link_dorama = bloco['href']
                
                # Utilizando o atributo data-src para obter a imagem
                link_imagem_elemento = bloco.find("img", class_="img-responsive")
                link_imagem = link_imagem_elemento['data-src'].replace("s.jpg", "c.jpg") if link_imagem_elemento else ""

                titulo_elemento = bloco.find_next("h6", class_="text-primary title")
                nome_dorama = titulo_elemento.text.strip() if titulo_elemento else ""

                classificacao_elemento = bloco.find_next("span", class_="p-l-xs score")
                classificacao_valor = classificacao_elemento.text.strip() if classificacao_elemento else ""

                # Adicionar os dados à lista de dramas
                drama = {
                    "Imagem": link_imagem,
                    "Título": nome_dorama,
                    "Link": link_dorama,
                    "Classificação": classificacao_valor
                }
                dramas.append(drama)

        else:
            return json({"error": f"Erro ao acessar o site: {response.status_code}"})

    # Retorna os resultados como JSON em UTF-8
    return json.dumps(dramas, ensure_ascii=False)

if __name__ == '__main__':
    app.run(debug=True)
