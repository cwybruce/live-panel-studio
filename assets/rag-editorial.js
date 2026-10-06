/* Original RAG editorial scene. All motion remains a pure function of seek(t). */
B.ragEditorial=function(e){
 var root=vroot(e),svg=root.svg,id=root.id,C=editorialPalette(e);
 var mono='"LP Mono", "LP Sans", monospace',font='"LP Sans", sans-serif',serif='"LP Serif", serif';
 function txt(x,y,s,size,c,b,extra){var face=(size>=17&&!/^[0-9.?%]+$/.test(s))?serif:/^[\x20-\x7e]+$/.test(s)?mono:font;return '<text x="'+x+'" y="'+y+'" font-size="'+(size||12)+'" fill="'+(c||C.fg)+'" font-family="'+face.replace(/"/g,'&quot;')+'"'+(b?' font-weight="600"':'')+(extra||'')+' data-component-text="1">'+esc(s)+'</text>'}
 function small(x,y,s,c){return txt(x,y,s,9,c||C.dim,false,' letter-spacing="1.3"')}
 function rect(x,y,w,h,stroke,fill,rx,extra){return '<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="'+(rx==null?4:rx)+'" fill="'+(fill||'none')+'" stroke="'+(stroke||C.line)+'" stroke-width=".8"'+(extra||'')+'/>'}
 function badge(x,y,w,s,c){return rect(x,y,w,19,c,C.shade('#181611'),3)+txt(x+7,y+13,s,9,c)}
 function card(x,y,w,h,title,sub,c){return rect(x,y,w,h,c,C.shade('#201d18'),4)+txt(x+9,y+17,title,10,c,true)+txt(x+9,y+33,sub,8,C.dim)}
 function panel(x,y,w,h,n,title,c){return '<g transform="translate('+x+' '+y+')" data-panel="'+n+'">'+rect(0,0,w,h,C.line,C.panel,5,' data-panel-border="'+n+'" data-neon-border="rag-'+['retrieve','rerank','ground','abstain'][n]+'" data-neon-color="'+c+'"')+badge(13,12,95,'0'+(n+1)+' / '+['RETRIEVE','RERANK','GROUND','ABSTAIN'][n],c)+txt(15,58,title,17,C.fg,true)+ '<path d="M15 75H'+(w-15)+'" stroke="'+C.line+'" stroke-width=".6"/>'}
 var s='<defs><pattern id="'+id+'grid" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".45" fill="'+C.shade('#625643')+'" opacity=".17"/></pattern><filter id="'+id+'halo" x="-180%" y="-180%" width="460%" height="460%"><feGaussianBlur stdDeviation="'+(C.light?1.7:4)+'" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>';
 [C.amber,C.cyan,C.pink,C.mint].forEach(function(c,i){s+='<radialGradient id="'+id+'orb'+i+'" cx="30%" cy="25%"><stop stop-color="'+C.shade('#fff5df')+'" stop-opacity=".85"/><stop offset=".35" stop-color="'+(C.light?C.tint(c,.72):c)+'"/><stop offset="1" stop-color="'+C.shade('#211b1a')+'"/></radialGradient>'});s+='</defs>';
 s+='<rect width="984" height="1280" fill="'+C.bg+'"/><rect x="18" y="16" width="948" height="1248" fill="url(#'+id+'grid)"/>';
 s+=small(28,29,'MOTION DIAGRAM STUDIO / A QUESTION’S JOURNEY / 4 STAGES',C.dim);
 s+=txt(28,76,'一个问题，如何找到它的依据',31,C.fg,true)+txt(28,106,'RAG · 从候选知识，到可以核对的回答',14,C.amber);
 s+=txt(28,133,'先检索，再筛选；让每一句回答，沿着引用回到原文。',12,C.dim);
 ['01 提问','02 检索','03 重排','04 回答'].forEach(function(t,i){s+=badge(28+i*87,150,77,t,[C.amber,C.cyan,C.pink,C.mint][i])});
 s+=txt(958,163,'12 秒循环 / 模拟知识库',10,C.dim,false,' text-anchor="end"');
 s+=rect(28,192,928,355,C.line,C.shade('#171511'),5,' data-neon-border="rag-hero" data-neon-color="'+C.amber+'" data-neon-role="hero"')+badge(42,205,108,'THE JOURNEY',C.amber);
 s+=txt(42,251,'把问题交给知识，让回答带着出处。',20,C.fg,true)+small(944,220,'08 DOCUMENTS → 03 CANDIDATES → 02 SOURCES',C.dim).replace('<text ','<text text-anchor="end" ');
 var xs=[145,376,607,838],colors=[C.amber,C.cyan,C.pink,C.mint],names=['明确问题','检索候选','筛选证据','带引用回答'],details=['保留问题的原意','先找到相关片段','核对相关性与原文','每项结论都有出处'];
 for(var i=0;i<3;i++)s+='<path data-route="'+i+'" d="M'+(xs[i]+44)+' 345 C'+(xs[i]+85)+' 303 '+(xs[i+1]-85)+' 303 '+(xs[i+1]-44)+' 345" fill="none" stroke="'+colors[i]+'" stroke-width=".8" opacity=".3"/>';
 xs.forEach(function(x,i){
  s+='<g data-step="'+i+'"><circle data-ring="'+i+'" cx="'+x+'" cy="345" r="55" fill="none" stroke="'+colors[i]+'" stroke-width=".7" opacity=".35"/><circle cx="'+x+'" cy="345" r="45" fill="none" stroke="'+colors[i]+'" stroke-dasharray="2 8" opacity=".3"/><circle cx="'+x+'" cy="345" r="36" fill="url(#'+id+'orb'+i+')" stroke="'+colors[i]+'" stroke-width="1.2"/>';
  if(i===0)s+=txt(x,359,'?',37,C.shade('#fff6de'),true,' text-anchor="middle"');
  if(i===1){s+='<g fill="'+C.shade('#16303a')+'" stroke="'+C.shade('#c6f5f4')+'" stroke-width="1.3"><ellipse cx="'+x+'" cy="332" rx="18" ry="6"/><path d="M'+(x-18)+' 332v23c0 8 36 8 36 0v-23M'+(x-18)+' 344c0 8 36 8 36 0" fill="none"/></g>'}
  if(i===2){s+='<g stroke="'+C.shade('#ffe7f0')+'" stroke-width="4" stroke-linecap="round"><path d="M'+(x-16)+' 358v-12M'+x+' 358v-29M'+(x+16)+' 358v-20"/></g>'}
  if(i===3){s+=rect(x-17,323,34,44,C.shade('#c6efd5'),C.shade('#1e3b2a'),5)+'<path d="M'+(x-9)+' 333h18M'+(x-9)+' 341h18M'+(x-9)+' 349h12" stroke="'+C.shade('#d8ffe8')+'" stroke-width="1.8"/>'}
  s+=txt(x,423,names[i],14,colors[i],true,' text-anchor="middle"')+txt(x,446,details[i],10,C.dim,false,' text-anchor="middle"');
  s+=small(x,281,['QUERY / 01','RETRIEVE / 03','KEEP / 02','CITE / 02'][i],colors[i]).replace('<text ','<text text-anchor="middle" ');
  s+='</g>';
 });
 for(var i=0;i<3;i++)for(var j=0;j<5;j++)s+='<circle data-flight="'+i+':'+j+'" r="'+(j===0?3:1.6)+'" fill="'+colors[i]+'" filter="url(#'+id+'halo)"/>';
 s+='<path d="M43 506H940" stroke="'+C.line+'" stroke-width=".6"/>'+txt(43,529,'当前 · 明确问题',11,C.amber,true,' data-stage-label="1"')+txt(940,529,'只改变状态，所有帧都可以精确回放',10,C.dim,false,' text-anchor="end"');

 // Retrieval: a document array becomes three readable candidates.
 s+=panel(28,566,454,300,0,'先找到相关，再判断是否够用',C.cyan);
 s+=small(18,96,'THE KNOWLEDGE SHELF',C.dim);
 for(var d=0;d<8;d++){var xx=24+(d%4)*43,yy=111+Math.floor(d/4)*64;var hit=[1,4,6].indexOf(d)>=0;s+='<g data-document="'+d+'">'+rect(xx,yy,31,44,hit?C.cyan:C.shade('#655d51'),hit?C.shade('#1a3032'):'none',2)+ '<path d="M'+(xx+6)+' '+(yy+10)+'h18m-18 7h18m-18 7h12" stroke="'+(hit?C.cyan:C.shade('#625b50'))+'" stroke-width=".7"/>'+txt(xx+15,yy+36,'0'+(d+1),7,C.dim,false,' text-anchor="middle"')+'</g>'}
 s+='<path d="M200 143C222 144 211 127 231 127M200 174C221 173 211 176 231 176M200 204C220 208 215 225 231 225" fill="none" stroke="'+C.cyan+'" opacity=".38"/>';
 [['账户帮助 / 02','密码重置入口'],['安全说明 / 05','邮件验证步骤'],['产品公告 / 07','相关，但未回答问题']].forEach(function(a,i){s+=card(231,107+i*49,202,42,a[0],a[1],i===2?C.shade('#796f62'):C.cyan)});
 s+=txt(22,261,'03',26,C.cyan,true)+txt(64,260,'/ 08  候选文档命中',11,C.dim)+txt(18,282,'命中只是开始；不等于可以直接拿来回答。',10,C.dim)+'</g>';
 // Ranking: real authored values and rejected weak evidence.
 s+=panel(502,566,454,300,1,'从 3 条候选，留下 2 条证据',C.pink);
 s+=small(18,97,'ILLUSTRATIVE RELEVANCE SCORES',C.dim);
 [['账户帮助',.91],['安全说明',.84],['产品公告',.22]].forEach(function(a,i){var yy=119+i*50,c=i===2?C.shade('#786b61'):C.pink;s+=txt(18,yy,a[0],11,i===2?C.dim:C.fg)+rect(98,yy-9,265,7,'none',C.shade('#31292a'),2)+'<rect data-score="'+i+'" x="98" y="'+(yy-9)+'" height="7" width="'+(265*a[1])+'" rx="2" fill="'+c+'"/>'+txt(431,yy,a[1].toFixed(2),12,c,true,' text-anchor="end"');if(i===2)s+='<path d="M98 '+(yy-10)+'l6 9m-6 0l6-9" stroke="'+C.red+'" stroke-width=".9"/>'});
 s+=badge(18,246,99,'02 SOURCES',C.pink)+txt(131,260,'保留相关，仍需核对原文',11,C.fg)+txt(18,282,'分数是预设示例；相关性不等于证据充分。',10,C.dim)+'</g>';
 // Grounding: two source fragments feed two explicit citations.
 s+=panel(28,886,454,305,2,'让答案沿着引用，回到原文',C.mint);
 s+=small(18,97,'SOURCE → CLAIM → CITATION',C.dim);
 s+=card(20,118,142,54,'[1] 账户帮助','“点击忘记密码”',C.cyan)+card(20,192,142,54,'[2] 安全说明','“通过邮件验证”',C.pink);
 s+='<path d="M162 145C190 145 193 151 214 151M162 218C189 218 192 192 214 192" fill="none" stroke="'+C.mint+'" stroke-width="1" opacity=".5"/>';
 s+=rect(214,112,221,143,C.shade('#4e6f5b'),C.shade('#17221b'),5)+txt(227,137,'回答',12,C.mint,true)+txt(227,165,'进入登录页，选择',12,C.fg)+txt(227,187,'“忘记密码”。 [1]',12,C.fg)+txt(227,214,'按邮件提示完成验证。 [2]',11,C.fg)+txt(227,241,'引用可以定位到具体片段',9,C.dim);
 for(var i=0;i<2;i++)for(var j=0;j<4;j++)s+='<circle data-evidence-flight="'+i+':'+j+'" r="2" fill="'+C.mint+'" filter="url(#'+id+'halo)"/>';
 s+=txt(18,284,'不是让答案看起来可信，而是让出处可以核对。',10,C.dim)+'</g>';
 // Abstention: an empty evidence relation, not a fake confident answer.
 s+=panel(502,886,454,305,3,'没有依据，也是一种明确的结果',C.red);
 s+=small(18,97,'WHEN EVIDENCE IS MISSING',C.dim)+card(20,116,184,57,'问题 / 管理员口令？','提供的文档没有这项信息',C.amber);
 s+='<path d="M205 144H262" stroke="'+C.red+'" stroke-width=".8" stroke-dasharray="3 5"/><circle cx="335" cy="155" r="42" fill="none" stroke="'+C.red+'" stroke-width=".8" opacity=".7"/><circle cx="335" cy="155" r="51" fill="none" stroke="'+C.red+'" stroke-dasharray="2 7" opacity=".25"/>'+txt(335,159,'0',31,C.red,true,' text-anchor="middle"')+txt(335,180,'条可用证据',9,C.dim,false,' text-anchor="middle"');
 s+=rect(20,220,414,42,C.shade('#70473d'),C.shade('#271b16'),4)+txt(32,247,'无法根据现有资料确认，请补充来源。',13,C.red,true)+txt(18,284,'缺失、矛盾和越界信息，都应当明确说明。',10,C.dim)+'</g>';
 s+='<path d="M28 1212H956" stroke="'+C.line+'" stroke-width=".7"/>'+txt(28,1237,'检索提供候选 · 重排筛选证据 · 引用连接原文 · 无依据时说明',12,C.fg)+txt(28,1259,'原创中文视觉样板 / 所有文本、分数与事件均为预设演示',9,C.dim)+txt(956,1259,'MOTION DIAGRAM STUDIO · RAG / 01',9,C.amber,false,' text-anchor="end"');
 svg.innerHTML=s;
 var rings=svg.querySelectorAll('[data-ring]'),steps=svg.querySelectorAll('[data-step]'),routes=svg.querySelectorAll('[data-route]'),dots=svg.querySelectorAll('[data-flight]'),panels=svg.querySelectorAll('[data-panel-border]'),docs=svg.querySelectorAll('[data-document]'),scores=svg.querySelectorAll('[data-score]'),evidence=svg.querySelectorAll('[data-evidence-flight]'),label=svg.querySelector('[data-stage-label]');
 COMPONENTS.push(function(t){
  var sec=mod(t,12),k=Math.min(3,Math.max(0,Number(V['rag.i'])||0));label.textContent='当前 · '+tv('rag');label.setAttribute('fill',colors[k]);
  steps.forEach(function(n,i){n.setAttribute('opacity',i===k?1:.68)});
  rings.forEach(function(n,i){n.setAttribute('r',55+(i===k?Math.sin(t*1.7)*2:0));n.setAttribute('opacity',i===k?.85:.2);n.setAttribute('filter',i===k?'url(#'+id+'halo)':'')});
  routes.forEach(function(n,i){n.setAttribute('opacity',i===k?.85:.22)});
  dots.forEach(function(n){var q=n.getAttribute('data-flight').split(':').map(Number),i=q[0],j=q[1],u=phase(t,2.3,j*.18),a=xs[i]+44,b=xs[i+1]-44;n.setAttribute('cx',a+(b-a)*u);n.setAttribute('cy',345-Math.sin(u*Math.PI)*30);n.setAttribute('opacity',i===k?Math.sin(u*Math.PI)*(.95-j*.12):.07)});
  panels.forEach(function(n,i){var active=i===Math.max(0,k-1)||(i===3&&k===3);n.setAttribute('stroke',active?[C.cyan,C.pink,C.mint,C.red][i]:C.line);n.setAttribute('stroke-opacity',active?.8:1)});
  docs.forEach(function(n,i){var hit=[1,4,6].indexOf(i)>=0;n.setAttribute('opacity',hit?(k>=1?1:.45):.3)});
  scores.forEach(function(n,i){n.setAttribute('opacity',k>=2?(i===2?.3:1):.45)});
  evidence.forEach(function(n){var q=n.getAttribute('data-evidence-flight').split(':').map(Number),i=q[0],j=q[1],u=phase(t,2.3,j*.45);n.setAttribute('cx',162+52*u);n.setAttribute('cy',i===0?145+6*u:218-26*u);n.setAttribute('opacity',k===3?Math.sin(u*Math.PI)*.9:0)});
 });
};
