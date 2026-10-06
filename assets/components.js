/* Optional vector components. Every animation derives solely from seek(t).
 * No timers, random state or network assets. Kept inside the template closure. */
var VCID=0, NS='http://www.w3.org/2000/svg';
function vx(tag,attrs,parent){var n=document.createElementNS(NS,tag);Object.keys(attrs||{}).forEach(function(k){n.setAttribute(k,attrs[k])});if(parent)parent.appendChild(n);return n}
function vtext(parent,x,y,text,color,size,anchor){var n=vx('text',{x:x,y:y,fill:color||'#d9d8d2','font-size':size||10,'font-family':'Consolas, "DejaVu Sans Mono", monospace','text-anchor':anchor||'start','data-component-text':'1'},parent);n.textContent=text;return n}
function vroot(e){var id='vc'+(++VCID),n=vx('svg',{width:e.w,height:e.h,viewBox:'0 0 '+e.w+' '+e.h,'data-component':e.type});n.style.cssText='position:absolute;left:'+(e.x||0)+'px;top:'+(e.y||0)+'px;overflow:'+(e.overflow||'hidden')+';pointer-events:none;transform-origin:0 0;transform:scale('+(e.scale||1)+')';ST.appendChild(n);return {svg:n,id:id}}
function glow(root,id){var defs=vx('defs',{},root);defs.innerHTML='<filter id="'+id+'" x="-150%" y="-150%" width="400%" height="400%"><feGaussianBlur stdDeviation="3" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>';return 'url(#'+id+')'}
function phase(t,period,offset){return mod(t+(offset||0),period)/period}
function smooth(v){return v*v*(3-2*v)}
function vlabel(e,key,fallback){return e.labels&&e.labels[key]!=null?e.labels[key]:fallback}
function vmetric(spec,n){var value=spec.value!=null?spec.value:n*(spec.perSeat==null?1:spec.perSeat);return (spec.prefix||'')+Number(value).toLocaleString('en-US',{minimumFractionDigits:spec.decimals||0,maximumFractionDigits:spec.decimals||0})+(spec.suffix||'')}
function seatCount(t,e){return 1+Math.floor(phase(t,e.period||12.5,e.phase||0)*25)}
function person(g,x,y,color,scale,dash){var p=vx('g',{transform:'translate('+x+' '+y+') scale('+(scale||1)+')',fill:'none',stroke:color,'stroke-width':1,'stroke-dasharray':dash?'2 3':''},g);vx('circle',{cx:0,cy:-5,r:3},p);vx('path',{d:'M-5 5V0Q0 -5 5 0V5Z'},p);return p}

B.vector=function(e){var r=vroot(e);r.svg.innerHTML=e.markup||'';r.svg.querySelectorAll('text').forEach(function(n){n.setAttribute('data-vector-text','1')})};

B.orb=function(e){
 var r=vroot(e),n=r.svg,c=e.color||'#e84a9c',cx=e.w/2,cy=e.cy||e.h*.42,rad=e.r||37,uid=r.id;
 var d=vx('defs',{},n);d.innerHTML='<radialGradient id="'+uid+'grad" cx="32%" cy="25%"><stop offset="0" stop-color="'+(e.light||'#ffd7ef')+'"/><stop offset=".46" stop-color="'+c+'"/><stop offset="1" stop-color="'+(e.dark||'#461630')+'"/></radialGradient><filter id="'+uid+'blur"><feGaussianBlur stdDeviation="7"/></filter>';
 vx('circle',{cx:cx,cy:cy,r:rad+12,fill:c,opacity:.17,filter:'url(#'+uid+'blur)'},n);
 var rings=vx('g',{fill:'none',stroke:c,'stroke-width':1},n);
 vx('circle',{cx:cx,cy:cy,r:rad+9,opacity:.25},rings);vx('circle',{cx:cx,cy:cy,r:rad+17,opacity:.12},rings);
 var body=vx('g',{},n);
 if(e.kind==='pixel'){
  vx('path',{d:'M'+(cx-25)+' '+(cy-28)+'h49v16h9v17h-9v28h-12v-13h-12v13h-13v-14h-12v14h-11v-29h-10v-16h10Z',fill:'url(#'+uid+'grad)',stroke:'#f5d99b','stroke-width':2},body);
  vx('rect',{x:cx-13,y:cy-12,width:10,height:10,fill:'#211a13'},body);vx('rect',{x:cx+9,y:cy-12,width:10,height:10,fill:'#211a13'},body);
 }else{
  vx('circle',{cx:cx,cy:cy,r:rad,fill:'url(#'+uid+'grad)',stroke:c,'stroke-width':1.5},body);
  var eyes=vx('g',{transform:'rotate(12 '+cx+' '+cy+')',stroke:e.eyeColor||'#fcf1fc','stroke-width':8,'stroke-linecap':'round'},body);
  vx('line',{x1:cx-10,y1:cy-7,x2:cx-10,y2:cy+6},eyes);vx('line',{x1:cx+10,y1:cy-7,x2:cx+10,y2:cy+6},eyes);
 }
 vtext(n,cx,cy+rad+21,e.label,c,12,'middle').setAttribute('font-weight','bold');
 vtext(n,cx,cy+rad+33,e.subtitle,'#d5d4ce',8,'middle');vtext(n,cx,cy+rad+43,e.detail,'#73716c',7,'middle');
 COMPONENTS.push(function(t){body.setAttribute('transform','translate(0 '+(Math.sin(t*1.6+(e.phase||0))*2.2)+')');rings.setAttribute('opacity',.65+.3*Math.sin(t*1.3));});
};

