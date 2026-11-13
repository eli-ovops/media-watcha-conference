from pathlib import Path
R=Path(__file__).resolve().parent
s=(R.parent/'build.py').read_text()
s=s.replace("C=R.parent;", "C=R.parent.parent;")
s=s.replace("for p in ['prepared','shots','qa']", "for p in ['prepared','shots','qa']")
s=s.replace("('V05',180,124,None,'考试感想'),('V08',0,121,None,'闭卷规则')", "('P05',0,78,None,'活动资料'),('P05',0,102,(0,.30,.58,.65),'胸牌与册子'),('V05',180,65,None,'现场过渡')")
s=s.replace("('P13',0,145,(70,1190,1060,550),'成绩')", "('P13',0,145,(90,1310,450,440),'成绩')")
s=s.replace("('P08',0,60,(.03,.30,.94,.68),'现场红黑榜'),('P08',0,60,(.50,.33,.46,.33),'Claude区域')", "('MOTION',0,120,None,'红黑榜聚焦')")
s=s.replace("source=M/('视频'", "source=M/('视频'")
s=s.replace(" item={'shot'", " if sid=='MOTION': source=R/'board-focus.mp4'\n item={'shot'")
s=s.replace(" if sid.startswith('P'):", " if sid=='MOTION':\n  args=['-i',str(source)];vf='setsar=1'\n elif sid.startswith('P'):")
s=s.replace("(720,1280)","(1080,1920)").replace("(720,1150)","(1080,1800)").replace("(720-im.width)//2,(1280-im.height)//2", "(1080-im.width)//2,(1920-im.height)//2")
s=s.replace("'-framerate','30'", "'-framerate','60'")
a="vf='scale=720:1280:force_original_aspect_ratio=decrease,pad=720:1280:(ow-iw)/2:(oh-ih)/2:color=0x151515,setsar=1' if sid=='V02' else 'scale=720:1280,setsar=1'"
b="vf=('crop=404:720:200:0,scale=1080:1920,setsar=1' if src==0 else 'crop=404:720:40:0,scale=1080:1920,setsar=1') if sid=='V02' else 'scale=1080:1920,setsar=1'"
s=s.replace(a,b)
s=s.replace("'-vf',vf,'-frames:v',str(nf),'-r','30'", "'-vf',vf+',fps=60','-frames:v',str(nf*2),'-r','60'")
# Existing master and source clock preserved; same code byte-exact inserts same silence.
s=s.replace('PlayResX: 720','PlayResX: 1080').replace('PlayResY: 1280','PlayResY: 1920')
s=s.replace('Default,PingFang SC,34','Default,PingFang SC,68').replace('1,2,1,2,35,35,140,1','1,3,1,2,60,60,255,1')
s=s.replace("cues+labels:ass+=f'Dialogue: 0", "cues+labels:ass+=f'Dialogue: 0")
s=s.replace("watcha-rough-v1.mp4", "watcha-full-v2.mp4")
(R/'build_v2.py').write_text(s)
