/* Four palettes share the same authored geometry and semantic color roles.
 * Palette IDs remain stable; component recoloring runs after draw callbacks. */
function editorialPalette(e){
 var globalTheme=cfg.theme||{},localTheme=e&&e.theme||{},variant=localTheme.variant||localTheme.preset||globalTheme.variant||globalTheme.preset||'terminal-dark';
 var light=variant==='light-pastel'||variant==='pastel-classic',classic=variant==='terminal-classic'||variant==='pastel-classic';
 var palettes={
  "terminal-dark": {
    "bg": "#191713",
    "panel": "#25221b",
    "surface": "#211e18",
    "line": "#958871",
    "fg": "#fff5e6",
    "dim": "#d0c1aa",
    "amber": "#f3cf88",
    "cyan": "#8de1ee",
    "pink": "#ff9bcc",
    "mint": "#a7e6bd",
    "red": "#ff9a88",
    "blue": "#aacff7"
  },
  "light-pastel": {
    "bg": "#faf7f0",
    "panel": "#fffdf8",
    "surface": "#f2ecdf",
    "line": "#978a76",
    "fg": "#24211c",
    "dim": "#62584a",
    "amber": "#885412",
    "cyan": "#216674",
    "pink": "#943768",
    "mint": "#326743",
    "red": "#a1382b",
    "blue": "#2f568d"
  },
  "terminal-classic": {
    "bg": "#191f27",
    "panel": "#222a35",
    "surface": "#1e2630",
    "line": "#8395ad",
    "fg": "#f6f8ff",
    "dim": "#c0cbd9",
    "amber": "#f2ca80",
    "cyan": "#80dfef",
    "pink": "#c7acff",
    "mint": "#89e7b4",
    "red": "#ff786f",
    "blue": "#9bbeff"
  },
  "pastel-classic": {
    "bg": "#ffffff",
    "panel": "#ffffff",
    "surface": "#f1f4f8",
    "line": "#8996a8",
    "fg": "#18212f",
    "dim": "#526174",
    "amber": "#9f4800",
    "cyan": "#146f70",
    "pink": "#723d9d",
    "mint": "#326b25",
    "red": "#b72b36",
    "blue": "#275bac"
  }
};
 var C=Object.assign({},palettes[variant]||palettes[light?'light-pastel':'terminal-dark']);
 [globalTheme.colors||{},localTheme.colors||{}].forEach(function(colors){
  ['bg','panel','surface','line','fg','dim'].forEach(function(k){if(colors[k])C[k]=colors[k]});
  [['amber','ye'],['cyan','cy'],['pink','pi'],['mint','gr'],['red','rd'],['blue','bl']].forEach(function(k){if(colors[k[0]]||colors[k[1]])C[k[0]]=colors[k[0]]||colors[k[1]]});
 });
 C.light=light;C.variant=variant;C.recolor=true;
 C.tint=function(color,paper){
  function rgb(s){var m=/^#([0-9a-f]{6})$/i.exec(s||'');return m?[0,2,4].map(function(i){return parseInt(m[1].slice(i,i+2),16)}):null}
  var a=rgb(color),b=rgb(C.panel);if(!a||!b)return color;
  return '#'+a.map(function(v,i){return Math.round(v*(1-paper)+b[i]*paper).toString(16).padStart(2,'0')}).join('');
 };
 var primary={'#12110f':'bg','#191713':'panel','#171511':'surface','#3c352c':'line','#eee9df':'fg','#9f9587':'dim','#dfb96d':'amber','#64bed0':'cyan','#e776af':'pink','#88c4a2':'mint','#d77768':'red'};
 var fills={
  '#181611':'paper','#201d18':'paper','#171512':'surface','#211b1a':'surface','#201c16':'paper','#1b1815':'paper','#1d1a15':'paper','#171714':'paper',
  '#16303a':'cyan','#1a3032':'cyan','#19272a':'cyan','#183036':'cyan','#1b2628':'cyan','#182326':'cyan',
  '#251f15':'amber','#302619':'amber','#272117':'amber','#2b2418':'amber',
  '#1e3b2a':'mint','#17221b':'mint','#203324':'mint','#1b291f':'mint','#1c2b21':'mint','#1b241b':'mint','#1e2b21':'mint',
  '#251c21':'pink','#271d23':'pink','#271b16':'red','#2a1c17':'red',
  '#31292a':'track','#292620':'track','#343b2d':'track','#362b30':'track'
 };
 var lines={'#625643':'line','#76654b':'line','#75664d':'line','#655d51':'line','#625b50':'dim','#796f62':'dim','#786b61':'dim','#4e6f5b':'mint','#70473d':'red','#61503a':'line','#88704a':'amber','#c9a86e':'amber','#615039':'line','#584d3a':'line'};
 var icons={'#fff6de':'fg','#f0e7d8':'fg','#c6f5f4':'cyan','#ffe7f0':'pink','#c6efd5':'mint','#d8ffe8':'mint'};
 var componentColors={
  '#d9d8d2':'fg','#d5d4ce':'fg','#73716c':'dim','#d4a7c0':'pink','#636668':'line','#aaa9a5':'line','#161718':'fg','#8d8c84':'dim','#53b9c5':'cyan','#142125':'fg','#625e55':'line','#382816':'amber','#eab961':'amber','#ec55a6':'pink','#5e5c54':'dim','#e954a7':'pink','#f48ac1':'pink','#6e625f':'dim','#f060b2':'pink','#393832':'line','#e7bd66':'amber','#57c5d8':'cyan','#f164b2':'pink','#70d6b0':'mint','#96928a':'dim','#e45a9d':'pink','#e7bb67':'amber',
  '#80796d':'line','#e44e99':'pink','#737577':'dim','#447cb0':'blue','#d67d61':'red','#debb66':'amber','#69bba0':'mint','#f1efdf':'fg','#979286':'dim','#f268b5':'pink','#ed61ad':'pink','#91908a':'dim','#598bc1':'blue','#34332d':'line','#cac6ba':'fg','#858278':'dim',
  '#9d9b90':'dim','#e6ba67':'amber','#609dd0':'blue','#73c89d':'mint','#aaa89b':'line','#caae70':'amber','#e9e4d2':'fg','#71bf93':'mint','#62cca4':'mint','#71dab0':'mint','#ccc8bd':'fg','#8a867b':'dim',
  '#818d96':'dim','#5797d2':'blue','#e1579b':'pink','#bc9f54':'amber','#6fba92':'mint','#64b18f':'mint','#f0efdf':'fg','#48886c':'mint','#7acfaa':'mint','#a0e3b6':'mint','#dbd9cd':'fg','#a6aaac':'dim','#609cce':'blue','#dbb865':'amber','#78cda5':'mint','#eeeade':'fg','#70bf97':'mint','#7baf8c':'mint','#d4d7c8':'fg',
  '#686657':'line','#a09c66':'amber','#5da98a':'mint','#bcae78':'amber','#62c795':'mint','#8beac0':'mint','#efc875':'amber','#bab8ae':'fg','#c9c4b6':'dim','#49463d':'line','#a55457':'red','#e8be6c':'amber','#78d3a4':'mint',
  '#f5d99b':'amber','#211a13':'fg','#fcf1fc':'fg','#dbd4c6':'dim','#ed5cac':'pink','#ef553e':'red','#62dd9b':'mint','#155c38':'mint','#6bea9b':'mint','#1b663a':'mint','#80a9ff':'blue','#527bbb':'blue','#f754b2':'pink','#aec5ff':'blue','#ff594b':'red','#74f3a9':'mint','#769fff':'blue','#ff65c8':'pink','#1a6947':'mint','#455fbc':'blue','#ffe6fa':'fg','#fca3d8':'pink','#99bdff':'blue','#62c4d2':'cyan','#e4bc62':'amber','#e768ac':'pink','#79cf9f':'mint'
 };
 var componentFills={'#351c2b':'pink','#27241c':'paper','#282e24':'track','#304c35':'mint','#24221b':'paper','#202d61':'blue','#131d3c':'blue','#34477a':'blue','#10152d':'paper','#394a9c':'blue','#182446':'blue','#131b37':'blue','#141511':'paper'};
 C.shade=function(color){
  var key=String(color||'').toLowerCase();
  if(primary[key])return C[primary[key]];
  if(!C.recolor)return color;
  if(!light&&(key==='#161718'||key==='#142125'||key==='#211a13'))return C.bg;
  if(classic&&(key==='#d68865'||key==='#9d9acc'))return C[key==='#d68865'?'red':'pink'];
  if(classic&&key==='#e0efe4')return light?C.tint(C.mint,.92):C.tint(C.mint,.65);
  if(classic&&key==='#203b3b')return C.tint(C.cyan,.82);
  var role=fills[key]||componentFills[key];
  if(role==='paper')return C.panel;if(role==='surface')return C.surface;if(role==='track')return C.tint(C.dim,.79);if(role)return C.tint(C[role],.88);
  if(lines[key]||icons[key]||componentColors[key])return C[lines[key]||icons[key]||componentColors[key]];
  if(key==='#fff5df')return C.tint(C.amber,.97);
  if(key==='#28231b')return C.panel;if(key==='#30271d')return C.tint(C.amber,.88);if(key==='#1b1813')return C.surface;
  if(key==='#ffd7ef')return C.tint(C.pink,.94);if(key==='#461630')return C.tint(C.pink,.82);if(key==='#e84a9c')return C.pink;
  return color;
 };
 return C;
}

var baseEditorialThemeBoot=boot;
boot=function(c){
 baseEditorialThemeBoot(c);
 var author=(c.elements||[]).filter(function(e){return /^(rag|agent|request|incident|knowledge|workflow|lab|avatar)Editorial$/.test(e.type)})[0];
 if(!author)return;
 var C=editorialPalette(author);if(!C.recolor)return;
 var kinds=['orb','seats','donut','ghostSeats','ribbons','kanban','drone'];
 var scopes=Array.from(ST.querySelectorAll('svg[data-component]')).filter(function(svg){return kinds.indexOf(svg.getAttribute('data-component'))>=0});
 // Reuse the authored token when a previous mapping is still on the node.
 // Draw callbacks can write a new token; newly inserted nodes start uncached.
 var sourceTokens=new WeakMap();
 COMPONENTS.push(function(){
  scopes.forEach(function(svg){
   svg.querySelectorAll('[fill],[stroke],[stop-color]').forEach(function(n){
    var saved=sourceTokens.get(n);if(!saved){saved={};sourceTokens.set(n,saved)}
    ['fill','stroke','stop-color'].forEach(function(attr){if(!n.hasAttribute(attr))return;var current=n.getAttribute(attr),last=saved[attr],original=last&&current===last.mapped?last.source:current,mapped=C.shade(original);
     if(attr==='stop-color'&&original==='#e84a9c')mapped=C.tint(C.pink,C.light?.6:.12);
     saved[attr]={source:original,mapped:mapped};
     if(mapped!==current)n.setAttribute(attr,mapped);
    });
   });
   if(C.light)svg.querySelectorAll('feGaussianBlur').forEach(function(n){if(Number(n.getAttribute('stdDeviation'))>2)n.setAttribute('stdDeviation','1.5')});
  });
 });
};