B.seats=function(e){
 var r=vroot(e),s=r.svg,id=r.id,filter=glow(s,id+'glow'), seats=[],packs=[],originX=22,y=64,step=28,goal=[e.w-111,53];
 vtext(s,20,13,vlabel(e,'title','25 SEATS · ONE ORG CHART'),'#d4a7c0',9).setAttribute('letter-spacing',1);
 var tree=vx('g',{fill:'none',stroke:'#636668','stroke-width':.7,opacity:.5},s),heads=[];
 vx('path',{d:'M300 20V35H80V49M300 35H640V49M221 35V49M362 35V49M502 35V49'},tree);
 vx('rect',{x:284,y:4,width:33,height:15,rx:3,fill:'#aaa9a5',opacity:.8},s);person(s,300,13,'#161718',.65);vtext(s,321,15,vlabel(e,'leader','CTO'),'#8d8c84',7);
 [80,221,362,502].forEach(function(x){var g=vx('g',{},s);vx('rect',{x:x-12,y:37,width:24,height:15,rx:3,fill:'#53b9c5',opacity:.7},g);person(g,x,y-19,'#142125',.7);heads.push(g)});
 for(var i=0;i<25;i++){
  var x=originX+i*step;
  var a=vx('rect',{x:x,y:y,width:22,height:12,rx:2,fill:'none',stroke:'#625e55','stroke-width':.6,'stroke-dasharray':'2 2'},s);a._person=person(s,x+11,y+7,'#382816',.7);seats.push(a);
  var p=vx('circle',{r:2.5,fill:i<20?'#eab961':'#ec55a6',filter:filter,opacity:0},s);packs.push(p);
 }
 [92,245,398,552].forEach(function(x,i){vtext(s,x,91,vlabel(e,'teams',['PLATFORM','ML','PRODUCT','DATA + QA'])[i],'#5e5c54',7)});
 var wheel=vx('g',{transform:'translate('+goal[0]+' '+goal[1]+')'},s),bars=[];
 for(var j=0;j<32;j++){var a=j*Math.PI/16;bars.push(vx('line',{x1:Math.cos(a)*35,y1:Math.sin(a)*35,x2:Math.cos(a)*43,y2:Math.sin(a)*43,stroke:'#ec55a6','stroke-width':2,opacity:.35},wheel))}
 vx('polygon',{points:'0,-26 24,-13 24,13 0,26 -24,13 -24,-13',fill:'#351c2b',stroke:'#e954a7','stroke-width':1.3,filter:filter},wheel);
 vtext(wheel,0,-2,vlabel(e,'hub',['ONE','AGENT'])[0],'#f48ac1',8,'middle');vtext(wheel,0,9,vlabel(e,'hub',['ONE','AGENT'])[1],'#f48ac1',8,'middle');vtext(s,goal[0]+53,45,vlabel(e,'count','seats'),'#6e625f',7);
 var count=vtext(s,goal[0]+53,58,'1','#f060b2',13);
 vx('line',{x1:6,y1:105,x2:e.w-6,y2:105,stroke:'#393832','stroke-width':.7},s);
 var vals=[];[[95,'#e7bd66','seats it stands in for'],[302,'#57c5d8','a month of that payroll'],[505,'#f164b2','a month of the agent'],[713,'#70d6b0','a month · 402 × $299']].forEach(function(q,i){vals.push(vtext(s,q[0],124,'',q[1],13,'middle'));vtext(s,q[0],138,vlabel(e,'captions',['seats it stands in for','a month of that payroll','a month of the agent','a month · 402 × $299'])[i],'#96928a',7,'middle')});
 COMPONENTS.push(function(t){var n=seatCount(t,e);count.textContent=n;heads.forEach(function(g,i){g.setAttribute('opacity',n>(i+1)*5?.08:1)});seats.forEach(function(a,i){var active=i>=n;a.setAttribute('fill',active?(i===n?'#e45a9d':'#e7bb67'):'none');a.setAttribute('opacity',active?1:.38);a._person.setAttribute('opacity',active?1:0);a.setAttribute('stroke-dasharray',active?'':'2 2');var u=phase(t,2.8,i*.19),x=originX+i*step+11,p=packs[i];p.setAttribute('cx',x+(goal[0]-x)*u);p.setAttribute('cy',y-6+(goal[1]-y+6)*u-Math.sin(u*Math.PI)*18);p.setAttribute('opacity',active?.8:0)});bars.forEach(function(b,i){b.setAttribute('opacity',.24+.76*Math.pow((Math.sin(t*2-i*.4)+1)/2,3))});if(e.data&&e.data.metrics){vals.forEach(function(v,i){v.textContent=vmetric(e.data.metrics[i]||{},n)})}else{vals[0].textContent=n+' of 25';vals[1].textContent='$'+(n*13750).toLocaleString('en-US');vals[2].textContent='$'+Math.round(n*82.2).toLocaleString('en-US');vals[3].textContent='$120,198';}});
};

