/* Optional terminal presentation for authored scenes. All state follows seek(t).
 * Diagram presentation leaves every original node and pixel untouched. */
function installTerminalShell(presentation){
 var author=(cfg.elements||[]).filter(function(e){return /^(rag|agent|request|incident|knowledge|workflow|lab|avatar)Editorial$/.test(e.type)})[0];
 if(!author)return;
 var C=editorialPalette(author),ns='http://www.w3.org/2000/svg',font='LP Mono, LP Sans, monospace';
 function node(tag,attrs,parent){var n=document.createElementNS(ns,tag);Object.keys(attrs||{}).forEach(function(k){n.setAttribute(k,attrs[k])});if(parent)parent.appendChild(n);return n}
 function text(parent,x,y,value,color,size,attrs){var n=node('text',Object.assign({x:x,y:y,fill:color,'font-size':size,'font-family':font,'data-terminal-text':'1'},attrs||{}),parent);n.textContent=value;return n}
 function fit(n,value,width){n.textContent=value;while(n.getComputedTextLength()>width&&value.length>1){value=value.slice(0,-1);n.textContent=value+'…'}return n.getComputedTextLength()}
 function clock(seconds){var minutes=Math.floor(seconds/60),rest=Math.max(0,seconds-minutes*60);return String(minutes).padStart(2,'0')+':'+rest.toFixed(1).padStart(4,'0')}
 var duration=Math.max(.01,Number(cfg.canvas&&cfg.canvas.duration)||12),sceneId=String(presentation.sceneId||'diagram');
 var events=(presentation.events||[]).map(function(event,index){return {t:Number(event.t),actor:String(event.actor||'demo'),text:String(event.text||''),index:index}})
  .filter(function(event){return Number.isFinite(event.t)&&event.t>=0&&event.t<duration})
  .sort(function(a,b){return a.t-b.t||a.index-b.index});
 var command=String(presentation.command||''),title=String(presentation.title||'~/motion-diagram-studio/'+sceneId+' — zsh');
 ST.querySelectorAll('[data-diagram-header],[data-diagram-footer]').forEach(function(n){n.style.display='none'});
 ST.style.borderRadius='12px';

 // Literal ASCII forms the frame; neon still follows the original rectangles.
 var borders=Array.from(ST.querySelectorAll('rect[data-neon-border]')).map(function(source){
  var b=source.getBBox(),group=node('g',{'data-terminal-border':source.getAttribute('data-neon-border'),'aria-hidden':'true','pointer-events':'none','font-family':font,'font-size':12},source.parentNode);
  if(source.hasAttribute('transform'))group.setAttribute('transform',source.getAttribute('transform'));
  var step=7.2,columns=Math.max(3,Math.floor(b.width/step)),edge='+'+'-'.repeat(columns-1)+'+';
  [b.y,b.y+b.height].forEach(function(y){var n=node('text',{x:b.x-step/2,y:y,'dominant-baseline':'central',textLength:b.width+step,lengthAdjust:'spacing'},group);n.textContent=edge});
  var rows=Math.max(2,Math.ceil(b.height/16));
  for(var row=1;row<rows;row++)[b.x,b.x+b.width].forEach(function(x){var n=node('text',{x:x,y:b.y+b.height*row/rows,'text-anchor':'middle','dominant-baseline':'central'},group);n.textContent='|'});
  source.style.strokeOpacity='0';
  return {source:source,group:group,color:source.getAttribute('data-neon-color')||C.line};
 });

 var shell=node('svg',{width:CW,height:CH,viewBox:'0 0 '+CW+' '+CH,'data-terminal-shell':sceneId,'aria-label':'Simulated terminal presentation'},ST);
 shell.style.cssText='position:absolute;left:0;top:0;pointer-events:none;z-index:3;overflow:hidden';
 var bar=C.light?'#e8edf3':'#252d38';
 node('rect',{x:0,y:0,width:CW,height:40,fill:bar},shell);
 [20,42,64].forEach(function(x,i){node('circle',{cx:x,cy:20,r:6.5,fill:['#ff5f57','#febc2e','#28c840'][i],'data-terminal-traffic-light':String(i)},shell)});
 var titleNode=text(shell,CW/2,24,title,C.dim,12,{'text-anchor':'middle','data-terminal-title':'1'});
 text(shell,CW-28,24,'SIMULATED',C.dim,10,{'text-anchor':'end'});
 node('path',{d:'M0 40H'+CW,stroke:C.line,'stroke-width':1},shell);
 node('rect',{x:.6,y:.6,width:CW-1.2,height:CH-1.2,rx:11.4,fill:'none',stroke:C.line,'stroke-width':1,'stroke-opacity':.75},shell);

 // The footer starts below every 12px block-export margin (maximum y = 1205).
 var footerY=CH-68;
 node('rect',{x:0,y:footerY,width:CW,height:68,fill:C.surface},shell);
 node('path',{d:'M28 '+footerY+'H'+(CW-28),stroke:C.line,'stroke-width':1},shell);
 var rows=[footerY+18,footerY+35].map(function(y,i){return {
  time:text(shell,28,y,'',C.dim,12),actor:text(shell,112,y,'',C.cyan,12),
  spin:text(shell,204,y,'',C.amber,12),message:text(shell,222,y,'',C.fg,12,{'data-terminal-log':String(i)})
 }});
 var promptY=footerY+54;
 text(shell,28,promptY,'studio $',C.mint,12,{'data-terminal-prompt':'1'});
 var commandNode=text(shell,100,promptY,'',C.fg,12,{'data-terminal-command':'1'});
 var cursor=node('rect',{x:100,y:promptY-11,width:7,height:13,fill:C.fg,'data-terminal-cursor':'1'},shell);

 COMPONENTS.push(function(t){
  var sec=mod(t,duration);
  ST.querySelectorAll('svg[data-component] [data-component-text]').forEach(function(n){if(n.getAttribute('font-family')!==font)n.setAttribute('font-family',font)});
  borders.forEach(function(border){border.group.setAttribute('fill',border.source.getAttribute('stroke')||border.color)});
  fit(titleNode,title,CW-230);
  var visible=events.filter(function(event){return event.t<=sec}),last=visible.slice(-2);
  rows.forEach(function(row,i){var event=last[i],value=event?event.text:'';
   row.time.textContent=event?clock(event.t):'';fit(row.actor,event?event.actor:'',82);
   row.spin.textContent=event&&i===last.length-1?'|/-\\'[Math.floor(sec*8)%4]:'';
   fit(row.message,value,CW-250);
  });
  var typed=command.slice(0,Math.max(0,Math.floor(sec*48))),length=fit(commandNode,typed,CW-136);
  cursor.setAttribute('x',Math.min(CW-35,100+length+3));
  cursor.setAttribute('opacity',mod(sec,.9)<.55?1:0);
 });
}
var baseTerminalShellBoot=boot;
boot=function(c){
 baseTerminalShellBoot(c);
 if(c.presentation&&c.presentation.style==='terminal')installTerminalShell(c.presentation);
};
