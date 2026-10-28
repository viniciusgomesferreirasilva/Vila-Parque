"""Redesign both presentations from original text, images and vector plans."""
from pathlib import Path
from io import BytesIO
from collections import Counter
import json,re,html,hashlib,argparse
import fitz
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader

ROOT=Path(__file__).resolve().parent.parent
fitz.TOOLS.mupdf_display_errors(False)
fitz.TOOLS.mupdf_display_warnings(False)
for name,file in [('Sans','DejaVuSans.ttf'),('Serif','DejaVuSerif.ttf')]:
 pdfmetrics.registerFont(TTFont(name,'/usr/share/fonts/truetype/dejavu/'+file))
W,H=1280,800
GREEN='#253f34';CREAM='#f5f3ec';GOLD='#c7ac73';MUTED='#626d62'
EXCLUDE={5,7,9,34,36,38,44,81,462}
parser=argparse.ArgumentParser()
parser.add_argument('--document',choices=['VP','BOOK','ALL'],default='ALL')
args=parser.parse_args()
audit=[]
if args.document!='ALL' and (ROOT/'assets/auditoria-redesign.json').exists():
 audit=[r for r in json.loads((ROOT/'assets/auditoria-redesign.json').read_text()) if r['document']!=args.document]
def color(c,value):c.setFillColor(value)
def text(c,value,x,y,size=14,font='Sans',fill=GREEN):
 color(c,fill);c.setFont(font,size);c.drawString(x,y,value)
def paragraph(c,value,x,top,width,height,size=18,font='Sans',fill=GREEN):
 value=html.escape(value).replace('\uf075','•').replace('\n','<br/>')
 for s in range(size,10,-1):
  p=Paragraph(value,ParagraphStyle('p',fontName=font,fontSize=s,leading=s*1.55,textColor=fill,spaceAfter=8))
  pw,ph=p.wrap(width,height)
  if ph<=height:break
 if ph>height:raise RuntimeError('Text does not fit')
 p.drawOn(c,x,top-ph)
 return ph

def base(c,index,total,section,dark=False):
 bg=GREEN if dark else CREAM
 color(c,bg);c.rect(0,0,W,H,fill=1,stroke=0)
 text(c,'VILA PARQUE',48,752,15,fill=CREAM if dark else GREEN)
 text(c,section,720,752,10,fill=GOLD if dark else MUTED)
 c.setStrokeColor(GOLD);c.line(48,731,1232,731)
 text(c,'VILA PARQUE  /  '+section,48,28,9,fill=GOLD if dark else MUTED)
 text(c,f'{index+1:02d} / {total:02d}',1160,28,10,fill=GOLD if dark else MUTED)

def blocks(page):
 return sorted([b for b in page.get_text('blocks') if b[6]==0 and b[4].strip()],key=lambda b:(round(b[1]/8),b[0]))

def image(c,doc,xref,rect):
 info=doc.extract_image(xref)
 x,y,w,h=rect
 if xref==71:
  c.saveState();c.translate(x+w,y);c.rotate(90)
  c.drawImage(ImageReader(BytesIO(info['image'])),0,0,width=h,height=w,preserveAspectRatio=True,anchor='c',mask='auto')
  c.restoreState()
 elif xref==108:
  c.saveState();c.translate(x+w,y+h);c.rotate(180)
  c.drawImage(ImageReader(BytesIO(info['image'])),0,0,width=w,height=h,preserveAspectRatio=True,anchor='c',mask='auto')
  c.restoreState()
 else:
  c.drawImage(ImageReader(BytesIO(info['image'])),x,y,width=w,height=h,preserveAspectRatio=True,anchor='c',mask='auto')
 return {'xref':xref,'source_bytes_sha256':hashlib.sha256(info['image']).hexdigest(),'source_pixel_digest':fitz.Pixmap(doc,xref).digest.hex()}

