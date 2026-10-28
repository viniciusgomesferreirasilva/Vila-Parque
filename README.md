# Vila Parque

Site do empreendimento Vila Parque, com Mall e Office, fotografias originais, plantas com busca e favoritos e apresentação única.

- Site: https://viniciusgomesferreirasilva.github.io/Vila-Parque/
- PDF único: https://viniciusgomesferreirasilva.github.io/Vila-Parque/assets/vila-parque-apresentacao-completa.pdf
- Repositório: https://github.com/viniciusgomesferreirasilva/Vila-Parque

## Desenvolvimento

Use o checkout existente; não crie worktrees. Na raiz, execute `python3 -m http.server 4173 --bind 0.0.0.0`. Não há dependências de frontend.

## Publicação

Depois de validar e commitar, execute `python3 publicar.py`. O script salva main e gh-pages, sem force-push. Confira o deploy nativo do GitHub Pages antes de confirmar publicação.

## PDF e imagens

`python3 unificar_pdf.py` gera o PDF único com capa, 17 páginas do VP e 23 páginas do BOOK. Requer PyMuPDF e Pillow. Verifica textos e hashes das imagens das 40 páginas-fonte. Fotografias originais não devem ser substituídas. O site oferece abertura e download direto do PDF, sem ZIP.
