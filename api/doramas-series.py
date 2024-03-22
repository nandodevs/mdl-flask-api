from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from cachetools import cached

app = Flask(__name__)

def extrair_dorama(item):
    # Extraindo o título
    titulo = item.find("h3").text.strip()

    # Extraindo a imagem
    imagem = item.find("img")["src"]

    # Extraindo o ano de lançamento
    ano_tag = item.find("span", class_="ano")
    ano = ano_tag.text.strip() if ano_tag else None

    # Extraindo o link
    link = item.find("a")["href"]

    # Retornando um dicionário com os dados
    return {
        "titulo": titulo,
        "imagem": imagem,
        "ano": ano,
        "link": link,
    }

def extrair_doramas(tipo, page):
    if tipo == "legendado":
        url = f"https://doramasonline.org/br/generos/legendado/page={page}"
    elif tipo == "dublado":
        url = f"https://doramasonline.org/br/generos/dublado/page={page}"
    else:
        return None

    # Fazendo a requisição HTTP
    response = requests.get(url)

    # Verificando se a requisição foi bem sucedida
    if response.status_code == 200:

        # Criando um objeto BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Encontrando todos os cards de doramas
        cards = soup.find_all("article", class_="item movies")

        # Extraindo os dados de cada dorama
        doramas = []
        for card in cards:
            doramas.append(extrair_dorama(card))

        # Retornando a lista de doramas
        return doramas

    # Se a requisição falhou, retornando None
    else:
        return "Erro na requisição, verifique o código!"

@app.route("/api/doramas/legendado", methods=["GET"])
@cached(cache={})
def get_legendado_doramas():
    # Lista para armazenar os resultados
    doramas = []

    # Iterar sobre as páginas
    for page in range(1, 21):
        page_doramas = extrair_doramas("legendado", page)
        if page_doramas:
            doramas.extend(page_doramas)
        else:
            return jsonify({"error": "Erro ao acessar a página"}, ensure_ascii=False)

    # Retorna os resultados como JSON em UTF-8
    return json.dumps(doramas, ensure_ascii=False)

@app.route("/api/doramas/dublado", methods=["GET"])
@cached(cache={})
def get_dublado_doramas():
    # Lista para armazenar os resultados
    doramas = []

    # Iterar sobre as páginas
    for page in range(1, 21):
        page_doramas = extrair_doramas("dublado", page)
        if page_doramas:
            doramas.extend(page_doramas)
        else:
            return json.dumps({"error": "Erro ao acessar a página"}, ensure_ascii=False)

    # Retorna os resultados como JSON em UTF-8
    return jsonify(doramas)

if __name__ == "__main__":
    app.run(debug=True)
