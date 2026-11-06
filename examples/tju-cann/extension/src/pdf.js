const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const meta=JSON.parse(fs.readFileSync('meta.json'));const b=await chromium.launch();fs.mkdirSync('pdf',{recursive:true});
for(const [k,m] of Object.entries(meta)){ if(!m.mm) continue; let [wmm,hmm]=m.mm; let note='';
  if(wmm>5000){wmm/=2;hmm/=2;note='_1比2';}
  const s=(wmm/25.4*96)/m.w; const p=await b.newPage();
  await p.goto('file://'+path.resolve(k+'.html')+'?s='+s);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);
  await p.pdf({path:`pdf/${k}${note}.pdf`,width:wmm+'mm',height:hmm+'mm',printBackground:true,pageRanges:'1'});await p.close();}
await b.close();})();
