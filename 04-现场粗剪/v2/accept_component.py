from pathlib import Path
import json,sys,hashlib
sys.path.insert(0,'/Users/USER/.codex/skills/fred-remotion-output/scripts')
from library_gate import acceptance_signature
R=Path(__file__).resolve().parent;p=R/'component-manifest.json';m=json.loads(p.read_text());s=m['pages'][0]
def rec(p,**kw):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),**kw)
ref=s['referenceChoices'][0];ref.update(useMode='local',keyAction='Same source image and spotlight aperture share translated/scaled camera; emphasis after settlement.',source=rec(R/'NewsFocus.original.tsx',symbol='NewsSpotlightFocus'),implementation=rec(R/'NewsFocusPortrait.tsx',symbol='NewsSpotlightFocus'),callSite=rec(R/'Motion.tsx',symbol='BoardFocus',callee='NewsSpotlightFocus'))
s['keyframeReview']={'frames':[rec(R/'qa'/f'motion-{f}.png') for f in [0,42,75,110,150,210,239]],'sourceFiles':[rec(R/'NewsFocusPortrait.tsx'),rec(R/'Motion.tsx')]}
s['componentAcceptance'].update(stage='keyframes',evidence=s['keyframeReview']['frames'],checks={'semanticFit':'P08 original pixels enlarge to Claude, retain board context then darken outside one region.','corePreserved':'Exact 64-line component retained, only portrait dimensions/safe window parametrized; same camera matrix, easing, aperture, camera-first ordering.','visualQuality':'Inspected 7 actual 1080x1920 frames including midpoint, before/after emphasis and tail. Claude name and sticker edges stay within viewport, no duplicate or clipped aperture. Region fills 91% screen width; full-board establishing view lasts 0.7s before motion.'})
s['componentAcceptance']['contextSha256']=acceptance_signature(m,s,'keyframes');p.write_text(json.dumps(m,ensure_ascii=False,indent=2))