B.donut=function(e){
 var r=vroot(e),s=r.svg,id=r.id,filter=glow(s,id+'glow'),cx=107,cy=115,rad=65,sw=31;
 vx('circle',{cx:cx,cy:cy,r:rad+23,fill:'none',stroke:'#80796d','stroke-width':1,'stroke-dasharray':'3 8',opacity:.6},s);
 var ring=vx('g',{transform:'rotate(-90 '+cx+' '+cy+')'},s),arcs=[];
 ['#e44e99','#737577','#447cb0','#d67d61','#debb66','#69bba0'].forEach(function(c,i){arcs.push(vx('circle',{cx:cx,cy:cy,r:rad,fill:'none',stroke:c,'stroke-width':sw,filter:i===0?filter:''},ring))});
 vtext(s,cx,cy-1,vlabel(e,'total','1,000 h'),'#f1efdf',16,'middle').setAttribute('font-weight','bold');vtext(s,cx,cy+14,vlabel(e,'period','one week'),'#979286',8,'middle');
 var dot=vx('circle',{r:4,fill:'#f268b5',filter:filter},s),val=[];
 [['writing code','#ed61ad','410 h'],['meetings','#91908a','190 h'],['review','#598bc1','150 h'],['on-call','#d67d61','90 h'],['customers','#debb66','80 h'],['deciding','#69bba0','80 h']].forEach(function(q,i){vx('rect',{x:235,y:48+i*18,width:4,height:10,rx:1,fill:q[1]},s);vtext(s,245,57+i*18,vlabel(e,'items',['writing code','meetings','review','on-call','customers','deciding'])[i],q[1],10);val.push(vtext(s,e.w-12,57+i*18,vlabel(e,'values',['410 h','190 h','150 h','90 h','80 h','80 h'])[i],q[1],10,'end'))});
 var notes=vlabel(e,'notes',['the agent takes the 410','the other 590 were never code','41% is the work the agent takes']);
 vx('line',{x1:237,y1:158,x2:e.w-10,y2:158,stroke:'#34332d'},s);vtext(s,237,178,notes[0],'#ed61ad',10);vtext(s,237,195,notes[1],'#cac6ba',9);vtext(s,237,210,notes[2],'#858278',8);
 var sparks=[];for(var i=0;i<13;i++)sparks.push(vx('circle',{r:1.5,fill:'#ed61ad',filter:filter},s));
 COMPONENTS.push(function(t){var data=e.data||{},base=data.parts||[.41,.19,.15,.09,.08,.08],pulse=Math.max(0,Math.sin(t*.7))*(data.pulseAmount==null?.035:data.pulseAmount),parts=base.slice(),start=0,circ=2*Math.PI*rad;parts[0]+=pulse;parts[5]-=parts[0]-base[0];arcs.forEach(function(a,i){a.setAttribute('stroke-dasharray',(parts[i]*circ-2)+' '+circ);a.setAttribute('stroke-dashoffset',-start*circ);start+=parts[i]});var a=t*.8;dot.setAttribute('cx',cx+Math.cos(a)*(rad+19));dot.setAttribute('cy',cy+Math.sin(a)*(rad+19));sparks.forEach(function(p,i){var a=t*.2+i*.49,r=rad+20+Math.sin(t+i)*4;p.setAttribute('cx',cx+Math.cos(a)*r);p.setAttribute('cy',cy+Math.sin(a)*r);p.setAttribute('opacity',.3+.4*Math.sin(t+i)*Math.sin(t+i))});});
};

