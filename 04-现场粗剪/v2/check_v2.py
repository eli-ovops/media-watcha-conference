from pathlib import Path
import subprocess,json,os,hashlib,wave
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent;F='/Users/USER/.local/bin/ffmpeg';V=R/'watcha-full-v2.mp4'
P='/Volumes/EXTERNAL/自媒体/Fred复刻测试-20261016/7694088597179239690/source-snapshot/FredTalk-1.5-3D/camera/node_modules/@remotion/compositor-darwin-arm64/ffprobe'
env=dict(os.environ,DYLD_LIBRARY_PATH=str(Path(P).parent))
probe=json.loads(subprocess.check_output([P,'-v','error','-show_streams','-show_format','-of','json',str(V)],env=env));(R/'qa/probe.json').write_text(json.dumps(probe,indent=2))
with (R/'qa/decode.log').open('w') as f:subprocess.run([F,'-v','error','-i',str(V),'-f','null','-'],stderr=f,check=True)
subprocess.run([F,'-v','error','-y','-i',str(V),'-vf','fps=1,scale=180:320','-q:v','3',str(R/'qa/sec-%02d.jpg')],check=True)
edl=json.loads((R/'scene-edl-60fps.json').read_text());frames=sorted({k for s in edl[1:] for k in [s['timeline_in_frame']-1,s['timeline_in_frame'],s['timeline_in_frame']+1]})
sel='+'.join(f'eq(n,{n})' for n in frames)
subprocess.run([F,'-v','error','-y','-i',str(V),'-vf',f"select='{sel}',scale=180:320",'-vsync','vfr','-q:v','3',str(R/'qa/seam-%02d.jpg')],check=True)
for prefix,labels in [('sec',list(range(46))),('seam',[round(x/60,3) for x in frames])]:
 files=sorted((R/'qa').glob(prefix+'-*.jpg'))
 for page in range((len(files)+23)//24):
  group=files[page*24:(page+1)*24];sheet=Image.new('RGB',(6*180,4*345),'#ddd');d=ImageDraw.Draw(sheet)
  for j,p in enumerate(group):x=(j%6)*180;y=(j//6)*345;sheet.paste(Image.open(p),(x,y));d.text((x+3,y+322),str(labels[page*24+j]),fill='black')
  sheet.save(R/'qa'/f'{prefix}-contact-{page+1}.jpg')
print('probe',[(s['codec_type'],s.get('duration'),s.get('nb_frames')) for s in probe['streams']]);print('decode_bytes',(R/'qa/decode.log').stat().st_size)
