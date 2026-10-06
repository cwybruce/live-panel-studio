/* Original story illustrations. Geometry and state depend only on seek(t). */
(function(){
 function storyAuthor(e){
 var C=editorialPalette(e);
 function text(x,y,s,size,c,f,attr){var family=f&&f!=='LP Sans'?f+', LP Sans, sans-serif':'LP Sans, sans-serif';return '<text x="'+x+'" y="'+y+'" font-size="'+(size||13)+'" fill="'+(c||C.fg)+'" font-family="'+family+'" font-weight="400" data-component-text="1"'+(attr||'')+'>'+esc(s)+'</text>'}
 function mono(x,y,s,c,attr){return text(x,y,s,10,c||C.dim,'LP Mono',' letter-spacing="1"'+(attr||''))}
 function box(x,y,w,h,c,fill,rx,attr){return '<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="'+(rx==null?4:rx)+'" fill="'+(fill||'none')+'" stroke="'+(c||C.line)+'"'+(attr&&/\bstroke-width\s*=/.test(attr)?'':' stroke-width="1.2"')+(attr||'')+'/>'}
 function line(d,c,attr){return '<path d="'+d+'" fill="none" stroke="'+(c||C.line)+'"'+(attr&&/\bstroke-width\s*=/.test(attr)?'':' stroke-width="1.1"')+(attr||'')+'/>'}
 function badge(x,y,w,s,c){return box(x,y,w,20,c,C.shade('#181611'),3)+text(x+8,y+14,s,10,c,'LP Mono')}
 function section(x,y,w,h,n,title,tag,c){return '<g transform="translate('+x+' '+y+')" data-panel="'+n+'">'+box(0,0,w,h,c,C.panel,5,' data-section-border="'+n+'" data-panel-border="'+n+'" data-neon-border="story-'+tag.toLowerCase()+'" data-neon-color="'+c+'"')+mono(16,26,'0'+(n+1)+' / '+tag,c)+text(16,59,title,19,C.fg,'LP Serif')+line('M16 77H'+(w-16));}
 function defs(id){return '<defs><pattern id="'+id+'grain" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".45" fill="'+C.shade('#75664d')+'" opacity=".17"/></pattern><filter id="'+id+'halo" x="-180%" y="-180%" width="460%" height="460%"><feGaussianBlur stdDeviation="'+(C.light?1.7:3)+'" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter><linearGradient id="'+id+'paper" x1="0" x2="1"><stop stop-color="'+C.shade('#28231b')+'"/><stop offset=".5" stop-color="'+C.shade('#30271d')+'"/><stop offset="1" stop-color="'+C.shade('#1b1813')+'"/></linearGradient></defs>';}
 function header(id,title,sub,note,tags,colors){var s=defs(id)+'<rect width="984" height="1280" fill="'+C.bg+'"/><rect x="18" y="16" width="948" height="1248" fill="url(#'+id+'grain)"/>';
  s+='<g data-diagram-header="1">'+mono(28,29,'MOTION DIAGRAM STUDIO / '+note)+'</g>'+text(28,76,title,31,C.fg,'LP Serif')+text(28,107,sub,14,C.amber)+text(28,134,'用图形展示关键关系；再用例子，检查自己是否真的理解。',12,C.dim);
  tags.forEach(function(a,i){s+=badge(28+i*102,151,92,a,colors[i])});s+=text(956,165,'12 秒循环 / 原创场景',10,C.dim,'LP Sans',' text-anchor="end"');return s;
 }
 function footer(slogan,tag){return '<g data-diagram-footer="1">'+line('M28 1212H956')+text(28,1237,slogan,12,C.fg)+text(28,1259,'原创中文演示 / 所有文本、指标与事件均为预设模拟',10,C.dim)+mono(956,1259,'MOTION DIAGRAM STUDIO · '+tag,C.amber,' text-anchor="end"')+'</g>';}
 function flight(s,id,key,c,count){for(var i=0;i<count;i++)s+='<circle data-'+key+'="'+i+'" r="'+(i?1.8:3)+'" fill="'+c+'" filter="url(#'+id+'halo)"/>';return s;}
 function clamp(x){return Math.max(0,Math.min(1,x))}
 function machine(id){return cfg.machines&&cfg.machines[id]||{}}
 function counterText(id,label,unit){var m=machine(id),value=tv(id);return m.prefix||m.suffix?value:label+value+unit}
 return {C:C,text:text,mono:mono,box:box,line:line,badge:badge,section:section,header:header,footer:footer,flight:flight,clamp:clamp,machine:machine,counterText:counterText};
 }

 B.knowledgeEditorial=function(e){
  var A=storyAuthor(e),C=A.C,text=A.text,mono=A.mono,box=A.box,line=A.line,section=A.section,header=A.header,footer=A.footer,clamp=A.clamp,machine=A.machine,counterText=A.counterText;
  var r=vroot(e),svg=r.svg,id=r.id,colors=[C.amber,C.cyan,C.mint,C.pink];
  var s=header(id,'把一个知识点，翻成看得懂的页','短视频知识卡 · 输入、过程、输出，以及如何核对','THE EXPLAINER / 4 CHAPTERS',['01 输入','02 过程','03 输出','04 回顾'],colors);
  s+=box(28,192,928,360,C.amber,C.shade('#171511'),5,' data-neon-border="knowledge-hero" data-neon-color="'+C.amber+'" data-neon-role="hero"')+mono(43,220,'ONE IDEA / FOUR READABLE CHAPTERS',C.amber)+text(43,252,'让知识展开，而不是让文字堆满屏幕。',20,C.fg,'LP Serif');
  // An open book: multiple page edges, spine, ruled margins and a live right page.
  s+='<g transform="translate(492 363)">';
  for(var p=2;p>=0;p--){var yy=p*3;s+=line('M-254 '+(-74+yy)+'Q-127 '+(-100+yy)+' 0 '+(-62+yy)+'Q127 '+(-100+yy)+' 254 '+(-74+yy)+'V'+(112+yy)+'Q127 '+(88+yy)+' 0 '+(126+yy)+'Q-127 '+(88+yy)+' -254 '+(112+yy)+'Z',C.shade('#61503a'),' opacity="'+(.32+p*.13)+'"');}
  s+='<path d="M-254-78Q-127-105 0-66V122Q-127 84-254 108Z" fill="url(#'+id+'paper)" stroke="'+C.shade('#88704a')+'" stroke-width="1"/><path d="M0-66Q127-105 254-78V108Q127 84 0 122Z" fill="'+C.shade('#201c16')+'" stroke="'+C.shade('#88704a')+'" stroke-width="1"/>';
  s+=line('M0-63V117',C.shade('#c9a86e'),' opacity=".6"')+line('M-227-61Q-114-78-21-52V93M21-52Q114-78 227-61V93',C.shade('#615039'),' opacity=".35"');
  s+=mono(-222,-47,'A SMALL GUIDE',C.amber)+text(-221,-10,'输入、过程、输出',22,C.fg,'LP Serif')+text(-221,19,'一个问题，一组材料。',13,C.dim)+text(-221,43,'让信息走过解释的过程，',13,C.dim)+text(-221,67,'留下可以被核对的结果。',13,C.dim)+text(-221,92,'01 → 02 → 03',11,C.amber,'LP Mono');
  s+=mono(31,-47,'CHAPTER / 01',C.cyan,' data-book-number="1"')+text(31,-15,'明确输入',21,C.fg,'LP Serif',' data-book-title="1"')+text(31,8,'先说明问题与已有材料。',12,C.dim,'LP Sans',' data-book-note="1"');
  [54,133,212].forEach(function(x,i){s+='<circle cx="'+x+'" cy="53" r="19" fill="'+[C.shade('#302619'),C.shade('#183036'),C.shade('#203324')][i]+'" stroke="'+colors[i]+'" stroke-width="1.2" data-book-node="'+i+'"/>'+text(x,58,['问','解','验'][i],14,colors[i],'LP Serif',' text-anchor="middle"');if(i<2)s+=line('M'+(x+20)+' 53H'+(x+58),colors[i],' opacity=".7"');});
  s+=mono(55,87,'IN',C.amber,' text-anchor="middle"')+mono(134,87,'PROCESS',C.cyan,' text-anchor="middle"')+mono(214,87,'CHECK',C.mint,' text-anchor="middle"')+'</g>';
  s+=line('M43 514H940')+text(43,537,'当前 · 明确输入',12,C.amber,'LP Sans',' data-chapter-label="1"')+text(940,537,'演示播放 120 次',11,C.dim,'LP Mono',' text-anchor="end" data-view-count="1"');
  // Concept: the question and its material are two distinct inputs.
  s+=section(28,571,454,294,0,'输入，是问题加上已有材料','INPUT',C.amber);
  s+=box(20,105,155,56,C.amber,C.shade('#251f15'),4)+text(33,128,'需要回答的问题',13,C.amber)+text(33,149,'“怎样找回密码？”',12,C.dim);
  for(var d=0;d<3;d++)s+=box(25+d*6,181-d*6,125,42,d===2?C.cyan:C.shade('#584d3a'),d===2?C.shade('#19272a'):C.shade('#1d1a15'),3);
  s+=text(51,190,'账户帮助文档',12,C.cyan)+line('M183 133H235M181 199C210 199 210 152 235 152',C.amber,' opacity=".7"');
  s+='<circle cx="293" cy="155" r="45" fill="none" stroke="'+C.amber+'" stroke-width="1.1"/><circle cx="293" cy="155" r="53" fill="none" stroke="'+C.amber+'" stroke-dasharray="2 7" opacity=".25"/>'+text(293,150,'明确边界',17,C.fg,'LP Serif',' text-anchor="middle"')+text(293,172,'问什么 · 有什么',11,C.dim,'LP Sans',' text-anchor="middle"');
  s+=text(20,258,'没有材料时，先说明缺口。',13,C.amber)+text(20,280,'输入越具体，后续过程越容易解释和检查。',11,C.dim)+'</g>';
  // Relationship: a narrow, readable process trace rather than another text card.
  s+=section(502,571,454,294,1,'过程，要让关系看得见','PROCESS',C.cyan);
  var px=[67,224,384];px.forEach(function(x,i){s+='<circle cx="'+x+'" cy="147" r="31" fill="'+[C.shade('#302619'),C.shade('#183036'),C.shade('#203324')][i]+'" stroke="'+colors[i]+'" data-process-node="'+i+'"/>'+text(x,153,['问题','解释','结果'][i],15,colors[i],'LP Serif',' text-anchor="middle"')+text(x,197,['保留原意','展示步骤','核对依据'][i],12,C.dim,'LP Sans',' text-anchor="middle"');if(i<2)s+=line('M'+(x+31)+' 147H'+(px[i+1]-31),C.cyan,' opacity=".7"');});
  for(var f=0;f<7;f++)s+='<circle data-process-flight="'+f+'" r="'+(f?1.7:3)+'" fill="'+C.cyan+'" filter="url(#'+id+'halo)"/>';
  s+=line('M20 229H434')+text(20,258,'用流向解释“如何发生”。',13,C.cyan)+text(20,280,'路径、停留和交接，都可以承载信息。',11,C.dim)+'</g>';
  // Example: source and answer must agree, with a visible citation link.
  s+=section(28,885,454,306,2,'输出，不止是看起来像答案','CHECK',C.mint);
  s+=box(20,111,182,83,C.cyan,C.shade('#19272a'),4)+mono(32,132,'SOURCE / 01',C.cyan)+text(32,155,'账户帮助原文',13,C.fg)+text(32,178,'“点击忘记密码”',12,C.dim);
  s+=box(247,111,186,83,C.mint,C.shade('#1b291f'),4)+mono(260,132,'ANSWER / [1]',C.mint)+text(260,155,'选择“忘记密码”',13,C.fg)+text(260,178,'引用 [1] 可以返回原文',11,C.dim);
  s+=line('M203 152H247',C.mint,' stroke-dasharray="2 5"')+'<circle data-citation-dot="1" r="3" fill="'+C.mint+'" filter="url(#'+id+'halo)"/>';
  s+='<g data-output-check="1">'+line('M23 232l7 7 12-15',C.mint,' stroke-width="1.6"')+text(52,236,'检查引用，检查原文，检查结论。',13,C.mint)+'</g>'+text(20,280,'输出要经得起核对，才值得被继续使用。',11,C.dim)+'</g>';
  // Recap: a compact chapter map with different iconography.
  s+=section(502,885,454,306,3,'回顾，然后迁移到自己的问题','RECAP',C.pink);
  var recap=[['问','输入','明确问题与材料'],['连','过程','解释关键关系'],['验','输出','核对结果依据'],['用','迁移','换一个例子再试']];
  recap.forEach(function(a,i){var x=24+(i%2)*215,y=112+Math.floor(i/2)*74;s+='<g data-recap="'+i+'"><circle cx="'+(x+21)+'" cy="'+(y+16)+'" r="19" fill="none" stroke="'+colors[i]+'"/>'+text(x+21,y+21,a[0],15,colors[i],'LP Serif',' text-anchor="middle"')+text(x+51,y+11,a[1],15,C.fg,'LP Serif')+text(x+51,y+32,a[2],11,C.dim)+'</g>';});
  s+=text(20,280,'能换一个场景解释，才说明理解可以迁移。',11,C.dim)+'</g>'+footer('明确输入 · 展示过程 · 核对输出 · 换一个场景再试','STORY / 04');
  svg.innerHTML=s;
  var borders=svg.querySelectorAll('[data-section-border]'),bookNodes=svg.querySelectorAll('[data-book-node]'),processNodes=svg.querySelectorAll('[data-process-node]'),dots=svg.querySelectorAll('[data-process-flight]'),recaps=svg.querySelectorAll('[data-recap]');
  COMPONENTS.push(function(t){var cm=machine('chapter'),period=Math.max(.01,Number(cm.period)||1),chapter=Math.max(0,Math.min(3,Number(V['chapter.i'])||0)),chapterTitle=tv('chapter').replace(/^\s*\d+\s*[/／·]\s*/,''),sec=mod(t,Number(cfg.canvas.duration)||12);
   svg.querySelector('[data-book-number]').textContent='CHAPTER / 0'+(chapter+1);svg.querySelector('[data-book-number]').setAttribute('fill',colors[chapter]);svg.querySelector('[data-book-title]').textContent=chapterTitle;svg.querySelector('[data-book-note]').textContent=tv('chapter.note');
   svg.querySelector('[data-chapter-label]').textContent='当前 · '+chapterTitle;svg.querySelector('[data-chapter-label]').setAttribute('fill',colors[chapter]);svg.querySelector('[data-view-count]').textContent=counterText('views','演示播放 ',' 次');
   borders.forEach(function(n,i){n.setAttribute('stroke',colors[i]);n.setAttribute('stroke-opacity',i===chapter?1:C.light?.8:.85)});
   bookNodes.forEach(function(n,i){n.setAttribute('opacity',chapter===i||chapter===3?1:.85)});processNodes.forEach(function(n){n.setAttribute('opacity',chapter===1||chapter===3?1:.85)});
   dots.forEach(function(n,i){var u=phase(sec,period*.8,i*period*.07);n.setAttribute('cx',98+255*u);n.setAttribute('cy',147);n.setAttribute('opacity',(chapter===1||chapter===3)?Math.sin(u*Math.PI)*(.95-i*.08):.08)});
   var dot=svg.querySelector('[data-citation-dot]'),u=phase(sec,period*.6,0);dot.setAttribute('cx',203+44*u);dot.setAttribute('cy',152);dot.setAttribute('opacity',chapter===2?Math.sin(u*Math.PI):.08);svg.querySelector('[data-output-check]').setAttribute('opacity',1);svg.querySelector('[data-output-check] path').setAttribute('stroke-opacity',chapter===2||chapter===3?1:.75);
   recaps.forEach(function(n,i){n.setAttribute('opacity',1);n.querySelector('circle').setAttribute('stroke-opacity',chapter===3||i===chapter?1:.75)});
  });
 };

 B.workflowEditorial=function(e){
  var A=storyAuthor(e),C=A.C,text=A.text,mono=A.mono,box=A.box,line=A.line,section=A.section,header=A.header,footer=A.footer,clamp=A.clamp,machine=A.machine,counterText=A.counterText;
  var r=vroot(e),svg=r.svg,id=r.id,colors=[C.amber,C.cyan,C.pink,C.mint],xs=[49,279,509,739];
  var s=header(id,'一张工单，走过四个处理站','业务流程 · 从受理、处理、复核，到确认完成','A TICKET’S JOURNEY / 4 STATIONS',['01 受理','02 处理','03 复核','04 完成'],colors);
  s=s.replace('用图形展示关键关系；再用例子，检查自己是否真的理解。','先确认问题，再给出方案；经过复核，才把工单归档。');
  s+=box(28,192,928,422,C.amber,C.shade('#171511'),5,' data-neon-border="workflow-hero" data-neon-color="'+C.amber+'" data-neon-role="hero"')+mono(43,220,'THE SERVICE BOARD / SIX TRAVELLING TICKETS',C.amber)+text(43,252,'每一次转交，都应该带着处理依据。',20,C.fg,'LP Serif');
  var labels=['待受理','处理中','待复核','已完成'];
  xs.forEach(function(x,i){s+=box(x,280,195,265,colors[i],C.shade('#171714'),4,' stroke-opacity=".85"')+text(x+13,305,labels[i],16,colors[i],'LP Serif')+mono(x+181,302,'0'+(i+1),colors[i],' text-anchor="end"')+line('M'+(x+12)+' 319H'+(x+182),colors[i],' opacity=".7"')+text(x+13,530,'00 张',11,C.dim,'LP Mono',' data-lane-count="'+i+'"');if(i<3)s+=line('M'+(x+204)+' 389l9 9-9 9',colors[i],' opacity=".85"');});
  var tickets=['01 · 退款','02 · 登录','03 · 配送','04 · 发票','05 · 地址','06 · 订阅'];
  tickets.forEach(function(a,i){s+='<g data-ticket="'+i+'">'+box(0,0,168,27,C.amber,C.shade('#272117'),3,' data-ticket-face="'+i+'"')+'<circle cx="10" cy="13.5" r="2.3" fill="'+C.amber+'" data-ticket-dot="'+i+'"/>'+text(20,18,a,12,C.fg)+mono(154,18,'↗',C.dim,' text-anchor="end"')+'</g>';});
  s+=line('M43 565H940')+text(43,591,'受理 · 先确认用户问题',12,C.amber,'LP Sans',' data-policy="1"')+text(342,591,'补齐订单编号，确认问题类别。',11,C.dim,'LP Sans',' data-policy-detail="1"')+text(940,591,'收到工单 24 张 · 模拟',11,C.dim,'LP Mono',' text-anchor="end" data-received="1"');
  // Branch assignment topology.
  s+=section(28,634,454,266,0,'先识别问题，再交给合适的人','ASSIGN',C.cyan);
  s+='<circle cx="65" cy="162" r="28" fill="'+C.shade('#2b2418')+'" stroke="'+C.amber+'"/>'+text(65,168,'用户',15,C.amber,'LP Serif',' text-anchor="middle"')+line('M94 162H166',C.amber,' opacity=".7"');
  s+='<polygon points="202,128 236,162 202,196 168,162" fill="'+C.shade('#183036')+'" stroke="'+C.cyan+'"/>'+text(202,166,'分流',14,C.cyan,'LP Serif',' text-anchor="middle"');
  [['退款',C.amber,114],['登录',C.pink,165],['配送',C.mint,216]].forEach(function(a,i){s+=line('M237 162C266 162 256 '+a[2]+' 296 '+a[2],a[1],' data-assign-route="'+i+'"')+'<circle cx="328" cy="'+a[2]+'" r="22" fill="none" stroke="'+a[1]+'"/>'+text(328,a[2]+4,a[0],12,a[1],'LP Sans',' text-anchor="middle"')+mono(380,a[2]+4,['02 / 06','02 / 06','02 / 06'][i],C.dim);});
  s+='<circle data-assign-flight="1" r="3" fill="'+C.cyan+'" filter="url(#'+id+'halo)"/>'+text(20,247,'分类、责任人与材料，随工单一起交接。',11,C.dim)+'</g>';
  // Completion: a thin segmented dial and accurate illustrative count.
  s+=section(502,634,454,266,1,'完成，是被复核过的结果','COMPLETE',C.mint);
  var cx=103,cy=172,rad=55,circ=2*Math.PI*rad;
  s+='<circle cx="'+cx+'" cy="'+cy+'" r="'+rad+'" fill="none" stroke="'+C.shade('#343b2d')+'" stroke-width="12"/><circle cx="'+cx+'" cy="'+cy+'" r="'+rad+'" fill="none" stroke="'+C.mint+'" stroke-width="12" transform="rotate(-90 '+cx+' '+cy+')" data-completion-ring="1"/><circle cx="'+cx+'" cy="'+cy+'" r="68" fill="none" stroke="'+C.mint+'" stroke-dasharray="1 8" opacity=".4"/>'+text(cx,174,'20%',28,C.fg,'LP Serif',' text-anchor="middle" data-completion-percent="1"')+mono(cx,193,'VERIFIED',C.mint,' text-anchor="middle"');
  s+=text(202,142,'06',35,C.mint,'LP Serif',' data-closed-count="1"')+text(264,139,'/ 30',16,C.dim,'LP Mono')+text(202,165,'模拟已完成工单',12,C.fg)+line('M202 184H431')+text(202,208,'先处理，再复核。',13,C.mint)+text(202,231,'数字用于演示，不代表运营统计。',11,C.dim)+'</g>';
  // Review state: an inspection rail with a retriable interruption.
  s+=section(28,920,454,271,2,'复核，是流程中的一道关口','REVIEW',C.pink);
  var rx=[68,225,383];rx.forEach(function(x,i){s+='<circle cx="'+x+'" cy="136" r="23" fill="none" stroke="'+[C.cyan,C.pink,C.mint][i]+'" data-review-node="'+i+'"/>'+text(x,142,['查','核','归'][i],18,[C.cyan,C.pink,C.mint][i],'LP Serif',' text-anchor="middle"')+text(x,179,['核对资料','确认结果','记录归档'][i],12,C.dim,'LP Sans',' text-anchor="middle"');if(i<2)s+=line('M'+(x+23)+' 136H'+(rx[i+1]-23),C.pink,' opacity=".65"');});
  s+=box(20,205,414,38,C.pink,C.shade('#271d23'),3)+text(33,229,'复核处理中 · 核对资料',13,C.pink,'LP Sans',' data-review-label="1"')+'<rect x="20" y="250" width="414" height="2" fill="'+C.shade('#362b30')+'"/><rect x="20" y="250" width="0" height="2" fill="'+C.pink+'" data-review-bar="1"/></g>';
  // Retry: a deliberately visible detour, then a return to review.
  s+=section(502,920,454,271,3,'遇到问题，先补齐再继续','RETRY',C.red);
  s+=box(22,111,115,52,C.cyan,C.shade('#1b2628'),3)+text(35,134,'配送工单',14,C.cyan,'LP Serif')+text(35,152,'核对订单信息',11,C.dim);
  s+=line('M138 137H181',C.red,' stroke-dasharray="3 5"')+box(182,111,103,52,C.red,C.shade('#2a1c17'),3)+text(194,134,'缺少编号',14,C.red,'LP Serif')+text(194,152,'等待补充材料',11,C.dim);
  s+=line('M286 137H318',C.mint)+box(319,111,112,52,C.mint,C.shade('#1e2b21'),3)+text(332,134,'重新复核',14,C.mint,'LP Serif')+text(332,152,'依据完整后继续',11,C.dim);
  s+=line('M233 165V187H76V165',C.red,' opacity=".6"')+text(157,206,'回到处理，补齐缺失资料',11,C.dim,'LP Sans',' text-anchor="middle"');
  s+='<circle data-retry-flight="1" r="3" fill="'+C.red+'" filter="url(#'+id+'halo)"/>'+text(22,248,'当前 · 正常处理',12,C.dim,'LP Sans',' data-retry-label="1"')+'</g>'+footer('确认问题 · 交接依据 · 复核结果 · 遇到缺口先补齐','WORKFLOW / 05');
  svg.innerHTML=s;
  var ticketNodes=svg.querySelectorAll('[data-ticket]'),counts=svg.querySelectorAll('[data-lane-count]'),borders=svg.querySelectorAll('[data-section-border]'),routes=svg.querySelectorAll('[data-assign-route]'),reviewNodes=svg.querySelectorAll('[data-review-node]');
  COMPONENTS.push(function(t){var sec=mod(t,Number(cfg.canvas.duration)||12),policy=Math.max(0,Math.min(2,Number(V['policy.i'])||0)),total=[0,0,0,0];
   ticketNodes.forEach(function(n,i){var u=phase(sec,12,i*1.37),lane=Math.min(3,Math.floor(u*4)),local=u*4-lane,slide=lane<3?smooth(clamp((local-.65)/.35)):0;total[lane]++;
    n.setAttribute('transform','translate('+(xs[lane]+13+slide*230)+' '+(335+(i%5)*34)+')');n.setAttribute('opacity',u>.94?Math.max(0,(1-u)/.06):.95);
    n.querySelector('[data-ticket-face]').setAttribute('stroke',colors[lane]);n.querySelector('[data-ticket-face]').setAttribute('fill',lane===3?C.shade('#203324'):C.shade('#272117'));n.querySelector('[data-ticket-dot]').setAttribute('fill',colors[lane]);n.setAttribute('data-current-lane',lane);
   });counts.forEach(function(n,i){n.textContent=String(total[i]).padStart(2,'0')+' 张'});
   svg.querySelector('[data-policy]').textContent=tv('policy');svg.querySelector('[data-policy]').setAttribute('fill',colors[policy]);svg.querySelector('[data-policy-detail]').textContent=tv('policy.detail');svg.querySelector('[data-received]').textContent=counterText('received','收到工单 ',' 张')+' · 模拟';
   var closed=Math.min(30,6+Math.floor(sec*2)),ratio=closed/30;svg.querySelector('[data-closed-count]').textContent=String(closed).padStart(2,'0');svg.querySelector('[data-completion-percent]').textContent=Math.round(ratio*100)+'%';svg.querySelector('[data-completion-ring]').setAttribute('stroke-dasharray',circ*ratio+' '+circ);
   var policyPeriod=Math.max(.01,Number(machine('policy').period)||1),which=policy,au=phase(sec,policyPeriod*.6,0),assign=svg.querySelector('[data-assign-flight]'),ay=[114,165,216][which];assign.setAttribute('cx',237+59*au);assign.setAttribute('cy',162+(ay-162)*smooth(au));assign.setAttribute('opacity',Math.sin(au*Math.PI));routes.forEach(function(n,i){n.setAttribute('opacity',i===which?1:.6)});
   var rm=machine('review'),reviewPeriod=Math.max(.01,Number(rm.period)||1),run=Math.max(0,Math.min(reviewPeriod,Number(rm.run)||0)),review=mod(t-(Number(rm.off)||0),reviewPeriod),busy=V['review.state']==='busy',progress=busy?(run?clamp(review/run):0):1,reviewStage=busy?(progress<.5?0:1):2;reviewNodes.forEach(function(n,i){n.setAttribute('opacity',i===reviewStage?1:.85)});svg.querySelector('[data-review-label]').textContent=tv('review');svg.querySelector('[data-review-label]').setAttribute('fill',busy?C.pink:C.mint);svg.querySelector('[data-review-bar]').setAttribute('width',414*progress);svg.querySelector('[data-review-bar]').setAttribute('fill',busy?C.pink:C.mint);
   var retry=sec>=5&&sec<9,returning=sec>=9,rd=svg.querySelector('[data-retry-flight]');svg.querySelector('[data-retry-label]').textContent=retry?'当前 · 缺少订单编号，返回补充':returning?'当前 · 编号已补齐，重新进入复核':'当前 · 正常处理，等待核对';svg.querySelector('[data-retry-label]').setAttribute('fill',retry?C.red:returning?C.mint:C.dim);
   if(retry){var ru=phase(sec-5,2,0);rd.setAttribute('cx',233-157*ru);rd.setAttribute('cy',187);rd.setAttribute('fill',C.red);rd.setAttribute('opacity',Math.sin(ru*Math.PI));}else{var ru=phase(sec,2,0);rd.setAttribute('cx',286+33*ru);rd.setAttribute('cy',137);rd.setAttribute('fill',C.mint);rd.setAttribute('opacity',returning?Math.sin(ru*Math.PI):0);}
   borders.forEach(function(n,i){var active=i===policy||(i===3&&retry);n.setAttribute('stroke',[C.cyan,C.mint,C.pink,C.red][i]);n.setAttribute('stroke-opacity',active?1:C.light?.8:.85)});
  });
 };
})();