B.kanban=function(e){
 var r=vroot(e),s=r.svg,id=r.id,filter=glow(s,id+'glow'),cols=vlabel(e,'columns',['TODO','DOING','REVIEW','DONE']),colors=['#9d9b90','#e6ba67','#609dd0','#73c89d'],cw=(e.w-12)/4,top=37,h=132;
 cols.forEach(function(c,i){vx('rect',{x:3+i*cw,y:top,width:cw-5,height:h,rx:7,fill:colors[i],'fill-opacity':.028,stroke:colors[i],'stroke-opacity':.38,'stroke-width':.7},s);vtext(s,3+i*cw+(cw-5)/2,top+15,c,colors[i],10,'middle').setAttribute('letter-spacing',1.3);if(i<3)vx('path',{d:'M'+(cw*(i+1)-2)+' 94l7 7-7 7',fill:'none',stroke:'#aaa89b'},s)});
 var cards=[]; (e.tickets||['#807 invoices','#808 webhook','#809 quota','#810 emails','#823 cache','#806 login']).forEach(function(label,i){var g=vx('g',{},s);vx('rect',{width:95,height:14,rx:4,fill:'#27241c',stroke:'#caae70','stroke-width':.7},g);vtext(g,5,10,label,'#e9e4d2',8);cards.push(g)});
 var dots=[];for(var j=0;j<6;j++)dots.push(vx('circle',{cx:e.w-54,cy:65+j*16,r:8,fill:'none',stroke:'#71bf93','stroke-opacity':.3},s));
 vx('rect',{x:4,y:178,width:e.w-8,height:4,rx:2,fill:'#282e24'},s);var bar=vx('rect',{x:4,y:178,width:150,height:4,rx:2,fill:'#62cca4',filter:filter},s);
 var data=e.data||{},countStart=data.countStart==null?61:data.countStart,countMax=data.countMax==null?312:data.countMax,countRate=data.countRate==null?360:data.countRate,countPeriod=data.countPeriod||35;
 var closed=vtext(s,5,204,String(countStart),'#71dab0',23);closed.setAttribute('font-weight','bold');vtext(s,54,204,vlabel(e,'countCaption','tickets closed by the agent this week'),'#ccc8bd',9);vtext(s,5,220,vlabel(e,'footer','the 25 closed 96 in the same week · most of their week was not tickets'),'#8a867b',7.5);
 COMPONENTS.push(function(t){cards.forEach(function(g,i){var u=phase(t,e.period||9,i*1.37),lane=Math.min(3,Math.floor(u*4)),local=u*4-lane;var x=lane*cw+7+(lane<3?smooth(Math.max(0,(local-.65)/.35))*cw:0);g.setAttribute('transform','translate('+x+' '+(top+28+(i%5)*18)+')');g.setAttribute('opacity',u>.94?Math.max(0,(1-u)/.06):.85);var rect=g.firstChild;rect.setAttribute('stroke',colors[lane]);rect.setAttribute('fill',lane===3?'#304c35':'#24221b')});dots.forEach(function(a,i){a.setAttribute('r',5+phase(t,2.8,i*.4)*6);a.setAttribute('opacity',1-phase(t,2.8,i*.4))});var n=Math.min(countMax,countStart+Math.floor(phase(t,countPeriod)*countRate));closed.textContent=n;bar.setAttribute('width',(e.w-8)*n/countMax);});
};

