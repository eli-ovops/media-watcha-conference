from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();p=R/'Manifest.json';m=json.loads(p.read_text())
m['stage']='FORMAL_EXPORT_AND_COVERS_READY_FOR_PMO_QA';m['representative']['PMO_comparison']='SCOPED_VISUAL_ACCEPTED; PMO-代表段原效果对照-v2.json'
m['checked'].update(full_export='45.7s,2742frames,1080x1920,60fps; full decode no errors; qa/probe.json and decode.log',final_visual='46 one-second samples; all15 cuts x3 frames; 10 targeted native frames including motion midpoint; 6 key phone-size frames. No sampled white flash or clipped focus. Continuous AV remains NOT_PERFORMED.',audio='PCM file byte identical plus demuxed AAC packet hash identical to rough-v1; qa/audio-copy-proof.json',covers='4 independently generated layouts; actual final pixel sizes verified; complete generated image and normalized phone-contact inspected; main copy black AI考试, violet92分, black观猹大会.16x9 tiny wrong pedestal year removed via imagegen targeted edit. Platform auto-crop not verified.')
m['production_record']['formal_full_assembly_runs']=1;m['production_record']['cover_generation_calls']=5;m['production_record']['next_improvement']='Before next rough export, preview wide media and subtitles at360px width to prevent small center bands.'
m['cover_manifest']='covers/cover-manifest.json';m['actual_model_effort']='UNKNOWN';m['pending']=['PMO full-file review','05 independent QA dispatched by PMO','direct hearing/naturalness/word alignment','normal-speed continuous audiovisual acceptance','user final video and cover approval'];m['outputs']=[]
for name in ['watcha-full-v2.mp4','build_v2.py','Motion.tsx','NewsFocusPortrait.tsx','NewsFocus.original.tsx','render.cjs','scene-edl-60fps.json','voice-edl.json','subtitles-v1.srt','titles.ass','labels.json','component-manifest.json','covers/cover-manifest.json','covers/prompts.json']:
 f=R/name;m['outputs'].append({'path':str(f),'sha256':sha(f)})
p.write_text(json.dumps(m,ensure_ascii=False,indent=2))
(R/'play.html').write_text('''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>观猹大会 v2</title><style>body{margin:24px;background:#171717;color:white;font:16px system-ui;text-align:center}video{height:80vh;max-width:100%}a{color:#c7adff}.covers{display:flex;gap:14px;justify-content:center;flex-wrap:wrap}.covers img{max-width:300px;max-height:360px;object-fit:contain}</style><h1>观猹大会 · v2</h1><video controls playsinline preload="metadata" src="watcha-full-v2.mp4"></video><p>45.7秒 ·1080×1920·60fps ｜ 实拍源30fps ｜ 无BGM<br>直接听音、连续声画与终审仍待完成</p><p><a href="watcha-full-v2.mp4">完整视频</a> · <a href="README.md">交付说明</a></p><div class="covers">'''+''.join(f'<a href="covers/{f.name}"><img src="covers/{f.name}"></a>' for f in sorted((R/'covers').glob('cover-*-v2.png')))+ '</div></html>')
(R/'README.md').write_text('''# 观猹大会 v2 正式规格交付

完整成片45.7秒，1080×1920，60fps，2742帧。当前是待PMO/05/用户验收的制作交付，未发布。实拍源30fps重复帧输出；不宣称新增运动细节。原生INT02动效按60fps计算。

- 播放：`watcha-full-v2.mp4`；浏览器本地打开`play.html`可播放并查看四封面。
- R1：会场横幅改主体竖屏取景；P08准确INT02-v2源码保留完整同图相机组/单层蒙版，竖屏几何适配，已获PMO代表段限定视觉接收；92/通过为实际成绩截图的大幅裁切，无准考号。
- R2：27.5—30.1秒活动资料；30.1—33.5秒胸牌特写；33.5—35.6667秒短现场过渡；再接成绩。不编考场。
- R3：字幕68px/1080宽，手机尺度已实看；源候选时间重映射保持。区名未上屏，“最有意思”和精确字词仍待听核。
- 声音：复用rough-v1 AAC音频包，包哈希完全一致；PCM时间线文件也逐字节相同。无BGM，现场原音静音，中间19秒有意无旁白。
- 四封面：`covers/cover-3x4-1080x1440-v2.png`、`cover-9x16-1080x1920-v2.png`、`cover-16x9-1920x1080-v2.png`、`cover-4x3-1440x1080-v2.png`。白底黑紫标题AI考试／92分／观猹大会、真实入口作参考，无本人肖像。内置imagegen各比例独立生成，16:9局部修一次；等比规范化，不拉伸或盲裁。属于生成合成封面，不称原始现场像素。文字为本期事实草案，待终审。提示词/输入/来源/像素/SHA见covers下JSON。

## 工程与复现

现有工程直接接续，v1不覆盖。`build_v2.py`负责真实媒体裁切、字幕和封装；`Motion.tsx`实际调用`NewsFocusPortrait.tsx`，完整准确源存`NewsFocus.original.tsx`。`scene-edl-60fps.json`为正式时间线，`scene-edl.json`保留30fps剪辑换算轴，视频源入出帧均按原30fps；声音源钟见`voice-edl.json`。

使用现有依赖：先`node render.cjs`（仅改动组件时），再以已有Python/Pillow运行`build_v2.py`。项目node_modules链接已有Remotion环境，无新增安装。脚本复用shots缓存，修改镜头须为对应产物指定新文件名或新版本路径，不能盲用旧缓存。其余setup/prepare脚本是过程记录，重导出用上述两个入口。

组件建议门禁PASS；关键帧初次缺TypeScript路径失败，随后task-local `parser-dependency.cjs`仅把缺失路径映射到已有TypeScript，原门禁与解析逻辑未修改，真实关键帧门禁PASS。完整回执均在qa，非审美或听音的替代。

## 实际验收覆盖

全片解码与规格通过；看过最终46个1fps样本、全部15处剪点各前中后三帧、10张实际原尺寸重点帧、6张360px手机图，另有组件7中态和改区18帧。准确原组件及本期代表段由PMO按源码+实际帧接收。以上不是连续观看。

直接听音、自然度、精确字幕同步、正常速度连续声画仍UNKNOWN/未做：沿02已验证不支持音频输入的结果，未重跑ASR或部署模型。PMO/05和用户终审待完成，不能称全项验收通过。平台裁切未验、没有发布授权。

唯一交付清单`Manifest.json`含成片SHA与源码绑定。旧rough-v1为历史对照。制作记录：PMO反馈1批，正式全片封装1次，组件动效渲染1次；下次先在360px预览横幅主体和字幕，避免小中央条带。
''')
print('FINAL_SHA',sha(R/'watcha-full-v2.mp4'))
