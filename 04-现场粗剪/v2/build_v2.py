from pathlib import Path
import subprocess,json,hashlib,wave,re
from PIL import Image,ImageOps,ImageDraw
R=Path(__file__).resolve().parent; C=R.parent.parent; M=C/'01-原始素材'; A=C/'02-旁白接收'
FF='/Users/USER/.local/bin/ffmpeg'
FONT='/System/Library/AssetsV2/com_apple_MobileAsset_Font8/86ba2c91f017a3749571a82f2c6d890ac7ffb2fb.asset/AssetData'
for p in ['prepared','shots','qa']: (R/p).mkdir(exist_ok=True)
def run(args):
 with (R/'build.log').open('a') as f: subprocess.run([FF,'-hide_banner','-loglevel','warning','-y']+args,stdout=f,stderr=f,check=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
# Integer frames, original speed. Crops on EXIF-corrected photographs.
shots=[('V03',0,135,None,'到场'),('P03',0,60,(.27,0,.44,1),'入口'),('P05',0,60,None,'观猹员'),('V02',0,90,None,'会场'),('V01',0,45,None,'AI茶饮实验站'),('V07',135,75,None,'赛博换装'),('P02',0,60,None,'AI拼豆'),('V05',90,90,None,'现场交流'),('MOTION',0,120,None,'红黑榜聚焦'),('P12',0,90,None,'布袋'),('P05',0,78,None,'活动资料'),('P05',0,102,(0,.30,.58,.65),'胸牌与册子'),('V05',180,65,None,'现场过渡'),('P13',0,145,(90,1310,450,440),'成绩'),('V02',90,86,None,'互动收束'),('V08',150,70,None,'现场收束')]
assert sum(s[2] for s in shots)==1371
edl=[]; pos=0
for n,(sid,src,nf,crop,meaning) in enumerate(shots):
 source=M/('视频' if sid.startswith('V') else '照片')/(sid+'.mp4' if sid.startswith('V') else ('P13-exam-score.jpg' if sid=='P13' else sid+'.jpg'))
 if sid=='MOTION': source=R/'board-focus.mp4'
 item={'shot':n+1,'source_id':sid,'source':str(source),'sha256':sha(source),'source_in_frame':src if sid.startswith('V') else None,'source_out_frame_exclusive':src+nf if sid.startswith('V') else None,'timeline_in_frame':pos,'timeline_out_frame_exclusive':pos+nf,'fps':30,'purpose':meaning,'crop_after_exif':crop,'source_audio':'muted'};edl.append(item);pos+=nf
 out=R/'shots'/f'{n:02}.mp4'
 if out.exists():continue
 if sid=='MOTION':
  args=['-i',str(source)];vf='setsar=1'
 elif sid.startswith('P'):
  im=ImageOps.exif_transpose(Image.open(source)).convert('RGB')
  if crop:
   x,y,w,h=crop
   if w<=1 and h<=1:x,y,w,h=x*im.width,y*im.height,w*im.width,h*im.height
   im=im.crop((int(x),int(y),int(x+w),int(y+h)))
  # Photographs preserve relevant objects, large full-width; no decorative cards.
  canvas=Image.new('RGB',(1080,1920),'#151515' if sid!='P13' else 'white')
  im=ImageOps.contain(im,(1080,1800));canvas.paste(im,((1080-im.width)//2,(1920-im.height)//2))
  inp=R/'prepared'/f'{n:02}-{sid}.png';canvas.save(inp)
  args=['-loop','1','-framerate','60','-i',str(inp)];vf='setsar=1'
 else:
  args=['-ss',str(src/30),'-i',str(source)]
  # Wide hall: retain stage and attendees in a substantial central panorama.
  vf=('crop=404:720:200:0,scale=1080:1920,setsar=1' if src==0 else 'crop=404:720:40:0,scale=1080:1920,setsar=1') if sid=='V02' else 'scale=1080:1920,setsar=1'
 run(args+['-an','-vf',vf+',fps=60','-frames:v',str(nf*2),'-r','60','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',str(out)])
(R/'scene-edl.json').write_text(json.dumps(edl,ensure_ascii=False,indent=2))
# Insert exact digital silence into PCM master; no gain, resampling or speed change.
master=A/'audio/voice-master-v1.wav'
with wave.open(str(master),'rb') as w:params=w.getparams();pcm=w.readframes(w.getnframes())
cut=round(8.5*params.framerate)*params.nchannels*params.sampwidth
silence=bytes(19*params.framerate*params.nchannels*params.sampwidth)
with wave.open(str(R/'voice-timeline.wav'),'wb') as w:w.setparams(params);w.writeframes(pcm[:cut]+silence+pcm[cut:])
(R/'voice-edl.json').write_text(json.dumps({'master':str(master),'master_sha256':sha(master),'rate':1,'gain_db':0,'segments':[{'original':'A03','original_seconds':[0,8.5],'master_seconds':[0,8.5],'timeline_seconds':[0,8.5]},{'silence_seconds':[8.5,27.5]},{'original':'A01','original_seconds':[0,18.2],'master_seconds':[8.5,26.7],'timeline_seconds':[27.5,45.7]}],'pcm_segments_exact':True},ensure_ascii=False,indent=2))
def parse(t):h,m,s=map(float,t.replace(',','.').split(':'));return h*3600+m*60+s
def stamp(t,ass=False):
 ms=round(t*(100 if ass else 1000)); div=100 if ass else 1000;sec,ms=divmod(ms,div);mn,sec=divmod(sec,60);hr,mn=divmod(mn,60)
 return f'{hr}:{mn:02}:{sec:02}.{ms:02}' if ass else f'{hr:02}:{mn:02}:{sec:02},{ms:03}'
cues=[]
for block in (A/'字幕草稿-v1.1.srt').read_text().strip().split('\n\n'):
 lines=block.splitlines();start,end=map(parse,lines[1].split(' --> '));text=''.join(lines[2:])
 if start==0:continue # Unknown district: replace with activity label, never invent transcript.
 if start>=8.5:start+=19;end+=19
 cues.append((start,end,text))
(R/'subtitles-v1.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(a)} --> {stamp(b)}\n{t}' for i,(a,b,t) in enumerate(cues))+'\n')
labels=[(0,3.9,'观猹大会 · 杭州'),(8.5,11.5,'现场见闻'),(11.5,13,'AI茶饮实验站'),(13,15.5,'赛博换装'),(15.5,17.5,'AI拼豆'),(17.5,20.5,'现场交流'),(20.5,22.5,'现场产品红黑榜'),(22.5,24.5,'Claude真是“罪孽深重”啊'),(24.5,27.5,'大家的怨念，都做成周边了')]
(R/'labels.json').write_text(json.dumps(labels,ensure_ascii=False,indent=2))
ass='''[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,PingFang SC,68,&H00FFFFFF,&H00FFFFFF,&H00101010,&H00000000,0,0,0,0,100,100,0,0,1,3,1,2,60,60,255,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''
for a,b,t in cues+labels:ass+=f'Dialogue: 0,{stamp(a,True)},{stamp(b,True)},Default,,0,0,0,,{t}\n'
(R/'titles.ass').write_text(ass)
(R/'concat.txt').write_text(''.join(f"file 'shots/{n:02}.mp4'\n" for n in range(len(shots))))
if __import__('os').environ.get('PREPARE_ONLY')=='1': raise SystemExit('SHOTS_READY')
run(['-f','concat','-safe','0','-i',str(R/'concat.txt'),'-i',str(R.parent/'watcha-rough-v1.mp4'),'-vf',f"ass='{R/'titles.ass'}':fontsdir='{FONT}'",'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','19','-c:a','copy','-t','45.7','-movflags','+faststart',str(R/'watcha-full-v2.mp4')])
print('COMPLETE',str(R/'watcha-full-v2.mp4'))