B.ribbons=function(e){
 var r=vroot(e),s=r.svg,id=r.id,defs=vx('defs',{},s),filter=glow(s,id+'glow'),flows=[];
 [['fee','#818d96',80],['hosting','#5797d2',100],['agent','#e1579b',119],['ops','#bc9f54',151],['net','#6fba92',203]].forEach(function(q,i){var y=q[2],th=i<3?5:(i===3?26:35);var endX=251;
  defs.innerHTML+='<linearGradient id="'+id+q[0]+'"><stop stop-color="#64b18f" stop-opacity=".35"/><stop offset="1" stop-color="'+q[1]+'" stop-opacity=".22"/></linearGradient>';
  var d='M28 101 C100 100 161 '+y+' '+endX+' '+y;
  vx('path',{d:d,fill:'none',stroke:'url(#'+id+q[0]+')','stroke-width':th},s);var p=vx('path',{d:d,fill:'none',stroke:q[1],'stroke-width':i<3?1:0,'stroke-opacity':.8},s);flows.push({path:p,y:y,th:th,color:q[1],dots:[]});
  for(var j=0;j<8;j++)flows[i].dots.push(vx('circle',{r:i<3?2:3,fill:'#f0efdf',filter:i<3?'':filter,opacity:.85},s));
  vx('line',{x1:endX,y1:y-th*.65,x2:endX,y2:y+th*.65,stroke:q[1],'stroke-width':i<3?3:4,filter:filter},s);
 });
 vx('rect',{x:8,y:85,width:18,height:130,rx:7,fill:'#48886c','fill-opacity':.8,stroke:'#7acfaa',filter:filter},s);vx('line',{x1:17,y1:95,x2:17,y2:203,stroke:'#a0e3b6','stroke-width':3,'stroke-linecap':'round'},s);
 var branches=vlabel(e,'branches',['payment fees · 3%','hosting + data','the agent','the 3 humans','left on the table']),values=vlabel(e,'values',['$3,606','$6,400','$2,055','$41,250','$66,887']);
 vtext(s,9,71,vlabel(e,'source','402 × $299'),'#dbd9cd',12);
 [83,103,124,156,207].forEach(function(y,i){vtext(s,266,y,branches[i],['#a6aaac','#609cce','#e1579b','#dbb865','#78cda5'][i],11);vtext(s,e.w-7,y,values[i],'#eeeade',12,'end')});
 vx('rect',{x:7,y:247,width:e.w-14,height:23,rx:4,fill:'#70bf97','fill-opacity':.06,stroke:'#7baf8c','stroke-opacity':.4},s);vtext(s,e.w/2,262,vlabel(e,'footer','$66,887 before tax, before churn, before you pay yourself'),'#d4d7c8',9,'middle');
 COMPONENTS.push(function(t){flows.forEach(function(f,i){f.dots.forEach(function(d,j){var u=phase(t,3.5+i*.4,j*(3.5+i*.4)/8),a=1-u,y=a*a*a*101+3*a*a*u*100+3*a*u*u*f.y+u*u*u*f.y,x=a*a*a*28+3*a*a*u*100+3*a*u*u*161+u*u*u*251;d.setAttribute('cx',x);d.setAttribute('cy',y+(i>2?Math.sin(j*2.13)*f.th*.22:0));d.setAttribute('opacity',Math.sin(u*Math.PI)*.9)});});});
};

