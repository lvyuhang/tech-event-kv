const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const meta=JSON.parse(fs.readFileSync('meta.json'));const b=await chromium.launch();fs.mkdirSync('out',{recursive:true});
for(const [k,m] of Object.entries(meta)){const s=Math.min(3,Math.max(1,4000/Math.max(m.w,m.h)));
 const p=await b.newPage({viewport:{width:m.w,height:m.h},deviceScaleFactor:s});
 await p.goto('file://'+path.resolve(k+'.html'));await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);
 await p.screenshot({path:`out/${k}.png`,clip:{x:0,y:0,width:m.w,height:m.h}});await p.close();}
await b.close();})();
