/* A short, tapered light travels around each authored function-block border.
 * Geometry and phase are derived only from seek(t); original state borders stay intact. */
function installNeonFlow(options){
 var NS='http://www.w3.org/2000/svg',light=TH.preset==='light-pastel';
 function node(tag,attrs,parent){var n=document.createElementNS(NS,tag);Object.keys(attrs).forEach(function(k){n.setAttribute(k,attrs[k])});parent.appendChild(n);return n}
 function positive(value,fallback){value=Number(value);return Number.isFinite(value)&&value>0?value:fallback}
 function wrap(value,length){return ((value%length)+length)%length}
 var intensity=options.intensity==null?.8:Number(options.intensity);
 intensity=Number.isFinite(intensity)?Math.max(0,Math.min(1,intensity)):.8;
 var borders=Array.from(ST.querySelectorAll('rect[data-neon-border]')),tracks=[];
 borders.forEach(function(source,index){
  var length=source.getTotalLength();if(!Number.isFinite(length)||length<=0)return;
  var hero=source.getAttribute('data-neon-role')==='hero',color=source.getAttribute('data-neon-color')||TH.colors.amber;
  var period=positive(hero?options.heroPeriod:options.period,hero?12:6);
  var tail=Math.min(length*.3,positive(options.tail,144)*(hero?1.35:1));
  var svg=source.ownerSVGElement,defs=svg.querySelector('defs')||node('defs',{},svg);
  var filterId='lp-neon-halo-'+index,box=source.getBBox();
  var filter=node('filter',{id:filterId,filterUnits:'userSpaceOnUse',x:box.x-12,y:box.y-12,width:box.width+24,height:box.height+24,'color-interpolation-filters':'sRGB'},defs);
  node('feGaussianBlur',{stdDeviation:light?1.7:2.5},filter);
  var layer=node('g',{'data-neon-layer':source.getAttribute('data-neon-border'),'pointer-events':'none','aria-hidden':'true'},source.parentNode);
  function outline(extra){var attrs={fill:'none',stroke:color,'stroke-linecap':'round','stroke-width':1.25};
   ['x','y','width','height','rx','ry','transform'].forEach(function(k){if(source.hasAttribute(k))attrs[k]=source.getAttribute(k)});
   return node('rect',Object.assign(attrs,extra),layer)}
  var halo=outline({'data-neon-halo':'1','stroke-width':5,filter:'url(#'+filterId+')',opacity:light?.1:.3,'stroke-dasharray':tail+' '+(length-tail)});
  var segments=[],count=8,piece=tail/count;
  for(var j=0;j<count;j++)segments.push(outline({opacity:(.94*Math.pow(1-j/count,1.7)).toFixed(4),'stroke-dasharray':(piece+.5)+' '+(length-piece-.5)}));
  var tip=outline({stroke:light?color:'#fff1d4','stroke-width':.85,opacity:light?.65:.75,'stroke-dasharray':'12 '+(length-12)});
  var head=node('circle',{'data-neon-head':'1',r:hero?1.7:1.5,fill:light?color:'#fff5df'},layer);
  if(source.hasAttribute('transform'))head.setAttribute('transform',source.getAttribute('transform'));
  tracks.push({source:source,layer:layer,halo:halo,segments:segments,tip:tip,head:head,length:length,tail:tail,piece:piece,period:period,
   phase:wrap(index*.173+(hero?.09:0),1),hero:hero,baseStroke:source.getAttribute('stroke')});
 });
 COMPONENTS.push(function(t){
  tracks.forEach(function(track){
   var u=wrap(t/track.period+track.phase,1),position=u*track.length;
   var active=track.hero||track.source.getAttribute('stroke')!==track.baseStroke;
   var strength=(active?.94:.65)*(.94+.06*Math.sin(u*Math.PI*2));
   track.layer.setAttribute('opacity',(intensity*strength).toFixed(4));
   track.halo.setAttribute('stroke-dashoffset',(-(position-track.tail)).toFixed(4));
   track.segments.forEach(function(segment,j){segment.setAttribute('stroke-dashoffset',(-(position-(j+1)*track.piece)).toFixed(4))});
   track.tip.setAttribute('stroke-dashoffset',(-(position-12)).toFixed(4));
   var point=track.source.getPointAtLength(position);
   track.head.setAttribute('cx',point.x.toFixed(4));track.head.setAttribute('cy',point.y.toFixed(4));
  });
 });
}
var baseNeonBoot=boot;
boot=function(c){
 baseNeonBoot(c);
 var options=c.effects&&c.effects.neon;
 if(options&&options.enabled!==false)installNeonFlow(options===true?{}:options);
};
