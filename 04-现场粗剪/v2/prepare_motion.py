from pathlib import Path
from PIL import Image,ImageOps
R=Path(__file__).resolve().parent
src=Path('/Volumes/EXTERNAL/自媒体/Fred付费资料全站学习-20261016/解包只读副本/FredTalk公开仓库/components/projects/interaction-components-20261007/interaction-components/src/NewsFocus.tsx')
s=src.read_text();(R/'NewsFocus.original.tsx').write_text(s)
s='// Adapted from exact INT02-v2 NewsFocus.tsx; only portrait geometry parametrized.\n'+s
s=s.replace('1920','1080').replace('1080/sh','1920/sh').replace('(1080-imageHeight)/2','(1920-imageHeight)/2')
s=s.replace('1600/(maxX-minX),740/(maxY-minY)','980/(maxX-minX),1050/(maxY-minY)')
s=s.replace('(960-cx*safeZoom)','(540-cx*safeZoom)').replace('(470-cy*safeZoom)','(850-cy*safeZoom)')
s=s.replace('height:1080','height:1920').replace('height={1080}','height={1920}')
(R/'NewsFocusPortrait.tsx').write_text(s)
photo=R.parents[1]/'01-原始素材/照片/P08.jpg'
im=ImageOps.exif_transpose(Image.open(photo));im.save(R/'public/P08.jpg',quality=96)
print(im.size)