B.ghostSeats=function(e){
 var r=vroot(e),s=r.svg,id=r.id,filter=glow(s,id+'glow'),nodes=[];
 for(var i=0;i<25;i++){nodes.push(person(s,25+(i%5)*29,43+Math.floor(i/5)*31,'#686657',1.3,true));}
 var rings=[];for(var j=0;j<3;j++)rings.push(vx('circle',{cx:85+(j===1?-25:j===2?25:0),cy:102+(j===0?-14:15),r:18,fill:'none',stroke:['#a09c66','#5da98a','#bcae78'][j],opacity:.5},s));
 var realPeople=vx('g',{},s),yellowPeople=vx('g',{},s);[[52,85],[85,85],[52,116]].forEach(function(q){vx('circle',{cx:q[0],cy:q[1],r:11,fill:'#62c795',opacity:.2,filter:filter},realPeople);person(realPeople,q[0],q[1],'#8beac0',1.4)});person(yellowPeople,85,116,'#efc875',1.4);
 vtext(s,195,60,vlabel(e,'topValue','25'),'#bab8ae',24);vtext(s,242,60,vlabel(e,'topCaption','the number in the headline'),'#c9c4b6',9);
 var middleLines=vlabel(e,'middleLines',['if every dollar went','to salaries and nothing else']);vtext(s,195,88,vlabel(e,'middleValue','8.7'),'#bab8ae',24);vtext(s,242,84,middleLines[0],'#c9c4b6',9);vtext(s,242,96,middleLines[1],'#c9c4b6',9);
 vx('line',{x1:194,y1:103,x2:e.w-10,y2:103,stroke:'#49463d','stroke-width':2},s);vx('line',{x1:13,y1:198,x2:178,y2:198,stroke:'#a55457','stroke-width':3,opacity:.7},s);
 var bottomValues=vlabel(e,'bottomValues',['4','3']),bottomLines=vlabel(e,'bottomLines',['what a business that size','actually carries','humans it still needs','next to the agent']);
 var realLabels=vx('g',{},s);vtext(realLabels,217,130,bottomValues[0],'#e8be6c',17);vtext(realLabels,240,128,bottomLines[0],'#c9c4b6',8);vtext(realLabels,240,140,bottomLines[1],'#c9c4b6',8);vtext(realLabels,217,160,bottomValues[1],'#78d3a4',17);vtext(realLabels,240,158,bottomLines[2],'#c9c4b6',8);vtext(realLabels,240,170,bottomLines[3],'#c9c4b6',8);
 var data=e.data||{},revealPeriod=data.revealPeriod||35,revealStart=data.revealStart==null?8:data.revealStart,revealDuration=data.revealDuration||4;
 COMPONENTS.push(function(t){var reveal=smooth(Math.max(0,Math.min(1,(phase(t,revealPeriod)*revealPeriod-revealStart)/revealDuration)));realPeople.setAttribute('opacity',reveal);yellowPeople.setAttribute('opacity',reveal);realLabels.setAttribute('opacity',reveal);nodes.forEach(function(n,i){n.setAttribute('opacity',.27+.2*(1+Math.sin(t*.8-i*.4))/2)});rings.forEach(function(n,i){n.setAttribute('r',18+Math.sin(t*1.1+i)*2);n.setAttribute('opacity',.3+.25*(1+Math.sin(t+i))/2)});});
};

