/* Original portrait system illustrations. State is derived from machines and t. */
function ESRoot(e, meta, title, subtitle, detail, steps, footer){
 var r=vroot(e),svg=r.svg,id=r.id,C=editorialPalette(e);
 function txt(x,y,s,size,c,face,extra){return '<text x="'+x+'" y="'+y+'" font-size="'+(size||13)+'" fill="'+(c||C.fg)+'" font-family="'+(face||'LP Sans')+'" font-weight="400" data-component-text="1"'+(extra||'')+'>'+esc(s)+'</text>'}
 function mono(x,y,s,size,c,extra){return txt(x,y,s,Math.max(10,size||10),c||C.dim,'LP Mono',extra)}
 function small(x,y,s,c,extra){return mono(x,y,s,10,c||C.dim,' letter-spacing="1"'+(extra||''))}
 function rule(x,y,w){return '<path d="M'+x+' '+y+'h'+w+'" stroke="'+C.line+'" stroke-width="1"/>'}
 function rect(x,y,w,h,c,fill,rx,extra){return '<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="'+(rx==null?3:rx)+'" fill="'+(fill||'none')+'" stroke="'+(c||C.line)+'"'+(extra&&/\bstroke-width\s*=/.test(extra)?'':' stroke-width="1.2"')+(extra||'')+'/>'}
 function panel(x,y,w,h,n,label,title,color){return '<g transform="translate('+x+' '+y+')" data-panel="'+n+'">'+rect(0,0,w,h,color,C.panel,4,' data-panel-border="'+n+'" data-neon-border="'+e.type+'-'+label.toLowerCase().replace(/[^a-z0-9]+/g,'-')+'" data-neon-color="'+color+'"')+small(18,25,'0'+n+' / '+label,color)+txt(18,58,title,title.length>16?17:19,C.fg,'LP Serif')+rule(18,76,w-36)}
 function end(){return '</g>'}
 function circle(x,y,r,c,extra){return '<circle cx="'+x+'" cy="'+y+'" r="'+r+'" fill="none" stroke="'+c+'"'+(extra&&/\bstroke-width\s*=/.test(extra)?'':' stroke-width="1.2"')+(extra||'')+'/>'}
 function icon(kind,x,y,c){var d='';
  if(kind==='plan')d='<circle r="17"/><path d="M-24 0H24M0-24V24M-9 9L9-9L5 5Z"/>';
  if(kind==='search')d='<path d="M-18-19H9L17-11V19H-18Z M9-19V-11H17 M-11-9H5M-11-2H5"/><circle cx="8" cy="9" r="6"/><path d="M12 14L19 21"/>';
  if(kind==='code')d='<path d="M-10-13L-23 0L-10 13M10-13L23 0L10 13M5-18L-5 18"/>';
  if(kind==='check')d='<path d="M-17-17H17V17H-17Z M-9 0L-2 8L11-8"/>';
  if(kind==='query')d='<path d="M-19-14H19V12H-3L-13 20V12H-19Z M-9-5H9M-9 3H4"/>';
  if(kind==='api')d='<path d="M-16-20L16-20L23-9L16 2H-16L-23-9Z M-16 4L16 4L23 15L16 24H-16L-23 15Z"/><circle cx="-9" cy="-9" r="2"/><circle cx="-9" cy="15" r="2"/>';
  if(kind==='cache')d='<rect x="-20" y="-18" width="40" height="36" rx="3"/><path d="M-11-9H-3V-1H-11Z M4-9H12V-1H4Z M-11 6H-3V14H-11Z M4 6H12V14H4Z"/>';
  if(kind==='database')d='<ellipse cy="-14" rx="20" ry="7"/><path d="M-20-14V14C-20 24 20 24 20 14V-14 M-20 0C-20 10 20 10 20 0"/>';
  if(kind==='reply')d='<path d="M-17-21H8L18-11V21H-17Z M8-21V-11H18 M-9 0L-3 6L9-7"/>';
  if(kind==='worker')d='<circle r="18"/><path d="M0-12V0L9 7M-22-22L-27-17M22-22L27-17"/>';
  return '<g transform="translate('+x+' '+y+')" fill="none" stroke="'+c+'" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round">'+d+'</g>';
 }
 function node(x,y,i,c,kind){return '<g data-es-node="'+i+'">'+circle(x,y,56,c,' opacity=".5" data-es-ring="'+i+'"')+circle(x,y,44,c,' opacity=".4" stroke-dasharray="2 8"')+'<circle cx="'+x+'" cy="'+y+'" r="34" fill="url(#'+id+'orb'+i+')" stroke="'+c+'" stroke-width="1.3"/>'+icon(kind,x,y,C.shade('#f0e7d8'))+'</g>'}
 function route(key,d,c){return '<path data-es-route="'+key+'" d="'+d+'" fill="none" stroke="'+c+'" stroke-width="1.3" opacity=".55"/>'}
 function particles(key,c,n){var s='';for(var j=0;j<(n||5);j++)s+='<circle data-es-flight="'+key+':'+j+'" r="'+(j===0?2.6:1.2)+'" fill="'+c+'" filter="url(#'+id+'halo)"/>';return s}
 var colors=[C.amber,C.cyan,C.pink,C.mint,C.mint];
 var s='<defs><pattern id="'+id+'grid" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".4" fill="'+C.shade('#76654b')+'" opacity=".14"/></pattern><filter id="'+id+'halo" x="-180%" y="-180%" width="460%" height="460%"><feGaussianBlur stdDeviation="'+(C.light?1.7:3)+'" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>';
 colors.forEach(function(c,i){s+='<radialGradient id="'+id+'orb'+i+'" cx="30%" cy="25%"><stop stop-color="'+c+'" stop-opacity="'+(C.light?'.24':'.58')+'"/><stop offset="1" stop-color="'+C.shade('#171512')+'"/></radialGradient>'});s+='</defs>';
 s+='<rect width="984" height="1280" fill="'+C.bg+'"/><rect x="18" y="16" width="948" height="1248" fill="url(#'+id+'grid)"/><g data-diagram-header="1">'+small(28,29,meta)+'</g>'+txt(28,76,title,31,C.fg,'LP Serif')+txt(28,107,subtitle,14,C.amber)+txt(28,134,detail,12,C.dim);
 steps.forEach(function(a,i){s+=small(28+i*122,164,a[0],C.shade(a[1]))});s+=mono(956,164,'12s / SCRIPTED LOOP',9,C.dim,' text-anchor="end"');
 s+='<g data-panel="hero">'+rect(28,194,928,383,C.amber,C.shade('#171511'),4,' data-panel-border="hero" data-neon-border="'+e.type+'-hero" data-neon-color="'+C.amber+'" data-neon-role="hero"')+small(42,219,'THE SYSTEM IN MOTION',C.amber)+rule(43,531,897);
 var edition={agentEditorial:'COLLABORATION / 02',requestEditorial:'REQUEST / 03',incidentEditorial:'REPLAY / 04'};
 var tail='<g data-diagram-footer="1">'+rule(28,1212,928)+txt(28,1237,footer,12,C.fg)+txt(28,1259,'原创中文视觉示例 / 所有文本、指标与事件均为预设演示',10,C.dim)+mono(956,1259,'MOTION DIAGRAM STUDIO / '+edition[e.type],9,C.amber,' text-anchor="end"')+'</g>';
 return {svg:svg,id:id,C:C,txt:txt,mono:mono,small:small,rule:rule,rect:rect,panel:panel,end:end,circle:circle,icon:icon,node:node,route:route,particles:particles,s:s,tail:tail};
}
function ESValue(name){var v=V[name];return v==null?'':typeof v==='object'?v.text:String(v)}
function ESFlights(svg){var paths={};svg.querySelectorAll('[data-es-route]').forEach(function(p){paths[p.getAttribute('data-es-route')]={p:p,len:p.getTotalLength()}});return {paths:paths,dots:Array.prototype.slice.call(svg.querySelectorAll('[data-es-flight]'))}}
function ESAnimateFlights(f,t,active){Object.keys(f.paths).forEach(function(key){f.paths[key].p.setAttribute('opacity',active(key)? .95:.55)});f.dots.forEach(function(n){var a=n.getAttribute('data-es-flight').split(':'),key=a[0],j=Number(a[1]),u=phase(t,2.2,-j*.14),p=f.paths[key].p.getPointAtLength(f.paths[key].len*u);n.setAttribute('cx',p.x);n.setAttribute('cy',p.y);n.setAttribute('opacity',active(key)?Math.sin(u*Math.PI)*(.94-j*.14):0)})}

