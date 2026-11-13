# 04｜选定Carefree直接混入本期视频
用户当前要求“准备发布吧，选一个bgmg”。06已保存抖音非公开草稿，但网页“添加音乐”明确只挂作品底部音乐信息，不改变声音；当前不能只交手机操作即称完成。PMO已选作者官方公开免费署名音源Carefree—Kevin MacLeod，当前任务仅混音，不重新设计视频或换封面。
正式门禁rollback04仅为BGM变化，release/check后执行。唯一04不建新Owner。目标Astra medium沿现有设置；AGENTSv4/workflowv3/productionv5/reworkv2/ROUTINGv5/TOKEN-BUDGETv1。

## 输入
已验视频 ../04-现场粗剪/v2/watcha-full-v2.mp4，SHA6c3f10b0e98eba9b8db239dfc6c8ab4b78693ee19d7cfcb9533c23474a5ed0a8，45.7秒1080×1920/60fps2742帧。当前封面v3都保留。
已下载官方音源 ../06-发布准备/bgm/Carefree-Kevin-MacLeod.mp3，SHA8433b770a630d9b1594fd484442c677907ece899a4d149954cd2e74fd733e311。source-license.json核作者官网曲目页/MP3地址/CC BY4.0/署名/改动说明；96BPM、3:25、Ukulele/Guitar/Marimba/Glockenspiel/Percussion。不再研究/选其他曲，不称当前热榜，不再次下载。
之前无BGM边界被用户本轮选BGM明确覆盖；不改变原画面、旁白内容/速度/源时钟。

## 最小混音
仅copy原video stream，加入BGM导出另一个完整MP4，不重渲画面/组件/字幕。不要把导出变成新视频开发。优先整曲从0秒取45.7秒，既有ffmpeg测音乐段响度后定音量；首尾短淡入淡出，旁白0—8.5及27.5—45.7压低，中段8.5—27.5稍抬，音量渐变不硬跳。
可参考BGM说话段约-34LUFS、无旁白段约-25LUFS，实际沿已测源响度校准；这是保守混音起点，不是假称听过。旁白电平与时间不动，不重复变速/降噪/固定大增益，不为音乐伸缩45.7秒或改画面切点。混音不爆峰，淡出不切掉人声字尾。
保存mix脚本/滤镜及源范围、音量包络、原始旁白与音乐对应，报告客观音轨时长/真峰值/音乐段有声、原video packet不变。只做本改动需要的验证，复用原画面QA，不重复整片图像或ASR。直接听感仍未核，不用响度/包哈希代替听核；新混音先供用户最终预览，不承诺完全合拍。
文件另存watcha-full-v3-bgm.mp4，保留无BGM原件。工程/Manifest写source→music→滤镜→实际输出SHA、规格、音乐许可与署名；附适用播放页或直接可预览文件。仅写本04-BGM目录；不修改06已保存草稿/共享状态、不自行派05/06、不发布、无费用/安装/额外私有上传。
结束主动工具消息报告PMO01a11194-c40d-7bf0-8396-5bb5d6449444并保存发送回执，不只final、不轮询。人类通信授权沿当前AGENTS和协作入口userMessage01a133d5-4256-7321-a6d0-b6116d2e02ce。
