from pathlib import Path
import subprocess,json,hashlib
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;F='/Users/USER/.local/bin/ffmpeg';shots=json.loads((R/'scene-edl.json').read_text())
for n in [3,10,11,12,13,14]:
 for label,sec in [('head',0),('mid',(shots[n]['timeline_out_frame_exclusive']-shots[n]['timeline_in_frame'])/60),('tail',(shots[n]['timeline_out_frame_exclusive']-shots[n]['timeline_in_frame'])/30-.034)]:
  out=R/'qa'/f'shot-{n:02}-{label}.png'
  subprocess.run([F,'-v','error','-y','-ss',str(sec),'-i',str(R/'shots'/f'{n:02}.mp4'),'-frames:v','1',str(out)],check=True)
files=sorted((R/'qa').glob('shot-*.png'))
for page in range(3):
 canvas=Image.new('RGB',(1080,1320),'#ddd');d=ImageDraw.Draw(canvas)
 for j,p in enumerate(files[page*6:(page+1)*6]):
  x=j%3*360;y=j//3*660;im=Image.open(p).resize((360,640));canvas.paste(im,(x,y));d.text((x+5,y+642),p.stem,fill='black')
 canvas.save(R/'qa'/f'changed-shots-phone-{page+1}.jpg')
for s in shots:
 s['source_fps']=30 if s['source_id'].startswith('V') else None
 s['timeline_in_frame']*=2;s['timeline_out_frame_exclusive']*=2;s['fps']=60
 if s['source_id']=='MOTION':s['original_source']=str(R.parents[1]/'01-原始素材/照片/P08.jpg');s['component_manifest']='component-manifest.json'
(R/'scene-edl-60fps.json').write_text(json.dumps(shots,ensure_ascii=False,indent=2))
a=(R/'voice-timeline.wav').read_bytes();b=(R.parent/'voice-timeline.wav').read_bytes();print('voice_wav_exact',a==b,hashlib.sha256(a).hexdigest())
