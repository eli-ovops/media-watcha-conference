from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import subprocess,json,hashlib,shutil
R=Path(__file__).resolve().parent;G=Path('/Users/USER/.codex/generated_images/01a11a6f-49ef-7653-934a-4312979fd4e7');F='/Users/USER/.local/bin/ffmpeg';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=[('3x4',1080,1440,'exec-4b24fabe-db0c-4c37-ab59-d3e89bd4e9d8.png'),('9x16',1080,1920,'exec-33ee4a66-ed78-435e-a7b9-06899c8e69fe.png'),('16x9',1920,1080,'exec-9a8b71e7-eaa3-4ec9-bb74-dfb33cbc0c56.png'),('4x3',1440,1080,'exec-2acc0fb6-9159-4675-bd27-90dc2e522e79.png')]
records=[];sheet=Image.new('RGB',(900,750),'#ddd');d=ImageDraw.Draw(sheet)
for i,(ratio,w,h,f) in enumerate(files):
 src=G/f;im=Image.open(src).convert('RGB');old=im.size;shutil.copy2(src,R/'covers'/f'source-generated-{ratio}-v2.png')
 im=ImageOps.contain(im,(w,h),Image.Resampling.LANCZOS);canvas=Image.new('RGB',(w,h),'white');canvas.paste(im,((w-im.width)//2,(h-im.height)//2))
 out=R/'covers'/f'cover-{ratio}-{w}x{h}-v2.png';canvas.save(out)
 thumb=ImageOps.contain(canvas,(420,660));x=i%2*450;y=i//2*375;thumb=ImageOps.contain(canvas,(420,335));sheet.paste(thumb,(x+(450-thumb.width)//2,y+25));d.text((x+12,y+5),ratio+' '+str((w,h)),fill='black')
 records.append({'file':str(out),'sha256':sha(out),'size':[w,h],'original_generated_file':str(src),'original_size':old,'method':'independent built-in generation; proportional Lanczos normalization with white padding, no crop/stretch','main_text':'AI考试 / 92分 / 观猹大会','approval':'PENDING'})
(R/'covers/cover-manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2));sheet.save(R/'covers/phone-contact.png')
for sec in [12,21.25,21.75,22.35,23,26,29,32,37,42]:
 subprocess.run([F,'-v','error','-y','-ss',str(sec),'-i',str(R/'watcha-full-v2.mp4'),'-frames:v','1',str(R/'qa'/f'native-{sec}.png')],check=True)
phones=Image.new('RGB',(1080,1320),'#ddd');d=ImageDraw.Draw(phones)
for i,sec in enumerate([12,23,26,29,32,37]):
 im=Image.open(R/'qa'/f'native-{sec}.png').resize((360,640));x=i%3*360;y=i//3*660;phones.paste(im,(x,y));d.text((x+5,y+642),str(sec)+'s',fill='black')
phones.save(R/'qa/final-phone-contact.png')
# Hash demuxed compressed AAC payloads without changing audio.
for video,name in [(R.parent/'watcha-rough-v1.mp4','rough'),(R/'watcha-full-v2.mp4','full')]:
 result=subprocess.check_output([F,'-v','error','-i',str(video),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).decode().strip();records.append({'audio':name,'packet_hash':result})
(R/'qa/audio-copy-proof.json').write_text(json.dumps(records[-2:],indent=2));assert records[-1]['packet_hash']==records[-2]['packet_hash']
print('VIDEO_SHA256',sha(R/'watcha-full-v2.mp4'));print('COVERS',[(a,b,c) for a,b,c,_ in files]);print('AAC_IDENTICAL')
