# Projeto Vila Parque — continuidade

O site é a prioridade. Preservar as imagens originais; não gerar substituições. Usuário autorizou commits e pushes de todas as alterações e pede link de acesso ao encerrar cada entrega.

## Fonte e integridade

`assets/apresentacao-vila-parque.pdf` é o VP original. As cinco fotos de destaque foram extraídas diretamente dos objetos do PDF, sem alterar seus bytes. `assets/fotos-originais.json` registra origem e SHA-256. A galeria também contém as 17 páginas inteiras. O PDF revisado atual preserva a composição original dentro de uma moldura; ainda não é a reformulação editorial solicitada.

## Pendências reais

- BOOK MALL E OFFICE V4 foi reenviado, mas `download_file` recusa arquivos maiores que 32 MiB antes de transferir bytes. Não foi importado nem analisado. É necessário receber versão menor/dividida ou URL de download acessível por ferramenta disponível. Autorização do usuário já existe; o bloqueio é técnico.
- Áudio da cliente não transcrito. Não inventar seus requisitos.
- Confirmar marca Vila Parque versus Vila Parque, dados de contato e conteúdo comercial.
- GitHub Actions contém publicação do site via Pages. Conferir resultado antes de afirmar que existe URL pública. Caso GitHub Pages precise ser habilitado por administrador, o workflow pode falhar em configure-pages.

## Desenvolvimento

Use o checkout existente, sem criar worktrees. `python3 -m http.server 4173 --bind 0.0.0.0 --directory vila-parque` na raiz do repositório. Sem dependências de frontend. Não alterar o aplicativo de currículos para executar este site.

## Entregas

Salvar alterações do site com commit e push para main; conferir o SHA remoto. Informar link público somente quando houver confirmação. Nunca descrever um commit local como backup remoto concluído.

## Atualização: BOOK recebido e integrado

O arquivo `BOOK_MALL_E_OFFICE_32MB.pdf` foi baixado com sucesso (10.203.481 bytes), aberto e analisado: 23 páginas. As pendências anteriores sobre acesso ao BOOK estão resolvidas. Original retido em `assets/book-mall-office-original.pdf`.

Site atualizado com Mall & Office, ficha técnica, endereço, créditos, 16 plantas com filtro por Mall/Office e galeria das 23 páginas. Fotografias extraídas dos objetos originais. PDF público único: `assets/vila-parque-apresentacao-completa.pdf` (41 páginas: capa nova + 17 do VP + 23 do BOOK). `unificar_pdf.py` reproduz o PDF e verifica texto e hashes de todas as imagens das 40 páginas-fonte. Não oferecer dois PDFs ao usuário nem arquivo ZIP como forma principal de acesso.

Diagnóstico confirmado de publicação: Actions run 40713909079 falhou em configure-pages porque o GITHUB_TOKEN não pode criar o site Pages: `Resource not accessible by integration`. Página ainda não habilitada. API administrativa retorna Forbidden nesta sessão. Ler Actions pela interface web github.com funciona. Não afirmar que Pages está publicado sem evidência.

## Publicação resolvida

O envio direto de uma branch `gh-pages` com o site na raiz ativou o GitHub Pages nativo automaticamente. Run `40715346928` terminou com **Status Success**, duração 45s, e publicou `https://viniciusgomesferreirasilva.github.io/VG-curr-culos-IA/`. A instrução anterior de exigir ativação manual está superada. O workflow personalizado que falhava foi removido para utilizar somente a publicação nativa.

Após cada alteração: validar, commitar, executar `python3 vila-parque/publicar.py` na raiz do repositório com acesso ao proxy Git. O script envia main e uma atualização sem force-push para gh-pages. Conferir o novo workflow nativo e fornecer o link direto ao usuário. O conteúdo público de gh-pages corresponde à pasta vila-parque da main.


## Marca corrigida

Nome solicitado e definitivo: **Vila Parque**, em português. Pasta versionada: `vila-parque/`; usar `python3 vila-parque/publicar.py`. Site e PDF único atualizados. Novas ferramentas: busca, filtro por favoritos locais e navegação da galeria por teclado.

A criação do novo repositório público `viniciusgomesferreirasilva/Vila-Parque` foi bloqueada pela revisão automática por falta de autorização explícita para esse novo destino público. Não repetir nem contornar a rejeição; pedir autorização específica ao usuário. Até lá, manter backup e site no repositório e URL existentes, sem dizer que a URL mudou.

## Autorização de migração confirmada pelo usuário

O usuário autorizou explicitamente criar o repositório público `viniciusgomesferreirasilva/Vila-Parque`. Não pedir essa autorização novamente. A revisão automática aceitou a tentativa de criação após essa confirmação; `gh repo create viniciusgomesferreirasilva/Vila-Parque --public` falhou antes da criação: `Get https://api.github.com/users/viniciusgomesferreirasilva: Forbidden`.

Diagnóstico: a política de rede em execução não inclui `api.github.com`. `GH_TOKEN` está presente; não ler seu valor nem solicitar token novo sem testar a configuração após a liberação da rede. Rascunho de configuração atualizado com os destinos adicionais `api.github.com` e `viniciusgomesferreirasilva.github.io`, preservando os presets existentes. Ferramenta confirmou `status: saved`, `requires_publish: true`. Essa gravação não aplica a política à instância em execução. Nome do ambiente corrigido para Vila Parque por ferramenta de metadados, com sucesso.

Próximos passos quando as configurações forem aplicadas/publicadas: conferir o estado do ambiente, repetir a operação de criação autorizada; se funcionar, publicar somente o conteúdo de `vila-parque/` na raiz da main e da gh-pages do novo repositório, verificar deploy nativo e passar o novo link `/Vila-Parque/`. Preservar o repositório anterior como backup; não renomeá-lo nem remover o aplicativo de currículos. URL nova ainda não foi criada nem validada. Não contornar o proxy ou a política de rede.


