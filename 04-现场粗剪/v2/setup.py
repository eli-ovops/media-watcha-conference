from pathlib import Path
import json,subprocess,hashlib
R=Path(__file__).resolve().parent;S=Path('/Users/USER/.codex/skills/fred-remotion-output/scripts');sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
q='真实截图 局部蒙版聚焦与镜头推进'
d=json.loads(subprocess.check_output(['python3',str(S/'references.py'),'--query',q,'--use','recording-focus','--limit','3']))
(R/'qa/candidate-catalog.json').write_text(json.dumps(d,ensure_ascii=False,indent=2))
choices=[('component:interaction-news-spotlight','selected','同一P08源图先推进再单层挖孔，Claude贴纸仍是原像素，保留上下文。'),('component:interaction-news-brush','rejected','荧光笔覆盖照片贴纸会改变红绿颜色，适合文字行而非投票照片。'),('component:fred-wave3-40-t09o','rejected','圆镜会裁掉矩形Claude名称与贴纸分布，镜片巡游不适合单一目标。')]
preview=Path('/Volumes/EXTERNAL/自媒体/资产库/FredTalk/组件视频/INT02-2-preview.mp4');sheet=Path('/Volumes/EXTERNAL/自媒体/Fred付费资料全站学习-20261016/证据/333视频动态读取/时间序列图/INT02-2-preview-p01.jpg')
page={'stableId':'board-focus','sceneType':'prompt-reading','implementationMode':'adapted','start':20.5,'end':24.5,'sourceSpans':[{'text':'现场红黑榜，Claude真是罪孽深重啊'}],'referenceChoices':[{'id':choices[0][0],'reason':choices[0][2],'preserve':'同源整图、相机组位移与缩放、停稳后单层蒙版挖孔及原曲线完整保留','change':'横版1920×1080几何参数化为1080×1920；本期P08/ROI，4秒窗口，末态直接交布袋不回全景','useScope':'20.5—24.5 P08整图到Claude重点'}],'componentPlan':{'query':q,'use':'recording-focus','candidates':[{'id':i,'decision':a,'reason':b} for i,a,b in choices],'inspectedReferences':[{'id':choices[0][0],'path':str(preview),'sha256':sha(preview),'observations':'已看准确v2采样图0—5.75秒：整页推进，2.75后背景暗，目标孔与源图共变换，后退；本片同对象推进并保留停稳后强调。'}]},'componentAcceptance':{'status':'passed','stage':'suggestion','reviewer':'04','checks':{'semanticFit':'照片上Claude名称与红绿贴纸是单一矩形目标，用源图推进和单层挖孔匹配','corePreserved':'保留同源像素/共组相机/停稳后蒙版，portrait参数化而非跨栈重画','visualQuality':'实看INT02-v2与INT01-v2和T09o网格，暗幕可保照片颜色且无镜片遮挡；本期需核竖版目标最大安全范围'},'evidence':[{'path':str(sheet),'sha256':sha(sheet)}]}}
m={'content_id':'watcha-conference-20261024','version':'v2','referenceCatalogRevision':d['catalogRevision'],'pages':[page]}
(R/'component-manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
