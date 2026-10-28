"""Build a passive offline copy: HTML, CSS, images and the two current PDFs.
This reduces active content; it is not an antivirus certification.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import zipfile,re,hashlib,json
ROOT=Path(__file__).resolve().parent.parent
page=(ROOT/'index.html').read_text()
page=re.sub(r'<script\b[^>]*>.*?</script>','',page,flags=re.S|re.I)
page=re.sub(r'<dialog\b[^>]*>.*?</dialog>','',page,flags=re.S|re.I)
page=re.sub(r'<link\b[^>]*rel="icon"[^>]*>','',page)
page=re.sub(r'<button\b[^>]*id="menu"[^>]*>.*?</button>','',page,flags=re.S)
page=re.sub(r'<div class="plan-search">.*?</div>','',page,flags=re.S)
page=re.sub(r'<div class="plan-filters".*?</div>','',page,flags=re.S)
page=re.sub(r'<p id="plan-status".*?</p>','',page,flags=re.S)
page=re.sub(r'<button class="save-plan".*?</button>','',page,flags=re.S)
def photo(match):
 attrs,body=match.groups()
 src=re.search(r'data-image="([^"]+)"',attrs).group(1)
 return f'<a class="photo-open" href="{src}" target="_blank" rel="noopener">{body}</a>'
page=re.sub(r'<button\b([^>]*\bclass="[^"]*\bphoto-open\b[^"]*"[^>]*)>(.*?)</button>',photo,page,flags=re.S)
page=re.sub(r'\s+hidden(?=[\s>])','',page)
page=page.replace('</head>','<style>nav{display:flex!important}.photo-open{display:block}.plan-card[hidden]{display:block}@media(max-width:760px){header{height:auto;display:block;padding:20px}nav{position:static;flex-wrap:wrap;padding:20px 0;font-size:12px}}</style></head>')
page=page.replace('<main id="conteudo">','<main id="conteudo"><p style="padding:15px 7%;margin:0;background:#eaece2;font-size:13px">Versão de consulta offline. Clique nas imagens para ampliar. Busca e favoritos estão disponíveis no site online.</p>')
page=page.replace('href="downloads/', 'href="https://viniciusgomesferreirasilva.github.io/Vila-Parque/downloads/')
class Files(HTMLParser):
 def __init__(self):super().__init__();self.paths={'styles.css'}
 def handle_starttag(self,tag,attrs):
  assert tag not in ('script','iframe','object','embed','form'),tag
  for key,value in attrs:
   assert not key.lower().startswith('on'),key
   if key not in ('href','src','data-image') or not value:continue
   u=urlsplit(value);assert u.scheme.lower() not in ('javascript','vbscript'),value
   if not u.scheme and not u.netloc and u.path:self.paths.add(unquote(u.path))
files=Files();files.feed(page)
allowed={'assets/vila-parque-empreendimento-redesenhado.pdf','assets/vila-parque-mall-office-redesenhado.pdf'}
assert {p for p in files.paths if p.endswith('.pdf')}==allowed
out=ROOT/'downloads/Vila-Parque-Consulta.zip';out.parent.mkdir(exist_ok=True)
def add(z,name,data):
 info=zipfile.ZipInfo('Vila-Parque/'+name,date_time=(2026,1,1,0,0,0))
 info.compress_type=zipfile.ZIP_DEFLATED
 info.create_system=0
 z.writestr(info,data)
with zipfile.ZipFile(out,'w') as z:
 add(z,'index.html',page.encode())
 for name in sorted(files.paths):
  source=(ROOT/name).resolve()
  assert source.is_relative_to(ROOT) and source.is_file(),name
  assert source.suffix.lower() in ('.css','.jpg','.jpeg','.png','.pdf'),name
  add(z,name,source.read_bytes())
 add(z,'COMO-ABRIR.txt','Extraia a pasta e abra index.html. Cópia de consulta, sem scripts. Imagens e os dois PDFs estão incluídos. Busca e favoritos funcionam no site online. Esta versão não equivale a uma análise por antivírus.\n'.encode())
with zipfile.ZipFile(out) as z:
 assert z.testzip() is None
 assert not any(Path(n).suffix.lower() in ('.js','.exe','.msi','.bat','.cmd','.ps1','.py','.svg') for n in z.namelist())
manifest={'file':out.name,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size,'contents':'Passive offline HTML, CSS, original images and two current PDFs','antivirus_scan':'not_performed; no antivirus engine available'}
(ROOT/'downloads/verificacao-consulta.json').write_text(json.dumps(manifest,indent=2))
print(f'Pacote de consulta: {out.stat().st_size/1024/1024:.1f} MB; sem scripts, executáveis ou arquivos SVG.')