## Migração para repositório dedicado

O usuário criou o repositório público Vila-Parque, e a leitura Git confirmou que estava vazio. O site foi copiado para a raiz de `/workspace/Vila-Parque`, preservando o repositório anterior e os backups em `/workspace/backups`. Esta é agora a pasta de trabalho do site. `publicar.py` foi ajustado para publicar a raiz, main e gh-pages no novo origin. O botão Baixar PDF oferece download direto do único PDF público, sem ZIP. URLs antigas em registros anteriores são históricas; usar `/Vila-Parque/`.

## Migração concluída e publicação confirmada

O site está publicado no repositório dedicado `viniciusgomesferreirasilva/Vila-Parque`, raiz da main e gh-pages. O deploy nativo 40718779075 concluiu com Status Success em 1m31s. Endereço: https://viniciusgomesferreirasilva.github.io/Vila-Parque/ . Botão Baixar PDF completo validado com download real em Chromium, desktop 1440px e celular 390px; nome Vila-Parque-Apresentacao-Completa.pdf, 41 páginas.

A exclusão do repositório antigo foi tentada após confirmar a publicação e os backups, conforme autorização do usuário: `gh repo delete viniciusgomesferreirasilva/VG-curr-culos-IA --yes`. A API retornou Forbidden; o antigo NÃO foi excluído. O site e todos os próximos trabalhos devem usar este repositório dedicado, não o anterior. A exclusão é a única pendência da migração.


## PDFs separados — requisito atual

O usuário alterou o requisito: o primeiro PDF Vila Parque (17 páginas) e o segundo BOOK Mall & Office (23 páginas) devem permanecer SEPARADOS. Instruções anteriores para unir os materiais estão superadas. O site oferece quatro botões: abrir e baixar para cada PDF. Originais mantidos byte a byte. O PDF unificado, seu gerador e auditoria foram removidos da versão atual; continuam no histórico Git. O download do site contém os dois arquivos separados.


## Downloads alternativos

Usuário relatou falha nos anexos locais do chat para BOOK e site ZIP. Disponibilizar links HTTPS do GitHub: BOOK pelo endpoint github.com/.../raw/refs/heads/main/assets/book-mall-office-original.pdf e site pelo codeload.github.com/.../zip/refs/heads/main. Não depender somente de links sandbox temporários. Site ganhou link alternativo do BOOK e download do site via codeload. A pasta /mnt/data não é gravável neste ambiente mesmo com escalonamento; não prometer anexos por esse caminho.


## Redesign real dos dois PDFs

O usuário esclareceu que queria aprimorar a diagramação dos PDFs, preservando textos e imagens, além do site. Foram criados dois PDFs novos e separados: `assets/vila-parque-empreendimento-redesenhado.pdf` (17 páginas) e `assets/vila-parque-mall-office-redesenhado.pdf` (23 páginas). Novas capas, tipografia, grid, espaçamento, hierarquia e reorganização de fotos e plantas; não são molduras com as páginas antigas dentro. Fotos vêm dos objetos originais, sem substituição ou geração. Textos preservados; auditoria compara contagem de termos por página. Plantas originais incorporadas vetorialmente com novo layout lateral. `tools/redesenhar_pdfs.py` reproduz o trabalho; requisitos e auditoria acompanham. O site oferece estes novos PDFs, capas e 40 prévias novas. Arquivos-fonte originais continuam retidos no repositório.


## Uma imagem por slide e orientação corrigida

Fotos de pessoas permanecem exatamente as originais: hashes de pixels verificados. Mapa xref108 estava invertido; corrigido com rotação de apresentação de 180°, sem regravar a imagem. Fachada xref71 mantém a orientação original de 90°. Páginas com duas imagens foram desdobradas, sem exclusão: VP agora 19 páginas, BOOK agora 25. Cada slide editorial usa uma única imagem original (logos e montagens já incorporadas na imagem original são preservados). Plantas permanecem vetoriais. Site remapeado para a nova paginação, preservando as chaves de favoritos existentes.


## Remoção final solicitada — slide 7 do Vila Parque

Usuário pediu remover somente a imagem do slide 7 da apresentação Vila Parque. Correspondia à imagem xref201 da fonte VP, em uma página sem texto editorial. A imagem foi excluída do gerador e o slide vazio foi eliminado; VP passa de 19 para 18 páginas, com paginação ajustada. BOOK continua com 25 páginas e seu PDF não foi modificado. Usar `python3 tools/redesenhar_pdfs.py --document VP` para atualizar apenas o empreendimento. Galeria e download do site atualizados, sem outras alterações de conteúdo.


## Correção confirmada do BOOK Mall & Office — slide 7

O usuário confirmou a opção 2: corrigir o próprio BOOK, não substituí-lo pelo Vila Parque. A foto de pessoas do slide 7 do BOOK (xref355 da fonte, página 5 original) foi retirada. Os títulos Vila Parque / Centro Comercial foram preservados como abertura de seção; BOOK continua com 25 páginas. O PDF Vila Parque de 18 páginas ficou byte a byte inalterado. Site e prévias usam versão `book-slide7-corrigido`.

A causa adicional de confusão era o arquivo ZIP do repositório, que incluía fontes antigas. Download do site passou a `downloads/Vila-Parque-Site.zip`, gerado por `tools/empacotar_site.py`: apenas arquivos usados no site e exatamente dois PDFs atuais. Recriar esse pacote antes de commitar próximas alterações. Originais-fonte continuam no GitHub para reprodução, mas fora do pacote de download do site.
