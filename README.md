# Vila Parque

Site: https://viniciusgomesferreirasilva.github.io/Vila-Parque/

## Apresentações separadas

1. `assets/apresentacao-vila-parque.pdf`: primeiro material recebido, Vila Parque, 17 páginas.
2. `assets/book-mall-office-original.pdf`: segundo material recebido, BOOK Mall & Office, 23 páginas.

Os dois PDFs mantêm exatamente os arquivos originais fornecidos, sem substituição de imagens. O site tem botões separados para abrir e baixar cada um. O PDF unificado foi removido da versão atual por solicitação do usuário.

## Desenvolvimento e publicação

Use o checkout existente, sem criar worktrees. Na raiz, execute `python3 -m http.server 4173 --bind 0.0.0.0`. Não há dependências de frontend. Após validar e commitar, `python3 publicar.py` envia main e gh-pages sem force-push. Confira o deploy nativo do GitHub Pages antes de confirmar publicação.

## Baixar o site

Use **Baixar site completo** no site ou https://github.com/viniciusgomesferreirasilva/Vila-Parque/archive/refs/heads/main.zip . Extraia a pasta e abra `index.html`. O pacote inclui imagens, plantas e os dois PDFs separados. Somente links externos, como o mapa, exigem internet.