B.agentEditorial=function(e){
 var a=ESRoot(e,'MOTION DIAGRAM STUDIO / COLLABORATION / FOUR ROLES','一次任务，如何交到下一双手','多 Agent · 让状态、建议与验收依据一起交接','四种角色轮流工作；交付时，成果应当带着可以复现的证据。',[['01 / PLAN','#dfb96d'],['02 / RESEARCH','#64bed0'],['03 / BUILD','#e776af'],['04 / REVIEW','#88c4a2']], '角色划分职责 · 交接携带依据 · 时间线同步状态 · 结果需要验收'),s=a.s,C=a.C,T=a.txt,M=a.mono,R=a.rect,S=a.small;
 var xs=[145,376,607,838],colors=[C.amber,C.cyan,C.pink,C.mint],names=['规划','检索','实现','审核'],desc=['定义可验收的目标','补齐接口与来源','按约束编写补丁','核对边界与结果'];
 s+=T(42,253,'把分工变成一条可追踪的交付链。',20,C.fg,'LP Serif')+M(942,219,'GOAL → CONTEXT → PATCH → CHECK',9,C.dim,' text-anchor="end"');
 for(var i=0;i<3;i++){s+=a.route(String(i),'M'+(xs[i]+43)+' 339C'+(xs[i]+85)+' 294 '+(xs[i+1]-85)+' 294 '+(xs[i+1]-43)+' 339',colors[i])+a.particles(String(i),colors[i])}
 xs.forEach(function(x,i){s+=a.node(x,339,i,colors[i],['plan','search','code','check'][i])+S(x,281,['DEFINE / 01','SEARCH / 02','IMPLEMENT / 03','VERIFY / 04'][i],colors[i],' text-anchor="middle"')+T(x,416,names[i]+'角色',14,colors[i],null,' text-anchor="middle"')+T(x,440,'',12,C.dim,null,' text-anchor="middle" data-agent-status="'+i+'"')});
 s+=T(43,555,'',12,C.amber,null,' data-agent-phase="1"')+T(940,555,'',11,C.dim,null,' text-anchor="end" data-agent-task="1"');
 s+=a.end()+a.panel(28,596,454,284,1,'DECOMPOSE','一个目标，三个验收落点',C.amber)+S(18,101,'ONE GOAL / THREE ACCEPTANCE CHECKS');
 s+=a.circle(227,136,20,C.amber)+a.icon('plan',227,136,C.amber)+'<path d="M227 157V180H92V190M227 180V190M227 180H362V190" fill="none" stroke="'+C.line+'" stroke-width="1.1"/>';
 ['接口可用','边界明确','结果可复现'].forEach(function(n,i){var x=[92,227,362][i];s+='<g data-acceptance="'+i+'">'+a.circle(x,208,16,[C.cyan,C.pink,C.mint][i])+'<path d="M'+(x-6)+' 208l4 5 9-12" fill="none" stroke="'+[C.cyan,C.pink,C.mint][i]+'" stroke-width="1"/>'+T(x,242,n,12,C.fg,null,' text-anchor="middle"')+'</g>'});s+=T(18,269,'拆小任务，也保留最终结果的验收条件。',12,C.dim)+a.end();
 s+=a.panel(502,596,454,284,2,'TIME LANES','交接按顺序，结果按时间核对',C.cyan)+S(18,101,'A SCRIPTED HANDOFF / 0—12 SECONDS');
 for(var i=0;i<4;i++){var y=127+i*31;s+=T(18,y+5,names[i],12,C.dim)+R(106,y-4,322,9,'none',C.shade('#292620'),1)+'<rect data-agent-lane="'+i+'" x="'+(106+i*80.5)+'" y="'+(y-4)+'" width="'+(i===3?48.3:80.5)+'" height="9" rx="1" fill="'+colors[i]+'" opacity=".35"/>'}
 [0,3,6,9,12].forEach(function(n,i){s+=M(106+i*80.5,256,String(n)+'s',9,C.dim,' text-anchor="middle"')});s+='<path data-agent-cursor="1" d="M106 115V240" stroke="'+C.fg+'" stroke-width="1.1" stroke-dasharray="2 4"/>'+a.end();
 s+=a.panel(28,900,454,286,3,'HANDOFF PACKAGE','成果，连同依据一起走',C.pink)+S(18,101,'CONTRACT / CONTEXT / REPRODUCTION');
 s+='<path d="M80 143L227 175L372 143M227 175V225" fill="none" stroke="'+C.line+'" stroke-width="1.1"/>';
 [[80,143,'验收条件',C.amber],[372,143,'资料来源',C.cyan],[227,235,'复现方法',C.mint]].forEach(function(q){s+=a.circle(q[0],q[1],9,q[3])+T(q[0],q[1]+27,q[2],12,q[3],null,' text-anchor="middle"')});
 s+='<g data-handoff-paper="1">'+R(203,151,48,53,C.pink,C.shade('#251c21'),3)+R(210,144,48,53,C.pink,C.shade('#251c21'),3)+'<path d="M220 160H246M220 168H246M220 176H239" stroke="'+C.pink+'" stroke-width="1.1"/></g>'+T(18,279,'交接对象既是产物，也是它成立的证据。',11,C.dim)+a.end();
 s+=a.panel(502,900,454,286,4,'EVENT REPLAY','每次交接，都有一个明确的事件',C.mint)+S(18,101,'ADVICE AND EVENTS / SIMULATED');
 s+='<path d="M29 123V219" stroke="'+C.line+'" stroke-width="1.1"/>';
 names.forEach(function(n,i){var yy=126+i*28;s+='<circle data-agent-event="'+i+'" cx="29" cy="'+(yy-3)+'" r="3" fill="'+colors[i]+'"/>'+M(43,yy,'00:0'+(i*3),10,C.dim)+T(108,yy,n+'：'+['定义验收条件','交付接口证据','交付最小补丁','核对并准备交付'][i],12,C.fg,null,' data-agent-event-text="'+i+'"')});
 s+=T(18,252,'',12,C.fg,null,' data-agent-advice="0"')+T(18,274,'',12,C.dim,null,' data-agent-advice="1"')+a.end()+a.tail;a.svg.innerHTML=s;
 var flights=ESFlights(a.svg),rings=a.svg.querySelectorAll('[data-es-ring]'),nodes=a.svg.querySelectorAll('[data-es-node]'),statuses=a.svg.querySelectorAll('[data-agent-status]'),lanes=a.svg.querySelectorAll('[data-agent-lane]'),events=a.svg.querySelectorAll('[data-agent-event]'),eventText=a.svg.querySelectorAll('[data-agent-event-text]'),accept=a.svg.querySelectorAll('[data-acceptance]');
 COMPONENTS.push(function(t){var sec=mod(t,12),k=Number(ESValue('handoff.cur'))||0,done=ESValue('task.state')==='done';
  a.svg.querySelector('[data-agent-phase]').textContent='当前 · '+names[k]+'角色';a.svg.querySelector('[data-agent-phase]').setAttribute('fill',colors[k]);a.svg.querySelector('[data-agent-task]').textContent=done?'✓ 本轮已交付':'四种职责，沿着时间线依次完成';
  nodes.forEach(function(n){n.setAttribute('opacity',1)});rings.forEach(function(n,i){n.setAttribute('r',56+(i===k?Math.sin(t*1.5)*2:0));n.setAttribute('opacity',i===k?.95:.5)});statuses.forEach(function(n,i){n.textContent=ESValue('role'+i)});
  ESAnimateFlights(flights,t,function(key){return Number(ESValue('handoff.active'))===Number(key)});
  lanes.forEach(function(n,i){n.setAttribute('opacity',i===k?1:i<k?.88:.7)});a.svg.querySelector('[data-agent-cursor]').setAttribute('transform','translate('+(322*Math.min(1,sec/12))+' 0)');
  events.forEach(function(n,i){n.setAttribute('opacity',i<=k?1:.65)});eventText.forEach(function(n){n.setAttribute('opacity',1)});accept.forEach(function(n,i){n.setAttribute('opacity',1);n.querySelector('circle').setAttribute('opacity',done?1:.75+.1*Math.sin(t*1.2+i))});
  a.svg.querySelector('[data-handoff-paper]').setAttribute('transform','translate(0 '+Math.sin(t*1.3)*2+')');a.svg.querySelector('[data-agent-advice="0"]').textContent=ESValue('handoff.adv0');a.svg.querySelector('[data-agent-advice="1"]').textContent=ESValue('handoff.adv1');
 });
};

