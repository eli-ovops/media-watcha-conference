import {Client} from "/Volumes/EXTERNAL/自媒体/工具验证/video-mcp-20261007/upstream/node_modules/@modelcontextprotocol/sdk/dist/esm/client/index.js";
import {StdioClientTransport} from "/Volumes/EXTERNAL/自媒体/工具验证/video-mcp-20261007/upstream/node_modules/@modelcontextprotocol/sdk/dist/esm/client/stdio.js";
import {writeFileSync,mkdirSync} from 'node:fs';
const out="/Volumes/EXTERNAL/自媒体/watcha-conference-20261024/00-素材接收";
const names=["98af5d6722190a07fa32d89a12bb95b2.mp4","55737de88d63f8e39796ef97dffe8bb5.mp4","ba133b9b9a255ccb739331c5409fe45e.mp4","32ad7300b84096bc247ec0eaa46a1814.mp4","d13eac06b2cb29f7a6e69ffe11a99986.mp4","651c140d1606cd944cdd6fc093904ead.mp4","342354b593ded2b72fd3930e6f489fa5.mp4","b4b93514b48ef8a03e6ae40504a5368d.mp4","06569f26ac30632e35c93313d72b93b2_raw.mp4"];
const client=new Client({name:'watcha-material-intake',version:'1.0.0'});
const tr=new StdioClientTransport({command:process.execPath,args:["/Volumes/EXTERNAL/自媒体/工具验证/video-mcp-20261007/launch.mjs"],env:{PATH:'/usr/bin:/bin'},stderr:'pipe'});
try{
await client.connect(tr);
for(let i=0;i<names.length;i++){
const id='V'+String(i+1).padStart(2,'0'); const source='/Users/USER/Downloads/'+names[i];
const info=await client.callTool({name:'video_info',arguments:{source,response_format:'json'}},undefined,{timeout:180000});
writeFileSync(out+'/'+id+'-info.json',JSON.stringify(info,null,2));
if(info.isError)throw new Error(id+' info refused; stopped without another read route');
console.log(JSON.stringify({id,phase:'info',info:info.structuredContent}));
const result=await client.callTool({name:'video_analyze',arguments:{source,detail:'standard',max_frames:6,mode:'interval',language:'zh',skip_ocr:true,inline_images:false,response_format:'json'}},undefined,{timeout:180000});
writeFileSync(out+'/'+id+'-analysis.json',JSON.stringify(result,null,2));
if(result.isError)throw new Error(id+' analysis failed; saved exact error and stopped');
console.log(JSON.stringify({id,phase:'analyzed',resultFile:out+'/'+id+'-analysis.json'}));
}
}finally{await client.close();}

