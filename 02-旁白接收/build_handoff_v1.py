# coding: utf-8
from pathlib import Path
import json,hashlib,wave,subprocess,copy
p=Path(__file__).resolve().parent
m=json.loads((p/'录音接收清单-v1.json').read_text())
ff='/Users/USER/.local/bin/ffmpeg'
info=[]
for f in m['files']:
 path=p/'audio'/f'{f["id"]}-original.wav'
 with wave.open(str(path)) as w: d=dict(duration=w.getnframes()/w.getframerate(),sample_rate=w.getframerate(),channels=w.getnchannels(),sample_width=w.getsampwidth())
 info.append(dict(id=f['id'],source=f['archived'],source_sha256=f['sha256'],audio=str(path),audio_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),**d))
ed=[];pos=0
for n,end in [('A03',8.5),('A01',18.2)]:
 ed.append(dict(id=n,audio=str(p/'audio'/f'{n}-original.wav'),source_video=next(f['archived'] for f in m['files'] if f['id']==n),source_in=0,source_out=end,voice_in=pos,voice_out=pos+end,speed=1,reason='完整有效表达，仅收检测到持续低电平的尾空白并留约0.28—0.33秒余量；头部早期瞬态不确定，保留'))
 pos+=end
edl=dict(content_id=m['content_id'],coordinate_system='seconds from original audio/video, voice timeline is compact audio only',duration=pos,segments=ed,unused=[dict(id='A02',source_in=0,source_out=info[1]['duration'],enabled=False,reason='ASR为未完成起句“全场我觉得我……”；与A01开头主题重复，暂不入master，原音完整保留，待听核')],deleted=[dict(id='A03',source_in=8.5,source_out=info[2]['duration']),dict(id='A01',source_in=18.2,source_out=info[0]['duration'])],full_film_timeline='由04完整粗剪再插现场留白，不将compact voice时间冒称整片时间')
(p/'保守EDL-v1.json').write_text(json.dumps(edl,ensure_ascii=False,indent=2))
texts={'A01':['全场我个人觉得最有意思可能就是这场考试','整场考试是闭卷的 然后也不能用手机','最后我是考了92分','感觉还可以吧','如果说让你来考的话 你能考几分呢','大家可以来试试看'],'A02':['全场我觉得我……'],'A03':['今天来杭州西湖区这里参加观猹大会顺便还考了一场','AI能力的考试']}
records=[];cues=[]
for n in ['A01','A02','A03']:
 ar=json.loads((p/'asr'/f'{n}.json').read_text())['transcription'];assert len(ar)==len(texts[n])
 for a,txt in zip(ar,texts[n]):
  r=dict(id=n,source_in=a['offsets']['from']/1000,source_out=a['offsets']['to']/1000,raw=a['text'],text=txt,word_alignment=False)
  records.append(r)
  if n=='A02':continue
  s=next(x for x in ed if x['id']==n);a0=max(r['source_in'],s['source_in']);b0=min(r['source_out'],s['source_out']);assert a0<b0
  # Split only a complete phrase at a recorded ASR boundary; no letter/word slicing.
  parts=[(a0,b0,txt)]
  if n=='A03' and a0==0:parts=[(a0,3.9,'今天来杭州西湖区这里参加观猹大会'),(3.9,b0,'顺便还考了一场')]
  if n=='A01' and a0==0:parts=[(a0,2.6,'全场我个人觉得最有意思'),(2.6,b0,'可能就是这场考试')]
  if n=='A01' and a0==4.12:parts=[(a0,6.0,'整场考试是闭卷的'),(6.0,b0,'然后也不能用手机')]
  if n=='A01' and a0==13.0:parts=[(a0,14.5,'如果说让你来考的话'),(14.5,b0,'你能考几分呢')]
  for st,en,t in parts:cues.append(dict(id=n,source_in=st,source_out=en,voice_in=s['voice_in']+st-s['source_in'],voice_out=s['voice_in']+en-s['source_in'],text=t))
cues.sort(key=lambda x:x['voice_in'])
def ts(t):
 v=round(t*1000);return f'{v//3600000:02}:{v//60000%60:02}:{v//1000%60:02},{v%1000:03}'
(p/'字幕草稿-v1.srt').write_text('\n\n'.join(f'{i}\n{ts(c["voice_in"])} --> {ts(c["voice_out"])}\n{c["text"]}' for i,c in enumerate(cues,1))+'\n')
(p/'逐字稿与字幕映射-v1.json').write_text(json.dumps(dict(records=records,cues=cues,alignment='本地Whisper base片段级；人工按完整语义分段的边界为候选，未逐词精对齐',corrections=[dict(raw='观察大会',text='观猹大会',basis='用户指定活动及现场已核招牌'),dict(raw='必卷',text='闭卷',basis='用户明确考试闭卷'),dict(raw='这有意思',text='最有意思',basis='句法上下文，待听核'),dict(raw='西古区',text='西湖区',basis='杭州地名/语音候选，未直接听核')]),ensure_ascii=False,indent=2))
args=[];fs=[]
for k,s in enumerate(ed):args+=['-i',s['audio']];fs.append(f'[{k}:a]atrim=start={s["source_in"]}:end={s["source_out"]},asetpts=PTS-STARTPTS[a{k}]')
fs.append('[a0][a1]concat=n=2:v=0:a=1[out]')
cmd=[ff,'-v','error','-n',*args,'-filter_complex',';'.join(fs),'-map','[out]','-ar','48000','-ac','1','-c:a','pcm_s24le',str(p/'audio/voice-master-v1.wav')];subprocess.run(cmd,check=True)
(p/'audio/master-parameters-v1.json').write_text(json.dumps(dict(command=cmd,speed=1,gain_db=0,denoise=False,limiter=False,role='voice only no BGM'),ensure_ascii=False,indent=2))
with (p/'audio/loudness-v1.log').open('w') as h:subprocess.run([ff,'-hide_banner','-i',str(p/'audio/voice-master-v1.wav'),'-af','ebur128=peak=true','-f','null','-'],stdout=subprocess.DEVNULL,stderr=h,check=True)
with wave.open(str(p/'audio/voice-master-v1.wav')) as w:assert abs(w.getnframes()/w.getframerate()-pos)<1/48000
for a,b in zip(cues,cues[1:]):assert a['voice_out']<=b['voice_in']+.001
(p/'audio-inventory-v1.json').write_text(json.dumps(info,ensure_ascii=False,indent=2))
print(json.dumps(dict(raw_total=sum(x['duration'] for x in info),voice_duration=pos,order=['A03','A01'],unused='A02',cues=len(cues),audio=info),ensure_ascii=False,indent=2))