B.requestEditorial=function(e){
 var a=ESRoot(e,'MOTION DIAGRAM STUDIO / REQUEST ROUTING / TWO BRANCHES','一次请求，走捷径或回到源头','缓存 · 复用已有结果，也保留读取原始数据的路径','命中和未命中走不同分支，最终汇成同一种响应格式。', [['01 / HIT','#88c4a2'],['02 / MISS','#e776af'],['03 / RETURN','#64bed0']], '命中复用结果 · 未命中读取源头 · 两路统一响应 · 指标标明来源'),s=a.s,C=a.C,T=a.txt,M=a.mono,R=a.rect,S=a.small;
 s+=T(42,253,'分支不同，返回结果的约定一致。',20,C.fg,'LP Serif')+M(942,219,'REQUEST → CACHE / DATABASE → RESPONSE',9,C.dim,' text-anchor="end"');
 var routes=[['in','M167 353H302',C.amber],['lookup','M383 339C445 298 488 298 544 298',C.cyan],['hit','M586 340V386',C.mint],['miss','M628 304C708 292 750 313 797 341',C.pink],['read','M807 383C748 421 690 426 628 426',C.pink],['return','M544 430C410 491 217 488 139 393',C.mint]];
 routes.forEach(function(q){s+=a.route(q[0],q[1],q[2])+a.particles(q[0],q[2])});
 [[124,353,0,C.amber,'query','客户端',414,'保留请求的原意'],[342,353,1,C.cyan,'api','API 服务',414,'校验参数与选择分支'],[586,298,3,C.mint,'cache','缓存',236,'已有结果可复用'],[838,353,2,C.pink,'database','数据库',414,'读取原始库存记录'],[586,426,4,C.mint,'reply','',479,'']].forEach(function(q){s+=a.node(q[0],q[1],q[2],q[3],q[4]);if(q[5])s+=T(q[0],q[6],q[5],14,q[3],null,' text-anchor="middle"');if(q[7])s+=T(q[0],q[6]+21,q[7],11,C.dim,null,' text-anchor="middle"')});
 s+=T(648,462,'统一响应',14,C.mint);
 s+=M(609,363,'HIT',9,C.mint)+M(711,287,'MISS',9,C.pink)+T(43,555,'',12,C.amber,null,' data-request-phase="1"')+T(940,555,'预设分支 / 不连接业务服务',11,C.dim,null,' text-anchor="end"');
 s+=a.end()+a.panel(28,596,454,284,1,'KEY / VALUE','命中，是找到一份可以复用的结果',C.mint)+S(18,101,'A TINY CACHE / EIGHT AUTHORED KEYS');
 for(var i=0;i<8;i++){var x=27+i%4*48,y=124+Math.floor(i/4)*52;s+='<g data-cache-key="'+i+'">'+R(x,y,35,37,i===4?C.mint:C.line,i===4?C.shade('#1c2b21'):'none',2)+M(x+17.5,y+16,'K'+String(i+1),9,i===4?C.mint:C.dim,' text-anchor="middle"')+'<path d="M'+(x+8)+' '+(y+25)+'h19" stroke="'+(i===4?C.mint:C.line)+'" stroke-width="1.1"/></g>'}
 s+='<path d="M228 195C247 195 248 152 269 152" stroke="'+C.mint+'" stroke-width="1.1" fill="none"/>'+R(270,122,166,67,C.mint,C.shade('#1b241b'),3)+M(280,141,'ITEM / K5',10,C.mint)+T(280,163,'库存：24 件',13,C.fg)+T(280,181,'已有查询结果',11,C.dim)+T(18,269,'能否复用，取决于键、有效期与业务规则。',11,C.dim)+a.end();
 s+=a.panel(502,596,454,284,2,'SOURCE OF TRUTH','没有命中，再读取原始记录',C.pink)+S(18,101,'MISS → READ → NORMALIZE');
 s+=a.icon('database',90,165,C.pink)+a.circle(90,165,38,C.pink,' opacity=".35"')+'<path d="M134 165H231" stroke="'+C.pink+'" stroke-width="1.1"/>';
 for(var i=0;i<3;i++){s+='<g data-database-record="'+i+'">'+R(252+i*10,133+i*8,140,65,C.line,C.shade('#1b1815'),3)+(i===2?M(282,169,'ROW / 3',9,C.pink):'')+'<path d="M'+(262+i*10)+' '+(166+i*8)+'h109m-109 9h82" stroke="'+C.line+'" stroke-width="1.1"/></g>'}
 s+=T(90,224,'原始数据',12,C.pink,null,' text-anchor="middle"')+T(278,239,'读取与格式整理',12,C.fg)+T(18,269,'此处只是查询机制示例，不读取实际库存。',11,C.dim)+a.end();
 s+=a.panel(28,900,454,286,3,'MERGE THE BRANCHES','两条路径，一种返回格式',C.cyan)+S(18,101,'CACHE OR DATABASE / SAME RESPONSE');
 s+='<path d="M46 144C126 144 149 177 229 177" stroke="'+C.mint+'" stroke-width="8" opacity=".13" fill="none"/><path d="M46 219C126 219 149 177 229 177" stroke="'+C.pink+'" stroke-width="8" opacity=".13" fill="none"/>';
 s+='<path data-merge-hit="1" d="M46 144C126 144 149 177 229 177" stroke="'+C.mint+'" stroke-width="1.2" fill="none"/><path data-merge-miss="1" d="M46 219C126 219 149 177 229 177" stroke="'+C.pink+'" stroke-width="1.2" fill="none"/>'+a.circle(231,177,8,C.cyan)+'<path d="M239 177H277" stroke="'+C.cyan+'" stroke-width="1.1"/>';
 s+=T(30,132,'命中缓存',12,C.mint)+T(30,244,'读取数据库',12,C.pink)+R(278,126,150,103,C.cyan,C.shade('#182326'),3)+M(291,145,'RESPONSE',10,C.cyan)+M(291,170,'status: 200',11,C.fg)+M(291,192,'stock: 24',11,C.fg)+T(291,214,'输出约定一致',12,C.dim)+T(18,279,'机制解释与真实接口运行，应当分别验证。',11,C.dim)+a.end();
 s+=a.panel(502,900,454,286,4,'ILLUSTRATIVE COUNTER','每个数字，都应当说清它的来源',C.amber)+S(18,101,'A COUNTER / EIGHTEEN REQUESTS PER SECOND');
 s+=M(18,161,'000',43,C.amber,' data-request-count="1"')+T(155,152,'次模拟请求',13,C.fg)+M(155,175,'18 / SECOND',10,C.dim)+R(18,199,417,1,'none',C.line,0);
 s+='<path d="M18 234L435 203" fill="none" stroke="'+C.amber+'" stroke-width="1.1" opacity=".7"/><circle data-request-count-dot="1" r="3" fill="'+C.amber+'" filter="url(#'+a.id+'halo)"/>'+M(18,251,'0s',9,C.dim)+M(435,251,'12s',9,C.dim,' text-anchor="end"')+T(18,279,'独立计数器演示；这些数字不是线上流量。',11,C.dim)+a.end()+a.tail;a.svg.innerHTML=s;
 var flights=ESFlights(a.svg),keys=a.svg.querySelectorAll('[data-cache-key]'),records=a.svg.querySelectorAll('[data-database-record]'),nodes=a.svg.querySelectorAll('[data-es-node]'),rings=a.svg.querySelectorAll('[data-es-ring]');
 COMPONENTS.push(function(t){var sec=mod(t,12),k=Number(ESValue('route.i'))||0;
  a.svg.querySelector('[data-request-phase]').textContent='当前 · '+ESValue('route');a.svg.querySelector('[data-request-phase]').setAttribute('fill',[C.mint,C.pink,C.cyan][k]);
  ESAnimateFlights(flights,t,function(key){return (key==='in'||key==='lookup')?k<2:(key==='hit'?k===0:(key==='miss'||key==='read')?k===1:k===2)});
  nodes.forEach(function(n){n.setAttribute('opacity',1)});rings.forEach(function(n){var i=Number(n.getAttribute('data-es-ring')),on=(i===3&&k===0)||(i===2&&k===1)||(i===4&&k===2);n.setAttribute('r',56+(on?Math.sin(t*1.4)*2:0));n.setAttribute('opacity',on?.95:.5)});
  keys.forEach(function(n,i){n.setAttribute('opacity',1);n.querySelector('rect').setAttribute('stroke-opacity',i===4?(k===0?1:.8):.75)});records.forEach(function(n,i){n.setAttribute('opacity',1);n.querySelector('rect').setAttribute('stroke-opacity',k===1?.88+.1*Math.sin(t*1.8-i):.75)});a.svg.querySelector('[data-merge-hit]').setAttribute('opacity',k===0?1:.6);a.svg.querySelector('[data-merge-miss]').setAttribute('opacity',k===1?1:.6);
  a.svg.querySelector('[data-request-count]').textContent=ESValue('requests').padStart(3,'0');var dot=a.svg.querySelector('[data-request-count-dot]'),u=sec/12;dot.setAttribute('cx',18+417*u);dot.setAttribute('cy',234-31*u);
 });
};

