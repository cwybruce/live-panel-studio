/* Original editorial wrappers around the existing reusable vector components.
 * No network or clock state: every moving detail is drawn from seek(t). */
function ecPalette(e){
 return editorialPalette(e);
}
function ecAuthor(root,C){
 function txt(x,y,s,size,color,face,b,extra){return '<text x="'+x+'" y="'+y+'" font-size="'+(size||12)+'" fill="'+(color||C.fg)+'" font-family="'+(face==='serif'?'LP Serif, LP Sans':face==='mono'?'LP Mono, LP Sans':'LP Sans')+'"'+(b?' font-weight="600"':'')+(extra||'')+' data-component-text="1">'+esc(s)+'</text>'}
 function meta(x,y,s,color,extra){return txt(x,y,s,9,color||C.dim,'mono',false,' letter-spacing="1.1"'+(extra||''))}
 function rect(x,y,w,h,fill,stroke,rx,extra){return '<rect x="'+x+'" y="'+y+'" width="'+w+'" height="'+h+'" rx="'+(rx==null?4:rx)+'" fill="'+(fill||'none')+'" stroke="'+(stroke||C.line)+'" stroke-width=".8"'+(extra||'')+'/>'}
 function panel(x,y,w,h,index,title,caption,color){return '<g transform="translate('+x+' '+y+')">'+rect(0,0,w,h,C.panel,C.line,4,' data-neon-border="component-'+index.toLowerCase().replace(/[^a-z0-9]+/g,'-')+'" data-neon-color="'+color+'"')+meta(15,24,index,color)+txt(15,55,title,18,C.fg,'serif',true)+txt(w-15,24,caption,9,C.dim,'mono',false,' text-anchor="end"')+'</g>'}
 function page(title,sub,description,kicker){return '<rect width="984" height="1280" fill="'+C.bg+'"/>'+meta(28,29,kicker)+txt(28,77,title,31,C.fg,'serif',true)+txt(28,106,sub,14,C.amber)+txt(28,135,description,12,C.dim)+'<path d="M28 166H956" stroke="'+C.line+'" stroke-width=".7"/>'+meta(28,184,'12 SECOND LOOP / ORIGINAL CONFIGURATION / NO LIVE DATA')}
 function footer(s,label){return '<path d="M28 1212H956" stroke="'+C.line+'" stroke-width=".7"/>'+txt(28,1238,s,12,C.fg)+txt(28,1259,'原创中文视觉样板 / 所有事件、数字与状态均为预设演示',9,C.dim)+meta(956,1259,label,C.amber,' text-anchor="end"')}
 return {txt:txt,meta:meta,rect:rect,panel:panel,page:page,footer:footer};
}

B.labEditorial=function(e){
 var root=vroot(e),svg=root.svg,C=ecPalette(e),A=ecAuthor(root,C),id=root.id;
 var s='<defs><pattern id="'+id+'dots" width="23" height="23" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".45" fill="'+C.dim+'" opacity=".12"/></pattern></defs>';
 s+=A.page('六种组件，把过程变成可见的故事','角色 · 汇聚 · 比例 · 分支 · 虚实 · 任务状态','同一份配置，可以组织成网页，也可以导出成一段动画。','LIVE PANEL / THE VECTOR FIELD GUIDE / 06 COMPONENTS');
 s+=A.rect(28,201,928,247,C.surface,C.line,4,' data-neon-border="lab-hero" data-neon-color="'+C.amber+'" data-neon-role="hero"')+'<rect x="29" y="202" width="926" height="245" fill="url(#'+id+'dots)"/>';
 s+=A.meta(42,224,'01 / THE GLOWING GUIDE',C.cyan)+A.txt(334,261,'先让读者知道，应该看哪里。',21,C.fg,'serif',true);
 s+=A.txt(334,289,'角色的浮动、渐变与光环，把注意力聚在起点。',13,C.dim);
 s+=A.txt(334,313,'图形可以组合；每一次变化，都来自同一条时间线。',13,C.dim);
 s+=A.txt(334,366,'06',38,C.amber,'mono',true)+A.txt(411,365,'种可复用组件',15,C.fg)+A.meta(334,390,'SVG / FIXED GEOMETRY / DETERMINISTIC MOTION');
 s+='<path d="M311 235V410" stroke="'+C.line+'" stroke-width=".6"/>';
 ['01 角色','02 汇聚','03 比例','04 对比','05 流带','06 看板'].forEach(function(t,i){s+=A.txt(43+i*149,430,t,11,[C.cyan,C.amber,C.pink,C.mint,C.cyan,C.amber][i],'mono')});
 s+=A.panel(28,466,928,236,'02 / CONVERGE','从分散候选，到一个协调中心','25 NODES → 01 HUB',C.amber);
 s+=A.panel(28,707,454,240,'03 / PROPORTION','把结构与占比放在一起','06 SECTORS',C.pink);
 s+=A.panel(502,707,454,240,'04 / REVEAL','让候选与确认，各有形态','25 CANDIDATES / 04 PICKS',C.mint);
 s+=A.panel(28,965,454,228,'05 / DISTRIBUTE','同一请求，沿着不同路径展开','05 PATHS',C.cyan);
 s+=A.panel(502,965,454,228,'06 / PROGRESS','任务停留，然后继续前进','04 LANES',C.amber);
 s+=A.footer('组件不是结论；标签、比例和计数，都需要由作者说明来源。','FIELD GUIDE / 06');
 svg.innerHTML=s;
 var styled=false;
 COMPONENTS.push(function(t){
  if(!styled){
   ST.querySelectorAll('svg[data-component="orb"],svg[data-component="seats"],svg[data-component="donut"],svg[data-component="ghostSeats"],svg[data-component="ribbons"],svg[data-component="kanban"]').forEach(function(scene){
    var kind=scene.getAttribute('data-component'),texts=Array.from(scene.querySelectorAll('text'));
    texts.forEach(function(n){n.setAttribute('font-family',/[\u3400-\u9fff]/.test(n.textContent)?'LP Sans':'LP Mono, LP Sans');n.setAttribute('font-size',Math.max(Number(n.getAttribute('font-size')),10))});
    function move(n,y,size){n.setAttribute('y',y);if(size)n.setAttribute('font-size',size)}
    if(kind==='orb'){move(texts[0],151,12);move(texts[1],174,10);move(texts[2],191,9)}
    if(kind==='seats')texts.forEach(function(n){var y=Number(n.getAttribute('y'));if(n.parentNode!==scene&&y===-2)move(n,-6,9);else if(n.parentNode!==scene&&y===9)move(n,12,9);else if(y===45)move(n,36,9);else if(y===138)move(n,150,10)});
    if(kind==='ghostSeats')texts.forEach(function(n){var y=Number(n.getAttribute('y'));if(y===60)move(n,56,n.getAttribute('x')==='195'?22:10);else if(y===88)move(n,92,22);else if(y===84)move(n,82,10);else if(y===96)move(n,102,10);else if(y===130)move(n,138,17);else if(y===128)move(n,128,10);else if(y===140)move(n,148,10);else if(y===160)move(n,181,17);else if(y===158)move(n,172,10);else if(y===170)move(n,192,10)});
    if(kind==='kanban')texts.forEach(function(n){var y=Number(n.getAttribute('y'));if(y===220)move(n,224,8);else if(y===204&&n.getAttribute('x')==='5')move(n,201,23)});
   });styled=true;
  }
 });
};

