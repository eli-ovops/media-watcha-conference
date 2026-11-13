// Resolve only the gate's missing hard-coded TypeScript location to existing runtime.
// No validator/parser behavior is changed; no dependency is installed.
const Module=require('module');const path=require('path');const original=Module._resolveFilename;
Module._resolveFilename=function(request,...args){
 if(request==='/Users/USER/.codex/skill-repos/FredTalk/apps/library/node_modules/typescript') request=path.join(__dirname,'node_modules/typescript');
 return original.call(this,request,...args);
};