B.incidentEditorial=function(e){
 var a=ESRoot(e,'MOTION DIAGRAM STUDIO / INCIDENT REPLAY / DEPENDENCY CHAIN','一次异常，如何沿着依赖显形','回放 · 从服务稳定，到拥塞，再到恢复检查','用余量驱动状态，让异常路径与恢复证据出现在同一条时间线上。',[['01 / HEALTHY','#88c4a2'],['02 / DEGRADED','#d77768'],['03 / RECOVER','#64bed0']], '阈值驱动告警 · 依赖呈现传播 · 回放复现过程 · 恢复后仍需验收'),s=a.s,C=a.C,T=a.txt,M=a.mono,R=a.rect,S=a.small;
 var machines=cfg.machines,poolMachine=machines.pool,storageMachine=machines.storage,duration=cfg.canvas.duration||12;
 var thresholds={pool:Number(poolMachine.threshold),storage:Number(storageMachine.threshold)},phasePeriod=machines.phase.period;
 s+=T(42,253,'让指标变成可定位的状态。',20,C.fg,'LP Serif')+M(942,219,'ENTRY → WORK POOL → STORAGE',9,C.dim,' text-anchor="end"');
 var xs=[176,492,808];for(var i=0;i<2;i++){s+=a.route(String(i),'M'+(xs[i]+44)+' 339H'+(xs[i+1]-44),C.mint)+a.particles(String(i),C.mint)}
 xs.forEach(function(x,i){s+=a.node(x,339,i,[C.amber,C.cyan,C.pink][i],['api','worker','database'][i])+S(x,281,['ENTRY SERVICE','EXECUTION POOL','SOURCE STORAGE'][i],C.dim,' text-anchor="middle"')+T(x,419,['入口服务','工作池','存储服务'][i],14,C.fg,null,' text-anchor="middle"')+T(x,442,['请求持续进入','', ''][i],12,C.dim,null,' text-anchor="middle" data-incident-node-label="'+i+'"')});
 var thresholdNote=thresholds.pool===thresholds.storage?'任一余量低于 '+thresholds.pool.toFixed(2)+' → 标记异常依赖':'工作池 '+thresholds.pool.toFixed(2)+' / 存储 '+thresholds.storage.toFixed(2)+' → 阈值告警';
 s+=T(43,555,'',12,C.mint,null,' data-incident-phase="1"')+T(940,555,thresholdNote,11,C.dim,null,' text-anchor="end"');
 s+=a.end()+a.panel(28,596,928,284,1,'METRIC REPLAY','余量变化，要能沿时间追溯',C.cyan)+S(18,101,'SCRIPTED HEADROOM / 0—'+duration+' SECONDS')+M(892,101,'POOL ≥ '+thresholds.pool.toFixed(2),10,C.mint,' text-anchor="end"')+M(776,101,'STORAGE ≥ '+thresholds.storage.toFixed(2),10,C.cyan,' text-anchor="end"');
 var gx=74,gy=131,gw=827,gh=110,scale=function(v){return gy+(1-v)*gh};
 [.0,.35,1].forEach(function(v){s+='<path d="M'+gx+' '+scale(v)+'H'+(gx+gw)+'" stroke="'+C.line+'" stroke-width=".8" opacity=".8"/>'+M(52,scale(v)+3,v.toFixed(2),9,C.dim,' text-anchor="end"')});
 [thresholds.pool,thresholds.storage].filter(function(v,i,arr){return arr.indexOf(v)===i}).forEach(function(v){s+='<path data-incident-threshold="'+v+'" d="M'+gx+' '+scale(v)+'H'+(gx+gw)+'" stroke="'+C.red+'" stroke-width="1.1" stroke-dasharray="3 5"/>'});
 s+='<rect x="'+(gx+gw*Math.min(phasePeriod,duration)/duration)+'" y="'+gy+'" width="'+(gw*Math.min(phasePeriod,Math.max(0,duration-phasePeriod))/duration)+'" height="'+gh+'" fill="'+C.red+'" opacity=".05"/>';
 function chart(machine,c,name){
  var at=function(t){var k=Math.floor((t-(machine.t0||0))/machine.period);return Number(machine.values[pickIdx(machine,k)])},d='M'+gx+' '+scale(at(0)),samples=[at(0)];
  var first=(machine.t0||0)+(Math.floor(-(machine.t0||0)/machine.period)+1)*machine.period;
  for(var t=first;t<duration;t+=machine.period){var value=at(t);d+='H'+(gx+gw*t/duration)+'V'+scale(value);samples.push(value)}d+='H'+(gx+gw);
  return '<path data-incident-history="'+name+'" data-incident-values="'+samples.join(',')+'" d="'+d+'" fill="none" stroke="'+c+'" stroke-width="1.6" opacity=".85"/>';
 }
 s+=chart(poolMachine,C.mint,'pool')+chart(storageMachine,C.cyan,'storage')+'<path data-incident-cursor="1" d="M'+gx+' '+(gy-5)+'V'+(gy+gh+4)+'" stroke="'+C.fg+'" stroke-width=".75" stroke-dasharray="2 4"/>';
 for(var tick=0;tick<=duration;tick+=phasePeriod)s+=M(gx+gw*tick/duration,263,String(tick)+'s',9,C.dim,' text-anchor="middle"');
 s+='<circle data-incident-point="pool" r="3.5" fill="'+C.mint+'"/><circle data-incident-point="storage" r="3.5" fill="'+C.cyan+'"/>'+a.end();
 s+=a.panel(28,900,454,286,2,'THRESHOLD RELATION','低于阈值，让依赖链变成告警',C.red)+S(18,101,'ONE LOW METRIC IS ENOUGH');
 [[127,'pool','工作池',C.mint],[329,'storage','存储服务',C.cyan]].forEach(function(q){var circumference=2*Math.PI*42;s+=a.circle(q[0],176,42,C.line,' stroke-width="3"')+'<circle data-incident-gauge="'+q[1]+'" cx="'+q[0]+'" cy="176" r="42" fill="none" stroke="'+q[3]+'" stroke-width="3" transform="rotate(-90 '+q[0]+' 176)" stroke-dasharray="'+circumference+' '+circumference+'"/>';
  var ang=-Math.PI/2+Math.PI*2*thresholds[q[1]];s+='<path data-incident-gauge-threshold="'+q[1]+'" d="M'+(q[0]+Math.cos(ang)*37)+' '+(176+Math.sin(ang)*37)+'L'+(q[0]+Math.cos(ang)*47)+' '+(176+Math.sin(ang)*47)+'" stroke="'+C.red+'" stroke-width="1"/>'+M(q[0],184,'',27,q[3],' text-anchor="middle" data-incident-number="'+q[1]+'"')+T(q[0],241,q[2],12,C.fg,null,' text-anchor="middle"')});
 s+=T(18,279,'',11,C.dim,null,' data-incident-threshold-label="1"')+a.end();
 s+=a.panel(502,900,454,286,3,'RECOVERY CHECKS','恢复服务，也要留下验收空间',C.mint)+S(18,101,'RECOVERY ≠ BUSINESS ACCEPTANCE');
 s+='<path d="M29 122V189" stroke="'+C.line+'" stroke-width="1.1"/>';
 ['健康检查通过','余量下降，标记依赖异常','余量回升，开始恢复检查'].forEach(function(n,i){var y=127+i*29;s+='<circle data-incident-event="'+i+'" cx="29" cy="'+(y-4)+'" r="3" fill="'+[C.mint,C.red,C.cyan][i]+'"/>'+M(43,y,'00:0'+(i*4),10,C.dim)+T(111,y,n,12,C.fg,null,' data-incident-event-text="'+i+'"')});
 [[35,'余量回升'],[173,'依赖通畅'],[315,'结果核对']].forEach(function(q,i){s+='<circle data-recovery-check="'+i+'" cx="'+q[0]+'" cy="229" r="5" fill="none" stroke="'+(i===2?C.amber:C.mint)+'" stroke-width="1.1"/>'+T(q[0]+12,233,q[1],11,i===2?C.amber:C.dim)});
 s+=T(18,279,'恢复回放结束，业务结果仍需另行验收。',11,C.dim)+a.end()+a.tail;a.svg.innerHTML=s;
 var flights=ESFlights(a.svg),rings=a.svg.querySelectorAll('[data-es-ring]'),gauge=a.svg.querySelectorAll('[data-incident-gauge]'),events=a.svg.querySelectorAll('[data-incident-event]'),eventText=a.svg.querySelectorAll('[data-incident-event-text]'),checks=a.svg.querySelectorAll('[data-recovery-check]');
 COMPONENTS.push(function(t){var sec=mod(t,duration),k=Number(ESValue('phase.i')),low=ESValue('health')==='low',pool=Number(ESValue('pool')),storage=Number(ESValue('storage')),statusColor=low?C.red:C.mint;
  var phaseLabel=a.svg.querySelector('[data-incident-phase]');phaseLabel.textContent='当前 · '+ESValue('phase');phaseLabel.setAttribute('fill',statusColor);
  ESAnimateFlights(flights,t,function(){return true});Object.keys(flights.paths).forEach(function(key){flights.paths[key].p.setAttribute('stroke',statusColor)});flights.dots.forEach(function(n){n.setAttribute('fill',statusColor)});
  rings.forEach(function(n,i){n.setAttribute('stroke',i===0?C.amber:statusColor);n.setAttribute('opacity',low&&i>0?.85+.1*Math.sin(t*2.4):.55);n.setAttribute('r',56+(low&&i>0?Math.sin(t*2.4)*1.5:0))});
  a.svg.querySelector('[data-incident-node-label="1"]').textContent='可用余量 '+pool.toFixed(2);a.svg.querySelector('[data-incident-node-label="2"]').textContent='可用余量 '+storage.toFixed(2);
  var x=gx+gw*sec/duration;a.svg.querySelector('[data-incident-cursor]').setAttribute('transform','translate('+(x-gx)+' 0)');['pool','storage'].forEach(function(name,i){var n=a.svg.querySelector('[data-incident-point="'+name+'"]'),v=i===0?pool:storage;n.setAttribute('cx',x);n.setAttribute('cy',scale(v));a.svg.querySelector('[data-incident-number="'+name+'"]').textContent=v.toFixed(2)});
  gauge.forEach(function(n){var name=n.getAttribute('data-incident-gauge'),value=name==='pool'?pool:storage;n.setAttribute('stroke-dasharray',(2*Math.PI*42*value)+' '+(2*Math.PI*42));n.setAttribute('stroke',value<thresholds[name]?C.red:name==='pool'?C.mint:C.cyan)});
  a.svg.querySelector('[data-incident-threshold-label]').textContent=low?'任一余量低于各自阈值：触发异常标记。':'两项余量均达到阈值：继续核对运行结果。';
  events.forEach(function(n,i){n.setAttribute('opacity',i<=k?1:.65)});eventText.forEach(function(n){n.setAttribute('opacity',1)});checks.forEach(function(n,i){n.setAttribute('fill',k===2&&i<2?C.mint:'none');n.setAttribute('opacity',i===2?1:k===2?1:.75)});
 });
};
