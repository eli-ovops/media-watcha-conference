# 千年之后：仅换配乐交付

当前候选 watcha-full-v4-qiannian.mp4，播放入口 play.html。取本人旧 TikTok 作品 7698739733651934465 恢复文件音轨 0—45.7 秒，准确源与 SHA 见 Manifest.json / source-identity.json；不是独立 studio 音乐文件。不叠加 Carefree，原无 BGM v2 与 Carefree v3 均保留。

新源实测 −9.71 LUFS、真峰值 +0.96 dBTP；按新源校准增益，旁白段 −24.29 dB，中段 −15.29 dB。音乐8.5—9.1秒渐升、26.9—27.5秒渐降，首0.4秒淡入、末1.2秒淡出。保留原旁白单位增益/速度/源钟，仅复制至双声道再混音编码。未尝试修复源本身可能已有的失真。

最终 AAC 音轨45.674秒、48kHz双声道；全段 −21.03 LUFS、真峰值 −2.87 dBTP，无新增输出爆峰；中间10—26秒 −25.44 LUFS，证实有声。容器和画面45.700秒，音轨末尾短26毫秒。2742个视频包 data_hash、PTS、DTS、duration、size 逐项一致，仍1080×1920、60fps；未重渲画面/字幕/封面，复用其既有QA。

直接听感、是否盖旁白、自然度仍待用户试听。已有ASR仅未识别词句，不证明纯净分离或直接听过；本轮未重ASR/分离/研究音乐。

原始测量日志的 input_i/input_tp 表示实际源或交付音轨；output_* 是仅写入 null 的测量滤镜结果，未施加给最终音轨。源参数与复现入口 mix.py / filter.txt / command.json；视频包对照与规格见 video-packets-before/after.json / probe.json。原旁白测量复用上轮相同SHA输入的证据，无重复测量。

许可未确认，不标 CC BY、不沿用 Carefree 署名。任务记录：B站历史识别千年之后(氛围版)—和乐府；YouTube历史识别若如初见(千年之后)并 global block，后续由PMO单列，不变速变调规避。未发布、未改共享状态或06草稿、未派下游。

本目录新增文件均为工程、交付或必要验证证据，全部保留；无一次性清理项。目标Astra medium，实际模型/effort UNKNOWN；规则沿v4/workflowv3/productionv5/reworkv2/ROUTINGv5/TOKEN-BUDGETv1。
