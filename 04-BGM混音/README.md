# 观猹大会 BGM 变化交付

仅新增 Carefree — Kevin MacLeod 音乐混音，文件 watcha-full-v3-bgm.mp4；原无 BGM 视频保留。打开 play.html 预览。

- 音乐从原曲 0 秒截取到 45.7 秒。按源段实测 −19.94 LUFS 校准：旁白段增益 −14.06 dB，中段 −5.06 dB；8.5—9.1 秒抬升，26.9—27.5 秒回落；音乐首 0.4 秒淡入、末 1.2 秒淡出。
- 原旁白解码后以单位增益复制至左右声道，未变速、降噪、改字或改时间；混合后编码 AAC 192 kbps。测量用 loudnorm 的 input_i/input_tp 是实际文件指标，output_* 仅为丢弃到 null 的测量滤镜结果，并未应用给交付音轨。
- 实际新音轨：45.674 秒、48 kHz、双声道；容器与画面为45.700秒，音轨末尾相差26毫秒。全段 −21.01 LUFS / 真峰值 −2.85 dBTP，无爆峰。中段 10—26 秒 −25.35 LUFS，证实有声。
- 视频 2742 个包的 SHA256、PTS、DTS、duration、size 全部与原视频一致；1080×1920、60 fps、45.7 秒。仅流复制，无画面重渲或重复图像 QA；字幕和封面 v3 不变。
- 直接听感和连续声画仍未核，不称完全合拍；供 PMO 和用户预览。未发布，未改 06 草稿或共享状态。

复现入口 mix.py（默认不覆盖已存在成片）；--verify-existing 可复用已完成的音频测量并核现有输出。filter.txt 与 command.json 保存准确滤镜和命令。系统 ffprobe 的 Bad CPU type 已按 LOCAL_BLOCKERS 已知兼容路径处理：仅探测子进程使用现有 Remotion arm64 ffprobe 与对应 DYLD_LIBRARY_PATH，未安装或修改全局环境。

SHA、输入、许可、增益包络见 Manifest.json 和 source-license.json；原始测量日志和前后视频包 JSON 同目录保留。原始音乐仅引用已有 06 文件，未下载副本。目录中新增文件均为交付、源参数或必要证据，保留，无一次性清理项。

发布署名须保留：Carefree — Kevin MacLeod (incompetech.com). Licensed CC BY 4.0: https://creativecommons.org/licenses/by/4.0/ . Excerpted, volume adjusted and faded for this video.