def vp():
 src=fitz.open(ROOT/'assets/apresentacao-vila-parque.pdf')
 buf=BytesIO();c=canvas.Canvas(buf,pagesize=(W,H));records=[]
 work=[]
 for source_i,source_page in enumerate(src):
  seen=set()
  for entry in source_page.get_images():
   x=entry[0]
   if x not in EXCLUDE and x != 201 and x not in seen and src.extract_image(x)['ext']=='jpeg':
    work.append((source_i,x));seen.add(x)
 for output_i,(i,selected_xref) in enumerate(work):
  page=src[i]
  dark=i in [0,5,10,16]
  base(c,output_i,len(work),'O EMPREENDIMENTO',dark)
  bs=blocks(page)
  head=next((b for b in bs if 'PROJETOS IMPLANTADOS' in b[4]),bs[0] if bs else None)
  heading=head[4].strip() if head else ''
  body='\n'.join(b[4].strip() for b in bs if b is not head)
  photos=[selected_xref]
  used=[]
  if i==0:
   paragraph(c,heading,55,657,490,220,42,'Serif',CREAM)
   used.append(image(c,src,photos[0],(585,135,640,480)))
   text(c,'01',55,120,90,'Serif',GOLD)
  elif not bs:
   if len(photos)!=1:raise RuntimeError('Unexpected image-only page')
   used.append(image(c,src,photos[0],(50,85,1180,620)))
  elif len(body)>120:
   paragraph(c,heading,50,680,425,180,34,'Serif',CREAM if dark else GREEN)
   paragraph(c,body,50,477,425,370,18,fill=CREAM if dark else GREEN)
   colw=690/len(photos)
   for j,x in enumerate(photos):used.append(image(c,src,x,(520+j*colw,90,colw-16,605)))
  else:
   paragraph(c,heading,50,682,1170,100,36,'Serif',CREAM if dark else GREEN)
   if body:paragraph(c,body,52,590,1170,100,23,fill=CREAM if dark else GREEN)
   top=470 if body else 560
   for j,x in enumerate(photos):
    cw=1180/len(photos);used.append(image(c,src,x,(50+j*cw,85,cw-18,top-55)))
  records.append({'document':'VP','page':output_i+1,'source_page':i+1,'photos':used})
  c.showPage()
 c.save();result=fitz.open(stream=buf.getvalue(),filetype='pdf')
 # Preserve the original Group RZK logo, including its transparency mask, on the cover.
 logo=fitz.Pixmap(src,44)
 entry=next(x for x in src[0].get_images() if x[0]==44)
 if entry[1]:
  if logo.alpha:logo=fitz.Pixmap(logo,0)
  logo=fitz.Pixmap(logo,fitz.Pixmap(src,entry[1]))
 result[0].insert_image(fitz.Rect(55,355,350,417),pixmap=logo,keep_proportion=True)
 return src,result,records

def technical_region(page):
 rects=[]
 for info in page.get_image_info():
  r=fitz.Rect(info['bbox'])
  if r.y0>=160 and r.width>=100 and r.height>=100:rects.append(r)
 for b in blocks(page):
  if b[1]>=260:rects.append(fitz.Rect(b[:4]))
 if not rects:raise RuntimeError('No technical drawing found')
 r=rects[0]
 for other in rects[1:]:r|=other
 r=fitz.Rect(r.x0-10,r.y0-10,r.x1+10,r.y1+10)&page.rect
 return r

