# coding: utf-8
from pathlib import Path
import json,hashlib,copy
p=Path(__file__).resolve().parent
master=p/'audio/voice-master-v1.wav'
assert hashlib.sha256(master.read_bytes()).hexdigest()=='9ab8b943d5ba745cd7edc700342926ad507b871a221b1e7f58b97c0d4b466b52'
mapping=json.loads((p/'逐字稿与字幕映射-v1.json').read_text())
for r in mapping['records']+mapping['cues']:
 r['text']=r['text'].replace('杭州西湖区','杭州〔区名待核〕')
for c in mapping['corrections']:
 if c['raw']=='西古区': c.update(text='〔区名待核〕',basis='仅ASR西古区；无独立区名证据，不推断西湖区；不剪原声')
mapping['handoff_note']='地点占位仅供内部审校，未听核前不可将其称最终字幕；活动观猹大会按已核现场原字校正。'
(p/'逐字稿与字幕映射-v1.1.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2))
t=(p/'字幕草稿-v1.srt').read_text().replace('杭州西湖区','杭州〔区名待核〕');(p/'字幕草稿-v1.1.srt').write_text(t)
trans='# 实际逐字稿 v1.1\n\n完整本地ASR覆盖三条；本稿为校字稿，未直接听音。源段时码及原识别见逐字稿与字幕映射-v1.1.json。\n\n'
for n in ['A03','A01','A02']:
 rows=[r for r in mapping['records'] if r['id']==n]
 trans+='## '+n+('（未选，原音完整保留）' if n=='A02' else '（选用）')+'\n\n'+'。'.join(r['text'] for r in rows)+'。\n\n'
trans+='“〔区名待核〕”只是内部占位，不是说话内容；原ASR为西古区，未确认地名。最有意思仍为上下文校字候选。A02为未完成起句候选，保留原文件供听核。未补入书面稿Claude段或“通过”等未录词句。\n'
(p/'实际逐字稿-v1.1.md').write_text(trans)
doc=(p/'实际旁白与粗剪交接-v1.md').read_text().replace('交接 v1','交接 v1.1').replace('逐字稿与字幕映射-v1.json','逐字稿与字幕映射-v1.1.json').replace('杭州西湖区','杭州〔区名待核〕').replace('“西古区→西湖区”为语义/地名候选','“西古区”为未核区名；内部标〔区名待核〕，不推断西湖区；“这有意思→最有意思”为上下文候选')
# Replace historical gate paragraph only; preserve historical v1 as evidence.
doc=doc[:doc.index('实际02检查返回allowed=false')]+'''正式门禁已由PMO初始化并修正，证据见正式门禁初始化与释放回执-v1.json；本02本轮实际复核allowed=true。旧失败原件保留，不改检查器/共享状态。当前只完成本地接收与输入交接，PMO验收待定，04尚未放行。\n\n当前索引：实际逐字稿-v1.1.md、逐字稿与字幕映射-v1.1.json、字幕草稿-v1.1.srt；沿用保守EDL-v1.json、audio/voice-master-v1.wav及三条原音。音轨/26.7秒紧凑声音时钟未变，49—57秒整片示意只是供04选片，不是实际导出。Claude笑点以P08→P12及既定笑点文字、足够无旁白阅读间隔呈现。\n'''
(p/'实际旁白与粗剪交接-v1.1.md').write_text(doc)
r=json.loads((p/'02-旁白接收报告-v1.json').read_text());r.update(version='v1.1',status='LOCAL_HANDOFF_READY_PENDING_PMO_AND_DIRECT_LISTENING',gate=dict(allowed=True,stage='02',evidence='正式门禁初始化与释放回执-v1.json',owner_recheck=True,historical_error='v1保留，已由PMO纠正，非当前阻断'))
r['stage_complete']=False;r['transcription'].update(corrected='逐字稿与字幕映射-v1.1.json',draft_srt='字幕草稿-v1.1.srt',full_text='实际逐字稿-v1.1.md',pending_words=['最有意思','区名：ASR西古区，待核，不硬填西湖区'])
r['handoff']='实际旁白与粗剪交接-v1.1.md';r['report']=dict(send='PENDING',pmo_received='UNKNOWN',pmo_accepted='PENDING');r['audio']['reused_master_sha256']=hashlib.sha256(master.read_bytes()).hexdigest()
ns=['实际逐字稿-v1.1.md','逐字稿与字幕映射-v1.1.json','字幕草稿-v1.1.srt','实际旁白与粗剪交接-v1.1.md','保守EDL-v1.json','audio/voice-master-v1.wav']
r['output_hashes']={n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in ns};r['validation']='只更新地点不确定标记、独立全文稿和门禁当前结论；原音/EDL/master未变，无重复ASR或处理。'
(p/'02-旁白接收报告-v1.1.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));print(json.dumps(r['output_hashes'],ensure_ascii=False,indent=2))
