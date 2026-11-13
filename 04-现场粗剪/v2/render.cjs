const path=require('path');
const {bundle}=require('@remotion/bundler');
const {selectComposition,renderMedia,renderStill}=require('@remotion/renderer');
(async()=>{
const serveUrl=await bundle({entryPoint:path.join(__dirname,'Motion.tsx'),publicDir:path.join(__dirname,'public'),webpackOverride:c=>c});
const browserExecutable='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const composition=await selectComposition({serveUrl,id:'BoardFocus',browserExecutable});
for(const frame of [0,42,75,110,150,210,239]) await renderStill({serveUrl,composition,frame,output:path.join(__dirname,`qa/motion-${frame}.png`),browserExecutable});
await renderMedia({serveUrl,composition,codec:'h264',outputLocation:path.join(__dirname,'board-focus.mp4'),browserExecutable,concurrency:2,crf:18});
console.log('MOTION_COMPLETE');
})();
