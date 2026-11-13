from pathlib import Path
import subprocess,json,hashlib,shutil,os,sys
R=Path(__file__).resolve().parent
C=R.parent
video=C/'04-现场粗剪/v2/watcha-full-v2.mp4'
music=C/'06-发布准备/bgm/Carefree-Kevin-MacLeod.mp3'
out=R/'watcha-full-v3-bgm.mp4'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(video)=='6c3f10b0e98eba9b8db239dfc6c8ab4b78693ee19d7cfcb9533c23474a5ed0a8'
assert sha(music)=='8433b770a630d9b1594fd484442c677907ece899a4d149954cd2e74fd733e311'
def run(args,name):
 env=os.environ.copy()
 if args[0]=='ffprobe':
  runtime=Path('/Volumes/EXTERNAL/自媒体/Fred复刻测试-20261016/7694088597179239690/source-snapshot/FredTalk-1.5-3D/camera/node_modules/@remotion/compositor-darwin-arm64')
  args=[str(runtime/'ffprobe')]+args[1:];env['DYLD_LIBRARY_PATH']=str(runtime)
 r=subprocess.run(args,capture_output=True,text=True,env=env)
 (R/(name+'.log')).write_text(r.stderr)
 if r.returncode: raise RuntimeError(r.stderr[-3000:])
 return r.stdout,r.stderr
def measure(path,filters,name):
 if '--verify-existing' in sys.argv and (R/(name+'.log')).exists():
  log=(R/(name+'.log')).read_text()
  return json.loads(log[log.rfind('{'):log.rfind('}')+1])
 _,log=run(['ffmpeg','-hide_banner','-i',str(path),'-vn','-af',filters+',loudnorm=I=-25:TP=-2:LRA=11:print_format=json','-f','null','-'],name)
 return json.loads(log[log.rfind('{'):log.rfind('}')+1])
ms=measure(music,'atrim=0:45.7,asetpts=PTS-STARTPTS','music-source-measure')
voice=measure(video,'atrim=0:45.7','voice-source-measure')
low=-34-float(ms['input_i']);high=-25-float(ms['input_i'])
# Fade up only after narration ends; fade down before narration resumes.
db=f"if(lt(t,8.5),{low},if(lt(t,9.1),{low}+({high-low})*(t-8.5)/0.6,if(lt(t,26.9),{high},if(lt(t,27.5),{high}-({high-low})*(t-26.9)/0.6,{low}))))"
bgm=f"atrim=0:45.7,asetpts=PTS-STARTPTS,aresample=48000,volume='pow(10,({db})/20)':eval=frame,afade=t=in:st=0:d=0.4,afade=t=out:st=44.5:d=1.2"
# Duplicate mono narration at unity into stereo; no normalization or gain change.
graph=f"[0:a]atrim=0:45.7,pan=stereo|c0=c0|c1=c0[voice];[1:a]{bgm}[bgm];[voice][bgm]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,atrim=0:45.7[mix]"
(R/'filter.txt').write_text(graph)
args=['ffmpeg','-hide_banner','-n','-i',str(video),'-i',str(music),'-filter_complex_script',str(R/'filter.txt'),'-map','0:v:0','-map','[mix]','-c:v','copy','-c:a','aac','-b:a','192k','-ar','48000','-t','45.7','-movflags','+faststart',str(out)]
(R/'command.json').write_text(json.dumps(args,indent=2))
if '--verify-existing' not in sys.argv: run(args,'mix')
final=measure(out,'atrim=0:45.7','final-audio-measure')
assert float(final['input_tp'])<0,final
mid=measure(out,'atrim=10:26,asetpts=PTS-STARTPTS','middle-audio-measure')
def packets(path,name):
 data,_=run(['ffprobe','-v','error','-select_streams','v:0','-show_packets','-show_data_hash','sha256','-show_entries','packet=pts,dts,duration,size,data_hash','-of','json',str(path)],name)
 parsed=json.loads(data);(R/(name+'.json')).write_text(data);return parsed
a=packets(video,'video-packets-before');b=packets(out,'video-packets-after');assert a==b
probe,_=run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)],'probe')
(R/'probe.json').write_text(probe)
shutil.copy2(C/'06-发布准备/bgm/source-license.json',R/'source-license.json')
manifest={'content_id':C.name,'owner':'04','version':'v3-bgm','status':'READY_FOR_PMO_USER_PREVIEW','video_input':str(video),'video_input_sha256':sha(video),'music_input':str(music),'music_sha256':sha(music),'output':str(out),'output_sha256':sha(out),'duration':45.7,'music_source_range':[0,45.7],'gain_db':{'narration':low,'middle':high},'envelope':{'low':[0,8.5],'rise':[8.5,9.1],'high':[9.1,26.9],'fall':[26.9,27.5],'low_end':[27.5,45.7],'fade_in':[0,0.4],'fade_out':[44.5,45.7]},'voice':'Original decoded mono samples duplicated into stereo at unity; no gain, speed, denoise or time change; final AAC re-encoded','measurement':{'music_source':ms,'voice_source':voice,'final_encoded_audio':final,'middle_10_26':mid},'video_packets_identical':True,'packet_count':len(a['packets']),'video_packet_fields':['pts','dts','duration','size','data_hash'],'direct_listening':'UNKNOWN','continuous_AV':'NOT_PERFORMED','covers':'Existing v3 unchanged; outside this task','target_model_effort':'Astra medium','actual_model_effort':'UNKNOWN','rules':['AGENTS-v4','workflow-v3','production-v5','rework-v2','ROUTING-2026-10-24-v5','TOKEN-BUDGET-2026-10-24-v1'],'permission':'Task and formal release receipt in this directory; user request overrides prior no-BGM','license':'source-license.json','publishing':'NOT_PERFORMED','temporary_files':'None; all files in this directory are task inputs, source, output or retained verification evidence'}
(R/'Manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print(json.dumps(manifest,ensure_ascii=False,indent=2))
