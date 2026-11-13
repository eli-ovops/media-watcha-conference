# BGM 变化限定补核
2026-10-24｜05｜v3-bgm
结论：SCOPED_BGM_TECHNICAL_REVIEW_NO_NEW_MUST_FIX。可作为用户已选音乐后的非公开准备候选；不是听感或完整AV通过。

对象：../04-BGM混音/watcha-full-v3-bgm.mp4
SHA256：e5ec6ba3bfb967c37da5ada95448cf828d158085b3974f0e41079da32bb93330（复用PMO本次现文件核验，05不重复计算）。
已读正式05 allowed=true回执、Manifest、mix.py、filter.txt、command.json、mix.log、四份测量原始日志、probe.json、前后video-packets JSON、source-license及README、06平台音乐与话题规则v2。未执行混音脚本或重跑测量/解码/ASR/画面QA。

## 支持的技术结论
- 05实际解析比较既有前后包原件：两份JSON完全一致，均2742包，涵盖pts/dts/duration/size/data_hash。结合-c:v copy命令与执行日志，支持画面与时序未改；复用原视频和封面Q1结论。
- 音乐为Carefree，取0—45.7秒。音乐增益：旁白区-14.06dB，中段-5.06dB；8.5—9.1秒上升，26.9—27.5秒回落；首0.4秒、尾44.5—45.7秒淡化。音量包络作用于bgm支路。
- voice支路仅atrim与pan=stereo左右复制，amix normalize=0，无变速/增益/降噪/时间偏移；支持“混合前旁白以单位增益保留”。最终混音AAC重新编码，不支持旁白最终压缩样本/原AAC包完全不变。
- Manifest gain_db.narration 是“旁白期间的BGM增益”，不是旁白减14.06dB；脚本和README已明确，无需改音轨。
- 日志input_i/input_tp与Manifest一致：最终-21.01 LUFS/-2.85 dBTP，中段10—26秒-25.35 LUFS/-10.73 dBTP。loudnorm output_*只为输出到null的测量结果，未用于交付滤镜。测量支持中段有音频与真峰值低于0，不证明音乐悦耳、合拍或不盖人声。
- probe原件：视频45.700秒、音频45.674秒/48kHz/双声道、两轨start_time=0。尾差26ms明确保留，在既定尾淡化中不构成已有证据支持的必改；不能推定其不可听或精确同步通过。

## 来源与用途
作者官方曲目索引搜索结果本轮可读，确认Carefree / Kevin MacLeod / ISRC USUAN1400037 / CC BY 4.0；直接打开主详情入口只有Loading壳，不冒充其完整正文。官方索引来源：
https://incompetech.com/music/royalty-free/index.html?isrc=USUAN1400037&lt=
https://remote.incompetech.com/music/royalty-free/index.html?Search=Search&isrc=USUAN1400037
source-license记录源MP3 SHA8433b770a630d9b1594fd484442c677907ece899a4d149954cd2e74fd733e311，与脚本断言一致；本轮未重新下载或重哈希。README已保留作者、来源、许可链接与截取/音量/淡化改动署名，06须实际带入发布说明，本报告不证明各平台已填写。
其他当前活跃平台按用户决定用此Carefree混音；抖音沿无BGM v2及原生已有热门音频路线，不用此混音关联另一首曲目冒充配乐。全平台话题沿#观猹大会/#观猹，原生挂载是否生效由06核；本轮未操作平台。

## 未验与交付边界
直接听感、音乐与口播遮盖关系、首尾自然度、逐字同步、正常速度连续AV均UNKNOWN；本人完整试看听由PMO接续，尤其8.5/9.1和26.9/27.5秒音量转折、44.5秒后结尾。不能将本次技术通过升级为用户终审或发布授权。
无新增技术必修，未改04/06/共享状态、未派下游或发布。沿现行AGENTSv4/workflowv3/productionv5/reworkv2/ROUTINGv5/TOKEN-BUDGETv1；目标Astra medium，实际model/effort/speed UNKNOWN。
只新增本报告、补充JSON及发送回执，均为必要验收证据；没有新媒体/临时文件或清理。
