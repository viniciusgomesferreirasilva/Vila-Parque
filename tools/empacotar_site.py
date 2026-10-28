"""Package the website with only the files it uses, including the two current PDFs."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import zipfile
ROOT=Path(__file__).resolve().parent.parent
class Files(HTMLParser):
 def __init__(self):super().__init__();self.paths={'index.html','styles.css','script.js','favicon.svg'}
 def handle_starttag(self,tag,attrs):
  for key,value in attrs:
   if key not in ('href','src','data-image') or not value:continue
   u=urlsplit(value)
   if not u.scheme and not u.netloc and u.path:self.paths.add(unquote(u.path))
files=Files();files.feed((ROOT/'index.html').read_text())
allowed={'assets/vila-parque-empreendimento-redesenhado.pdf','assets/vila-parque-mall-office-redesenhado.pdf'}
assert {p for p in files.paths if p.endswith('.pdf')}==allowed
out=ROOT/'downloads/Vila-Parque-Site.zip';out.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
 for name in sorted(files.paths):
  source=(ROOT/name).resolve()
  assert source.is_relative_to(ROOT) and source.is_file(),name
  z.write(source,'Vila-Parque/'+name)
 z.writestr('Vila-Parque/COMO-ABRIR.txt','Extraia a pasta e abra index.html. O pacote contém somente os dois PDFs atuais.\n')
with zipfile.ZipFile(out) as z:assert z.testzip() is None
print(f'Pacote limpo: {out}, {out.stat().st_size/1024/1024:.1f} MB, dois PDFs atuais.')
