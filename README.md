# Web Scraping de Top Dramas - MyDramaList

Este projeto realiza web scraping do site MyDramaList para obter informações sobre os melhores Doramas da atualidade, incluindo imagem, título, link e classificação. Os dados são disponibilizados através de uma API Flask.

## Tecnologias Utilizadas

- **Python:** A linguagem de programação principal utilizada no projeto.
- **Flask:** Um framework web leve para criar a API.
- **BeautifulSoup:** Uma biblioteca Python para fazer web scraping de maneira fácil.
- **Requests:** Uma biblioteca HTTP para realizar requisições.

## Como Utilizar

1. Certifique-se de ter o Python instalado no seu sistema.
2. Instale as dependências executando o comando: `pip install Flask requests beautifulsoup4`.
3. Execute o script Python usando o comando: `python nome_do_script.py`.
4. Acesse a API em `http://localhost:5000/api/top-dramas` no seu navegador ou através de um cliente de API.

## Exemplo de Resposta da API

```json
[
  {
    "Imagem": "https://i.mydramalist.com/2w44jE_4s.jpg?v=1",
    "Título": "Melancia Cintilante",
    "Link": "/739603-sparkling-watermelon",
    "Classificação": "9.2"
  },
  // Outros dramas...
]
```
## Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

## Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE.md para detalhes.