B.avatarEditorial=function(e){
 var root=vroot(e),svg=root.svg,C=ecPalette(e),A=ecAuthor(root,C),id=root.id;
 var guide=cfg.machines&&cfg.machines.guide||{},guidePeriod=Number(guide.period)||4,guideCount=guide.order?guide.order.length:guide.values?guide.values.length:3,timelineDuration=guidePeriod*guideCount,guideStart=Number(guide.t0)||0;
 (cfg.elements||[]).forEach(function(actor){if(actor.type==='drone'){actor.period=timelineDuration;actor.focusPeriod=guidePeriod}});
 var s='<defs><filter id="'+id+'halo" x="-160%" y="-160%" width="420%" height="420%"><feGaussianBlur stdDeviation="'+(C.light?1.7:3)+'" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>';
 s+=A.page('一个游走的角色，带着读者走完过程','导航 · 聚焦 · 关键词 · 角色样式 · 深浅阅读环境','角色可以换，路径可以改；读者始终知道，当前正在讲哪一步。','LIVE PANEL / THE TRAVELING GUIDE / AVATAR & THEME');
 s+=A.rect(28,201,928,351,C.surface,C.line,4,' data-neon-border="avatar-hero" data-neon-color="'+C.amber+'" data-neon-role="hero"')+A.meta(42,224,'THE GUIDED JOURNEY',C.amber)+A.txt(42,258,'让视线跟随过程，而不只是在画布上移动。',20,C.fg,'serif',true);
 var centers=[178,492,807],colors=[C.cyan,C.amber,C.mint],titles=['检索依据','核对上下文','解释结果'];
 centers.forEach(function(x,i){
  s+='<circle cx="'+x+'" cy="352" r="77" fill="none" stroke="'+colors[i]+'" stroke-width=".65" opacity=".2"/><circle data-hotspot="'+i+'" cx="'+x+'" cy="352" r="66" fill="none" stroke="'+colors[i]+'" stroke-width="1" stroke-dasharray="2 8" opacity=".3"/>';
  s+=A.meta(x,290,['01 / RETRIEVE','02 / VERIFY','03 / EXPLAIN'][i],colors[i],' text-anchor="middle"');
  s+=A.txt(x,474,titles[i],17,colors[i],'serif',true,' text-anchor="middle"');
  s+=A.txt(x,499,['先找到相关片段','再判断是否够用','把结论带回出处'][i],12,C.dim,null,false,' text-anchor="middle"');
 });
 s+='<path d="M257 352C310 320 365 320 413 352M571 352C619 320 677 320 728 352" fill="none" stroke="'+C.line+'" stroke-width=".8" stroke-dasharray="3 6"/>';
 s+='<path d="M43 518H940" stroke="'+C.line+'" stroke-width=".6"/>'+A.txt(43,539,'当前 · 检索依据',11,C.cyan,null,true,' data-current-label="1"')+A.meta(940,539,'SPIDER / DRONE · SAME TIMELINE',C.dim,' text-anchor="end"');
 s+=A.panel(28,571,454,287,'01 / APPEARANCE','颜色是角色的一部分','STYLE TOKENS',C.pink);
 s+=A.txt(47,660,'纤细分节腿',13,C.fg)+A.txt(47,685,'用细线连接运动关节',12,C.dim);
 s+='<path d="M70 737L125 700L174 742" fill="none" stroke="'+C.red+'" stroke-width="2"/>';
 [70,125,174].forEach(function(x,i){s+='<circle cx="'+x+'" cy="'+[737,700,742][i]+'" r="5" fill="'+C.mint+'" filter="url(#'+id+'halo)"/>'});
 s+=A.txt(234,660,'甲壳与能量核心',13,C.fg)+A.txt(234,685,'轮廓、关节、核心各自配色',12,C.dim);
 s+=A.rect(256,707,62,51,C.surface,C.pink,12)+'<circle cx="287" cy="733" r="9" fill="'+C.amber+'" filter="url(#'+id+'halo)"/>';
 s+=A.txt(47,801,'八足蜘蛛与机器人，可以共享同一条路线。',12,C.fg)+A.meta(47,829,'PALETTE / SIZE / GAIT / AVATAR',C.dim);
 s+=A.panel(502,571,454,287,'02 / ATTENTION','每一步，都有一个明确的焦点','03 FOCUS REGIONS',C.cyan);
 titles.forEach(function(label,i){var y=665+i*45;s+=A.rect(519,y-19,420,31,C.surface,C.line,3,' data-state-row="'+i+'"')+A.txt(535,y+1,'0'+(i+1),11,colors[i],'mono',true)+A.txt(578,y+1,label,13,C.fg)+A.txt(921,y+1,['候选片段','原文语境','结论与引用'][i],11,C.dim,null,false,' text-anchor="end"')});
 s+=A.txt(519,817,'热区轻微呼吸，目标框与虚线说明指向。',12,C.dim);
 s+=A.panel(28,877,928,316,'03 / TIMELINE','换一种阅读环境，也保留同一段过程',timelineDuration+' SECONDS / '+guideCount+' STAGES',C.amber);
 s+=A.txt(47,963,'暖黑强调光点与细线；淡纸让文字与关系更容易阅读。',13,C.dim);
 s+=A.txt(47,988,'主题由配置控制。角色的游走、抬脚与聚焦，都可以精确回放。',13,C.dim);
 s+='<path d="M126 1046H860" stroke="'+C.line+'" stroke-width="1"/>';
 [126,370,615,860].forEach(function(x,i){s+='<path d="M'+x+' 1038v16" stroke="'+C.dim+'" stroke-width=".7"/>'+A.meta(x,1075,String(timelineDuration*i/3).padStart(2,'0')+' s',C.dim,' text-anchor="middle"')});
 s+='<circle data-clock-dot="1" cx="126" cy="1046" r="5" fill="'+C.amber+'" filter="url(#'+id+'halo)"/>';
 s+=A.txt(47,1133,'00.0 s',28,C.amber,'mono',true,' data-time-label="1"')+A.txt(189,1131,'暂停、跳转、重播，仍然回到相同一帧。',13,C.fg);
 s+=A.meta(47,1167,'CONFIGURABLE PRESENTATION · AUTHORED EVENTS · NO RUNTIME CONNECTION',C.dim);
 s+=A.footer('角色承载的是讲解与状态提示；动作本身，不代表真实系统正在执行。','AVATAR / THEME');
 svg.innerHTML=s;
 var rings=svg.querySelectorAll('[data-hotspot]'),rows=svg.querySelectorAll('[data-state-row]'),label=svg.querySelector('[data-current-label]'),dot=svg.querySelector('[data-clock-dot]'),time=svg.querySelector('[data-time-label]'),styled=false;
 COMPONENTS.push(function(t){if(!styled){ST.querySelectorAll('svg[data-component="drone"]').forEach(function(actor){var wire=actor.querySelector(':scope > path'),focus=actor.querySelector(':scope > rect');if(wire)wire.setAttribute('stroke',C.dim);if(focus)focus.setAttribute('stroke',C.pink);actor.querySelectorAll('text').forEach(function(n){n.setAttribute('font-family','LP Sans')})});styled=true}var local=mod(t-guideStart,timelineDuration),k=mod(parseInt(V['guide.i'],10)||0,colors.length);label.textContent='当前 · '+(tv('guide')||titles[k]);label.setAttribute('fill',colors[k]);time.textContent=local.toFixed(1).padStart(4,'0')+' s';dot.setAttribute('cx',126+734*local/timelineDuration);rings.forEach(function(n,i){n.setAttribute('r',66+(i===k?Math.sin(t*1.7)*2:0));n.setAttribute('opacity',i===k?.75:.18)});rows.forEach(function(n,i){n.setAttribute('stroke',i===k?colors[i]:C.line);n.setAttribute('stroke-opacity',i===k?.9:.6)});});
};
