from pathlib import Path
import json,hashlib,wave
R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
master=R.parent/'02-旁白接收/audio/voice-master-v1.wav'
with wave.open(str(master),'rb') as w:p=w.getparams();a=w.readframes(w.getnframes())
with wave.open(str(R/'voice-timeline.wav'),'rb') as w:b=w.readframes(w.getnframes())
c=int(8.5*p.framerate)*p.sampwidth*p.nchannels;gap=19*p.framerate*p.sampwidth*p.nchannels
assert b[:c]==a[:c] and b[c+gap:]==a[c:] and not any(b[c:c+gap])
(R/'play.html').write_text('''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>观猹大会｜完整粗剪 v1</title><style>body{background:#181818;color:white;font:16px system-ui;margin:24px}video{display:block;height:78vh;max-width:100%;margin:auto}p{text-align:center}</style><video controls playsinline preload="metadata" src="watcha-rough-v1.mp4"></video><p>完整粗剪 v1 · 45.7 秒 · 无 BGM<br>8.5—27.5 秒有意静音。直接听音及连续声画检查待完成。</p>''')
outputs=['watcha-rough-v1.mp4','build.py','check.py','scene-edl.json','voice-edl.json','voice-timeline.wav','subtitles-v1.srt','titles.ass','labels.json','play.html']
m={'content_id':'watcha-conference-20261024','version':'rough-v1','owner':'04','thread_id':'01a11a6f-49ef-7653-934a-4312979fd4e7','date':'2026-10-24','status':'INTERNAL_ROUGH_READY_FOR_PMO_REVIEW','duration_seconds':45.7,'frames':1371,'preview':{'width':720,'height':1280,'fps':30},'formal_target':{'width':1080,'height':1920,'fps':60,'status':'NOT_RENDERED'},'model_target':'Astra medium','actual_model_effort':'UNKNOWN','rules':['ELI-MEDIA-AGENTS-20261024-v4','CODEX-MEDIA-20261024-v3','ELI-PRODUCTION-20261024-v5','ELI-REWORK-20261024-v2','ROUTING-2026-10-24-v5','TOKEN-BUDGET-2026-10-24-v1'],'outputs':[{'path':str(R/f),'sha256':sha(R/f)} for f in outputs],'sources':'scene-edl.json and voice-edl.json','checks':{'full_decode':'PASS; qa/decode.log empty','spec':'PASS; qa/probe.json','visual_sampling':'46 samples at 1 fps; both sec-contact sheets viewed','all_cut_boundaries':'15 cuts x 3 frames; both seam-contact sheets viewed; no blank/flash frames in sampled boundaries','photo_details':'P08 Claude, P12 bag, P13 score prepared frames viewed at 720x1280; final sampled export inspected','score_privacy':'92 and 通过 retained; unrelated ticket identifier excluded by crop','master_pcm_preservation':'PASS; before/after inserted 19s silence byte-exact comparison','direct_listening':'UNKNOWN; existing 02 capability probe audio content omitted because you do not support audio input; LOCAL_BLOCKERS checked; no new supported entry','continuous_normal_speed_av':'NOT_PERFORMED','subtitle_word_alignment':'CANDIDATE; 02 timings remapped +19 seconds after original 8.5s; not force-aligned or heard','user_approval':'PENDING','PMO_review':'PENDING'},'limits':['Internal rough cut only; no packaging or cover.','All现场 source audio muted; no BGM. 8.5-27.5 seconds intentionally silent.','First unverified district cue omitted; opening uses event label. 最有意思 remains 02 candidate pending listening.','Wide room/board compositions retained in full-width letterbox for context; no decorative components or false Fred attribution.','No fake exam-room footage; exam narration uses real venue cutaways and real score.','No user speaking-video visuals; V09 excluded.'],'production_record':{'implementation':'FFmpeg hard cuts, fixed captions, source-clock shot EDL; existing runtime only','render_passes':1,'rework_rounds':0,'next_improvement':'PMO first evaluate venue-to-exam cutaways and silent segment reading rhythm; listening owner must resolve candidate transcript and naturalness before final release.'}}
(R/'Manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
(R/'README.md').write_text('''# 观猹大会完整现场粗剪 v1

内部粗剪完成，待 PMO 审实际原件；不是最终包装版，也未放行发布。

- 播放：同目录 `watcha-rough-v1.mp4`；或浏览器打开 `play.html`。
- 45.7 秒，720×1280，30fps。正式目标仍为1080×1920/60fps。
- 0—8.5秒到场原声；8.5—20.5秒现场所见；20.5—27.5秒红黑榜与Claude布袋；27.5—45.7秒考试/92分/互动。
- 无BGM、现场原声全静音；中间19秒静音是当前要求，非音轨丢失。
- 原旁白原速0dB；插入静音前后PCM逐字节一致。未使用本人讲话视频画面。
- `scene-edl.json` / `voice-edl.json` 保存源时钟；`subtitles-v1.srt`是重新映射候选，首句区名未核故未上屏；活动和现场标签另见`labels.json`。
- 复现：使用现有Python（Pillow）运行 `build.py`。脚本复用同版本shots缓存；修改shot输入后须输出到新版本目录或更换对应shot文件名，不能盲用旧缓存。
- 技术：全片解码通过、1371帧；视觉：每秒46帧及15处切点各前/中/后三帧实看；关键照片原尺寸核过。没有做正常速度连续视听，不以采样冒充连续验收。
- 直接听音未完成：02入口返回不支持音频输入，LOCAL_BLOCKERS有对应记录。本版只供内部试看；口播自然度、最有意思候选和精确字词同步待可听音者验收。
- `Manifest.json`绑定本版SHA、来源及检查范围；`qa`保存原始检查输出和联系表。
''')
print(sha(R/'watcha-rough-v1.mp4'))