var AVATARS=[];
window.setAvatar=function(kind){
 if(kind!=='spider'&&kind!=='drone')throw new Error('avatar must be spider or drone');
 AVATARS.forEach(function(select){select(kind)});
 if(window.__ready)window.seek(window.__t||0);
 return kind;
};
function blendHeading(a,b,u){var delta=((b-a+540)%360)-180;return a+delta*u}
B.drone=function(e){
 var timeline=e.timelineMachine&&(cfg.machines||{})[e.timelineMachine],sequence=null,offset=0;
 if(timeline&&timeline.type==='cycle'){sequence=timeline.order||timeline.values.map(function(_,i){return i});e.focusPeriod=timeline.period;e.period=timeline.period*sequence.length;offset=timeline.t0||0}
 var r=vroot(e),s=r.svg,id=r.id,filter=glow(s,id+'glow'),wire=vx('path',{fill:'none',stroke:'#dbd4c6','stroke-width':.8,'stroke-dasharray':'2 3',opacity:.6},s),focus=vx('rect',{fill:'none',stroke:'#ed5cac','stroke-width':1.5,rx:4,opacity:0},s),wordGroup=vx('g',{},s),g=vx('g',{},s),fans=[];
 var robot=vx('g',{'data-avatar':'drone'},g);
 for(var i=0;i<7;i++){var f=vx('g',{},robot);vx('line',{x1:0,y1:0,x2:-62,y2:(i-3)*10,stroke:'#ef553e','stroke-width':1.2,opacity:.8},f);vx('circle',{cx:-62,cy:(i-3)*10,r:4.3,fill:'#62dd9b',stroke:'#155c38','stroke-width':1,filter:filter},f);vx('circle',{cx:-43,cy:(i-3)*8,r:3.6,fill:'#6bea9b',stroke:'#1b663a','stroke-width':1,filter:filter},f);fans.push(f)}
 vx('rect',{x:-23,y:-18,width:46,height:36,rx:9,fill:'#202d61',stroke:'#80a9ff','stroke-width':3,filter:filter},robot);vx('rect',{x:-16,y:-11,width:32,height:22,rx:4,fill:'#131d3c',stroke:'#527bbb'},robot);vx('circle',{cx:-6,cy:0,r:4,fill:'#f754b2',filter:filter},robot);vx('circle',{cx:8,cy:0,r:2,fill:'#aec5ff'},robot);

 // Four pairs of articulated legs, drawn behind the two-part mechanical body.
 var spider=vx('g',{'data-avatar':'spider'},g),legs=[],palette=Object.assign({leg:'#ff594b',joint:'#74f3a9',shell:'#769fff',core:'#ff65c8'},e.avatarColors||{}),defs=vx('defs',{},s);
 defs.innerHTML='<radialGradient id="'+id+'shell" cx="32%" cy="25%"><stop stop-color="#34477a"/><stop offset="1" stop-color="#10152d"/></radialGradient>';
 [-1,1].forEach(function(side){for(var row=0;row<4;row++){
  var leg=vx('g',{'data-spider-leg':side+':'+row},spider);
  var shadow=vx('path',{fill:'none',stroke:palette.leg,'stroke-width':4,opacity:.12,filter:filter},leg);
  var upper=vx('path',{fill:'none',stroke:palette.leg,'stroke-width':1.9,'stroke-linecap':'round','stroke-linejoin':'round'},leg);
  var lower=vx('path',{fill:'none',stroke:palette.leg,'stroke-width':1.4,'stroke-linecap':'round'},leg);
  var hip=vx('circle',{cx:side*16,cy:-14+row*9,r:2.2,fill:palette.joint},leg);
  var knee=vx('circle',{r:3.5,fill:palette.joint,stroke:'#1a6947','stroke-width':.8,filter:filter},leg);
  var foot=vx('circle',{r:3,fill:palette.joint,stroke:'#1a6947','stroke-width':.8,filter:filter},leg);
  legs.push({side:side,row:row,shadow:shadow,upper:upper,lower:lower,knee:knee,foot:foot});
 }});
 var body=vx('g',{'data-spider-body':'1'},spider);
 vx('ellipse',{cx:0,cy:9,rx:21,ry:24,fill:'#394a9c',opacity:.2,filter:filter},body);
 vx('path',{d:'M-15 -4Q-24 8 -15 26Q0 36 15 26Q24 8 15 -4Q0 -12 -15 -4Z',fill:'url(#'+id+'shell)',stroke:palette.shell,'stroke-width':2,filter:filter},body);
 vx('path',{d:'M-11 0Q0 -6 11 0L14 18Q0 29 -14 18Z',fill:'#182446',stroke:'#455fbc','stroke-width':.8},body);
 vx('circle',{cx:0,cy:10,r:6,fill:palette.core,filter:filter},body);
 vx('circle',{cx:0,cy:10,r:2.6,fill:'#ffe6fa'},body);
 vx('path',{d:'M-12 -5L-14 -20L-8 -26H8L14 -20L12 -5Z',fill:'#131b37',stroke:palette.shell,'stroke-width':1.5,filter:filter},body);
 [-7,0,7].forEach(function(x){vx('circle',{cx:x,cy:-17,r:1.5,fill:'#fca3d8'},body);vx('circle',{cx:x*.8,cy:-21,r:1,fill:'#99bdff'},body)});
 vx('path',{d:'M-5 -25L-6 -32M5 -25L6 -32',stroke:palette.shell,'stroke-width':1.2,'stroke-linecap':'round'},body);
 var avatar=e.avatar||'drone';
 function select(kind){if(kind!=='spider'&&kind!=='drone')throw new Error('avatar must be spider or drone');avatar=kind;robot.style.display=kind==='drone'?'':'none';spider.style.display=kind==='spider'?'':'none'}
 select(avatar);AVATARS.push(select);
 var targets=e.targets||[],path=e.path||[[90,85],[800,60],[330,250],[820,540],[130,600]],tags=[];
 (e.words||[]).forEach(function(w,i){var gg=vx('g',{},wordGroup);vx('rect',{x:w.x-2,y:w.y-9,width:w.w,height:13,rx:2,fill:'#141511','fill-opacity':.8,stroke:['#62c4d2','#e4bc62','#e768ac','#79cf9f'][i%4],'stroke-width':.65},gg);vtext(gg,w.x,w.y,w.t,['#62c4d2','#e4bc62','#e768ac','#79cf9f'][i%4],7);tags.push(gg)});
 function routePoint(i){return path[sequence?sequence[mod(i,sequence.length)]%path.length:mod(i,path.length)]}
 COMPONENTS.push(function(t){var u=phase(t-offset,e.period||34),seg=u*(sequence?sequence.length:path.length),k=Math.floor(seg),local=seg-k,f=smooth(local),a=routePoint(k),b=routePoint(k+1),x=a[0]+(b[0]-a[0])*f,y=a[1]+(b[1]-a[1])*f,angle=Math.sin(t*.9)*15+Math.atan2(b[1]-a[1],b[0]-a[0])*180/Math.PI*.13,scale=e.avatarScale||1;
  if(avatar==='spider'){
   function heading(i){var p=routePoint(i),q=routePoint(i+1);return 90+Math.atan2(q[1]-p[1],q[0]-p[0])*180/Math.PI}
   angle=heading(k);if(local<.25)angle=blendHeading(heading(k-1),angle,.5+.5*smooth(local/.25));else if(local>.75)angle=blendHeading(angle,heading(k+1),.5*smooth((local-.75)/.25));
   if(e.avatarHeading!=null)angle=e.avatarHeading;
   var margin=92*scale;x=Math.max(margin,Math.min(e.w-margin,x));y=Math.max(margin,Math.min(e.h-margin,y));
   body.setAttribute('transform','translate(0 '+(Math.sin(t*(e.gaitSpeed||7.2))*.9)+')');
   legs.forEach(function(L){var row=L.row,side=L.side,step=Math.sin(t*(e.gaitSpeed||7.2)+(row%2+(side===1?1:0))*Math.PI),lift=Math.max(0,step),hip=[side*16,-14+row*9],knee=[side*([43,53,53,43][row]+lift*2),[-24,-9,13,29][row]+step*3],foot=[side*([55,67,67,55][row]-lift*5),[-56,-25,25,56][row]+step*7];
    var d='M'+hip.join(' ')+'L'+knee.join(' ')+'L'+foot.join(' ');L.shadow.setAttribute('d',d);L.upper.setAttribute('d','M'+hip.join(' ')+'L'+knee.join(' '));L.lower.setAttribute('d','M'+knee.join(' ')+'L'+foot.join(' '));L.knee.setAttribute('cx',knee[0]);L.knee.setAttribute('cy',knee[1]);L.foot.setAttribute('cx',foot[0]);L.foot.setAttribute('cy',foot[1]);L.foot.setAttribute('r',3+lift*.6);L.foot.setAttribute('opacity',.68+.32*lift);
   });
  }
  g.setAttribute('transform','translate('+x+' '+y+') rotate('+angle+')'+(scale!==1?' scale('+scale+')':''));fans.forEach(function(n,i){n.setAttribute('transform','rotate('+(Math.sin(t*2.5+i*.7)*5)+')')});
  var targetIndex=sequence?Number(V[e.timelineMachine+'.i']):Math.floor(t/(e.focusPeriod||3)),target=targets[mod(targetIndex,targets.length)];if(target){var on=phase(t-offset,e.focusPeriod||3)<.83;focus.setAttribute('x',target.x);focus.setAttribute('y',target.y);focus.setAttribute('width',target.w);focus.setAttribute('height',target.h);focus.setAttribute('opacity',on?.85:0);wire.setAttribute('d','M'+x+' '+y+'L'+(target.x+target.w/2)+' '+(target.y+target.h/2));wire.setAttribute('opacity',on?.5:0)}
  tags.forEach(function(n,i){n.setAttribute('opacity',Math.sin(t*1.5-i*.3)>.2?1:0)});
 });
};

// Include vector text in the existing DOM layout validator. Sprite overlays and
// intentional decorative overlaps are excluded; authored text is checked.
// __check is installed below by the base template, so boot installs the wrapper.
var baseVectorBoot=boot;
boot=function(c){baseVectorBoot(c);var old=window.__check;window.__check=function(){var p=old();ST.querySelectorAll('[data-vector-text],[data-component-text]').forEach(function(n){var b=n.getBBox(),svg=n.ownerSVGElement;if(svg.getAttribute('data-component')==='drone')return;var m=svg.getScreenCTM().inverse().multiply(n.getScreenCTM()),pts=[[b.x,b.y],[b.x+b.width,b.y],[b.x,b.y+b.height],[b.x+b.width,b.y+b.height]].map(function(q){return new DOMPoint(q[0],q[1]).matrixTransform(m)});if(pts.some(function(q){return q.x<-.5||q.y<-.5||q.x>Number(svg.getAttribute('width'))+.5||q.y>Number(svg.getAttribute('height'))+.5}))p.push('vector text outside panel: '+n.textContent)});return p}};