def book():
 src=fitz.open(ROOT/'assets/book-mall-office-original.pdf')
 buf=BytesIO();c=canvas.Canvas(buf,pagesize=(W,H));records=[];regions={}
 tech=set(range(5,13))|set(range(14,22))
 work=[(i,part) for i in range(len(src)) for part in range(2 if i in [1,3] else 1)]
 for output_i,(i,part) in enumerate(work):
  page=src[i]
  dark=i in [0,4,13,22]
  base(c,output_i,len(work),'MALL & OFFICE',dark)
  bs=blocks(page);used=[]
  if i in tech:
   region=technical_region(page);regions[output_i]=(i,region)
   outside=[b for b in bs if not region.contains(fitz.Rect(b[:4]))]
   title=outside[0][4].strip() if outside else ('IMPLANTAÇÃO' if i in [5,14,15] else '')
   paragraph(c,title,50,680,245,165,29,'Serif')
   rest='\n'.join(b[4].strip() for b in outside[1:])
   if rest:paragraph(c,rest,50,480,235,355,19)
   color(c,'#ffffff');c.roundRect(325,80,907,620,8,fill=1,stroke=0)
   text(c,'PLANTA ORIGINAL',348,104,9,fill=MUTED)
  elif i in [0,22]:
   heading=bs[0][4].strip() if bs else 'VILA PARQUE'
   paragraph(c,heading,50,670,470,200,42,'Serif',CREAM)
   if len(bs)>1:paragraph(c,'\n'.join(b[4].strip() for b in bs[1:]),50,430,455,120,19,fill=GOLD)
   used.append(image(c,src,13,(560,160,670,474)))
   text(c,'CENTRO COMERCIAL  /  OFFICE CENTER',50,112,12,fill=GOLD)
  elif i==1:
   paragraph(c,bs[0][4].strip(),50,680,460,100,36,'Serif')
   paragraph(c,'\n'.join(b[4].strip() for b in bs[1:]),50,555,480,455,17)
   used.append(image(c,src,108 if part==0 else 71,(570,110,660,570)))
  elif i==2:
   heading=next(b for b in bs if 'FICHA TÉCNICA' in b[4])
   paragraph(c,heading[4].strip(),50,680,650,100,36,'Serif')
   paragraph(c,'\n'.join(b[4].strip() for b in bs if b is not heading),50,555,650,475,17)
   used.append(image(c,src,145,(805,95,360,570)))
  elif i==3:
   title=next(b for b in bs if 'LAZER E COMPRAS' in b[4])
   paragraph(c,title[4].strip(),50,680,1170,100,35,'Serif')
   rest='\n'.join(b[4].strip() for b in bs if b is not title)
   paragraph(c,rest,50,570,400,420,21)
   used.append(image(c,src,235 if part==0 else 255,(495,100,735,495)))
  elif i in [4,13]:
   name='CENTRO COMERCIAL' if i==4 else 'OFFICE CENTER'
   if i==4:
    # Keep the chapter titles, removing only the photo requested on output slide 7.
    paragraph(c,'VILA PARQUE',200,555,880,150,60,'Serif',CREAM)
    paragraph(c,name,200,370,880,120,30,fill=GOLD)
   else:
    paragraph(c,'VILA PARQUE',50,650,420,110,42,'Serif',CREAM)
    paragraph(c,name,50,510,420,140,29,fill=GOLD)
    used.append(image(c,src,1158,(520,100,710,580)))
  records.append({'document':'BOOK','page':output_i+1,'source_page':i+1,'photos':used,'vector_plan':i in tech})
  c.showPage()
 c.save();result=fitz.open(stream=buf.getvalue(),filetype='pdf')
 for out_i,(src_i,r) in regions.items():result[out_i].show_pdf_page(fitz.Rect(343,90,1214,680),src,src_i,clip=r,keep_proportion=True)
 # Original image 71 is stored sideways; reproduce its source orientation without recompression.
 # Its bytes remain intact in the file; all other image placement also preserves aspect ratio.
 return src,result,records

def words(s):return Counter(re.findall(r'\w+',s.replace('\uf075',''),re.UNICODE))
for label,fn,outname in [('VP',vp,'vila-parque-empreendimento-redesenhado.pdf'),('BOOK',book,'vila-parque-mall-office-redesenhado.pdf')]:
 if args.document not in ['ALL',label]:continue
 source,result,records=fn()
 result.set_metadata({'title':'Vila Parque | '+('O empreendimento' if label=='VP' else 'Mall & Office'),'author':'Vila Parque','subject':'Nova diagramação com textos, fotografias e plantas originais'})
 out=ROOT/'assets'/outname;result.save(out,garbage=4,deflate=True);result.close()
 check=fitz.open(out)
 for i,record in enumerate(records):
  assert len(record['photos'])<=1
  missing=words(source[record['source_page']-1].get_text())-words(check[i].get_text())
  if missing:raise RuntimeError(f'{label} page {i+1} missing words: {missing}')
  digests={im['digest'].hex() for im in check[i].get_image_info(hashes=True)}
  for photo in record['photos']:
   assert photo['source_pixel_digest'] in digests,(label,i,photo['xref'])
  record['all_source_text_tokens_preserved']=True
  audit.append(record)
 preview_folder=ROOT/'assets/apresentacoes'/('empreendimento' if label=='VP' else 'mall-office')
 preview_folder.mkdir(parents=True,exist_ok=True)
 for old in preview_folder.glob('pagina-*.jpg'):old.unlink()
 for i,page in enumerate(check):
  pix=page.get_pixmap(matrix=fitz.Matrix(.9,.9),alpha=False)
  Image.frombytes('RGB',(pix.width,pix.height),pix.samples).save(preview_folder/f'pagina-{i+1:02d}.jpg',quality=88)
 for i in ([0,1,11,15] if label=='VP' else [0,2,5,14,16]):
  check[i].get_pixmap(matrix=fitz.Matrix(.8,.8),alpha=False).save(f'/tmp/{label}-novo-{i+1}.png')
 print(f'{outname}: {len(check)} páginas, textos e fotos conferidos.')
(ROOT/'assets/auditoria-redesign.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
