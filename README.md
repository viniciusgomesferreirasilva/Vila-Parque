# Vila Parque

Site: https://viniciusgomesferreirasilva.github.io/Vila-Parque/

## Apresentações separadas

1. `assets/vila-parque-empreendimento-redesenhado.pdf`: apresentação Vila Parque redesenhada, 19 páginas.
2. `assets/vila-parque-mall-office-redesenhado.pdf`: BOOK Mall & Office redesenhado, 25 páginas.

Os dois PDFs têm nova composição, tipografia, capas e organização. Textos, fotos e plantas são dos originais. As plantas técnicas permanecem vetoriais. O site tem botões separados para abrir e baixar cada um. O PDF unificado foi removido da versão atual por solicitação do usuário.

## Desenvolvimento e publicação

Use o checkout existente, sem criar worktrees. Na raiz, execute `python3 -m http.server 4173 --bind 0.0.0.0`. Não há dependências de frontend. Após validar e commitar, `python3 publicar.py` envia main e gh-pages sem force-push. Confira o deploy nativo do GitHub Pages antes de confirmar publicação.

## Baixar o site

Use **Baixar site completo** no site ou https://github.com/viniciusgomesferreirasilva/Vila-Parque/archive/refs/heads/main.zip . Extraia a pasta e abra `index.html`. O pacote inclui imagens, plantas e os dois PDFs separados. Somente links externos, como o mapa, exigem internet.

## Recriar os PDFs

Os originais ficam em `assets/apresentacao-vila-parque.pdf` e `assets/book-mall-office-original.pdf`, como fontes de trabalho. Instale `tools/requirements-pdf.txt`, com fontes DejaVu Sans e Serif disponíveis em `/usr/share/fonts/truetype/dejavu/`, e execute `python3 tools/redesenhar_pdfs.py`. O script redesenha os dois PDFs e verifica os termos dos textos e os hashes de pixels das fotografias utilizadas. A auditoria está em `assets/auditoria-redesign.json`. Plantas são incorporadas como conteúdo vetorial original, com nova organização ao redor. As prévias do site ficam em `assets/apresentacoes/`.

Uma fotografia/ilustração original por slide. As páginas com duas imagens foram desdobradas, preservando os textos. Montagens que já fazem parte de uma única imagem original são mantidas intactas. O mapa de localização usa a orientação correta de 180° e a foto da fachada usa 90°, mantendo os pixels originais.
