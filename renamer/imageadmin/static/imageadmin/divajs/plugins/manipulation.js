!function(t){var e={};function a(i){if(e[i])return e[i].exports;var n=e[i]={i:i,l:!1,exports:{}};return t[i].call(n.exports,n,n.exports,a),n.l=!0,n.exports}a.m=t,a.c=e,a.d=function(t,e,i){a.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:i})},a.r=function(t){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},a.t=function(t,e){if(1&e&&(t=a(t)),8&e)return t;if(4&e&&"object"==typeof t&&t&&t.__esModule)return t;var i=Object.create(null);if(a.r(i),Object.defineProperty(i,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var n in t)a.d(i,n,function(e){return t[e]}.bind(null,n));return i},a.n=function(t){var e=t&&t.__esModule?function(){return t.default}:function(){return t};return a.d(e,"a",e),e},a.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},a.p="/build/plugins/",a(a.s=1)}([,function(t,e,a){"use strict";a.r(e),a.d(e,"default",(function(){return V}));let i=[],n=!1;function s(){i=[],n=!1}function l(t,e,a,l){let r=i.findIndex(t=>t.filter.name===e.name);if(-1!==r){let t=i[r];t.adjust=a,"Sharpness"===t.name?0===t.adjust[1]?t.postData=t.prevData:t.postData=j(t.prevData,t.adjust):"Invert"===t.name?(t.postData=o(t.postData,t.filter,t.adjust),n=!n):t.postData=o(t.prevData,t.filter,t.adjust);for(let t=r+1,e=i.length;t<e;t++){let a=i[t];if(("Invert"!==a.name||n)&&(a.prevData=i[t-1].postData,"Sharpness"===a.name?0===a.adjust[1]?a.postData=a.prevData:a.postData=j(a.prevData,a.adjust):a.postData=o(a.prevData,a.filter,a.adjust),t===e-1))return a.postData}return t.postData}{if("Threshold"===l||i[0]&&"Threshold"===i[0].name){s();let t=document.getElementsByClassName("manipulation-tools")[0];for(let e=0,a=t.children.length;e<a;e++){let a=t.children[e].children[0];if(a&&"range"===a.type){let t=a.parentElement.textContent.includes("Threshold"),e=a.parentElement.textContent.includes("Zoom"),i=a.parentElement.textContent.includes("Rotation");"Threshold"!==l||t||e||i?"Threshold"!==l&&t&&(a.value=0):a.value=0}}document.getElementById("filter-log").innerHTML="<h3> Filter Application Order <h3>"}i.push({filter:e,prevData:0===i.length?t:i[i.length-1].postData,adjust:a,name:l});let r=i[i.length-1];"Sharpness"===r.name?r.postData=j(r.prevData,r.adjust):r.postData=o(r.prevData,r.filter,r.adjust),"Invert"===r.name&&(n=!0);let d=document.createElement("p");return d.setAttribute("style","color: white; margin: 0;"),d.innerText=r.name,document.getElementById("filter-log").appendChild(d),r.postData}}function r(t,e){return document.createElement("canvas").getContext("2d").createImageData(t,e)}function o(t,e,a){let i=function(t,e,a){let i=t.length;for(let n=0;n<i;n+=4){let i=e(t[n],t[n+1],t[n+2],a);t[n]=i[0],t[n+1]=i[1],t[n+2]=i[2],t[n+3]=i[3]}return t}(new Uint8ClampedArray(t.data),e,a),n=r(t.width,t.height);return n.data.set(i),n}function d(t){return l(t,c,null,"Grayscale")}function c(t,e,a){let i=.3*t+.59*e+.11*a;return[i,i,i,255]}function h(t,e){return l(t,u,e,"Saturation")}function u(t,e,a,i){let n=-.01*i,s=Math.max(t,e,a);return[t!==s?t+(s-t)*n:t,e!==s?e+(s-e)*n:e,a!==s?a+(s-a)*n:a,255]}function m(t,e){return l(t,p,e,"Vibrance")}function p(t,e,a,i){let n=-1*i,s=Math.max(t,e,a),l=t+e+a/3,r=2*Math.abs(s-l)/255*n/100;return[t!==s?t+(s-t)*r:t,e!==s?e+(s-e)*r:e,a!==s?a+(s-a)*r:a,255]}function g(t,e){return l(t,b,e,"Brightness")}function b(t,e,a,i){let n=Math.floor(i/100*255);return[t+n,e+n,a+n,255]}function v(t,e){return l(t,f,e,"Contrast")}function f(t,e,a,i){let n=Math.pow((i+100)/100,2),s=t,l=e,r=a;return s/=255,s-=.5,s*=n,s+=.5,s*=255,l/=255,l-=.5,l*=n,l+=.5,l*=255,r/=255,r-=.5,r*=n,r+=.5,r*=255,[s,l,r,255]}function _(t){return l(t,C,null,"Invert")}function C(t,e,a){return[255-t,255-e,255-a,255]}function E(t,e){return l(t,y,e,"Threshold")}function y(t,e,a,i){let n=.2126*t+.7152*e+.0722*a>=i?255:0;return[n,n,n,255]}function A(t,e){return l(t,L,e,"Hue")}function L(t,e,a,i){let{h:n,s:s,v:l}=function(t,e,a){let i=t,n=e,s=a;i/=255,n/=255,s/=255;let l,r=Math.max(i,n,s),o=Math.min(i,n,s),d=r,c=r-o,h=0===r?0:c/r;if(r===o)l=0;else{switch(r){case i:l=(n-s)/c+(n<s?6:0);break;case n:l=(s-i)/c+2;break;case s:l=(i-n)/c+4}l/=6}return{h:l,s:h,v:d}}(t,e,a);n*=100,n+=Math.abs(i),n%=100,n/=100;let r=function(t,e,a){let i,n,s,l,r,o,d,c;switch(l=Math.floor(6*t),n=6*t-l,r=a*(1-e),o=a*(1-n*e),c=a*(1-(1-n)*e),l%6){case 0:d=a,s=c,i=r;break;case 1:d=o,s=a,i=r;break;case 2:d=r,s=a,i=c;break;case 3:d=r,s=o,i=a;break;case 4:d=c,s=r,i=a;break;case 5:d=a,s=r,i=o}return{r:Math.floor(255*d),g:Math.floor(255*s),b:Math.floor(255*i)}}(n,s,l);return[r.r,r.g,r.b,255]}function x(t,e){return l(t,w,e,"Gamma")}function w(t,e,a,i){let n=i/100+1;return n<0&&(n*=-1),[255*Math.pow(t/255,n),255*Math.pow(e/255,n),255*Math.pow(a/255,n),255]}function T(t,e){return l(t,I,e,"CC Red")}function I(t,e,a,i){let n=i/100;return[n>0?t+(255-t)*n:t-t*Math.abs(n),e,a,255]}function D(t,e){return l(t,k,e,"CC Green")}function k(t,e,a,i){let n=i/100;return[t,n>0?e+(255-e)*n:e-e*Math.abs(n),a,255]}function M(t,e){return l(t,z,e,"CC Blue")}function z(t,e,a,i){let n=i/100;return[t,e,n>0?a+(255-a)*n:a-a*Math.abs(n),255]}function j(t,e,a){let i=Math.round(Math.sqrt(e.length)),n=Math.floor(i/2),s=t.data,l=t.width,o=t.height,d=l,c=o,h=r(d,c),u=h.data,m=a?1:0;for(let t=0;t<c;t++)for(let a=0;a<d;a++){let r=t,c=a,h=4*(t*d+a),p=0,g=0,b=0,v=0;for(let t=0;t<i;t++)for(let a=0;a<i;a++){let d=r+t-n,h=c+a-n;if(d>=0&&d<o&&h>=0&&h<l){let n=4*(d*l+h),r=e[t*i+a];p+=s[n]*r,g+=s[n+1]*r,b+=s[n+2]*r,v+=s[n+3]*r}}u[h]=p,u[h+1]=g,u[h+2]=b,u[h+3]=v+m*(255-v)}return h}function S(t,e){let a=e||100;return a/=100,0===e&&(a=0),l(t,j,[0,-a,0,-a,4*a+1,-a,0,-a,0],"Sharpness")}var X={onDoubleClick:function(t,e){t.addEventListener("dblclick",(function(t){t.ctrlKey||e(t,N(t.currentTarget,t))}));const a=B(500);t.addEventListener("contextmenu",(function(t){t.preventDefault(),t.ctrlKey&&(a.isTriggered()?(a.reset(),e(t,N(t.currentTarget,t))):a.trigger())}))},onPinch:function(t,e){let a=0;t.addEventListener("touchstart",(function(t){t.preventDefault(),2===t.originalEvent.touches.length&&(a=Y(t.originalEvent.touches[0].clientX,t.originalEvent.touches[0].clientY,t.originalEvent.touches[1].clientX,t.originalEvent.touches[1].clientY))})),t.addEventListener("touchmove",(function(t){if(t.preventDefault(),2===t.originalEvent.touches.length){const i=t.originalEvent.touches,n=Y(i[0].clientX,i[0].clientY,i[1].clientX,i[1].clientY),s=n-a;if(Math.abs(s)>0){const s={pageX:(i[0].clientX+i[1].clientX)/2,pageY:(i[0].clientY+i[1].clientY)/2};e(t,N(t.currentTarget,s),a,n)}}}))},onDoubleTap:function(t,e){const a=B(250);let i=null;t.addEventListener("touchend",t=>{if(t.preventDefault(),a.isTriggered()){a.reset();const n={pageX:t.originalEvent.changedTouches[0].clientX,pageY:t.originalEvent.changedTouches[0].clientY};Y(i.pageX,i.pageY,n.pageX,n.pageY)<50&&e(t,N(t.currentTarget,n)),i=null}else i={pageX:t.originalEvent.changedTouches[0].clientX,pageY:t.originalEvent.changedTouches[0].clientY},a.trigger()})}};function Y(t,e,a,i){return Math.sqrt((a-t)*(a-t)+(i-e)*(i-e))}function B(t){let e=!1,a=null;return{trigger(){e=!0,i(),a=setTimeout((function(){e=!1,a=null}),t)},isTriggered:()=>e,reset(){e=!1,i()}};function i(){null!==a&&(clearTimeout(a),a=null)}}function N(t,e){const a=t.getBoundingClientRect();return{left:e.pageX-a.left,top:e.pageY-a.top}}function O(t,e,a){let i;return function(){let n=this,s=arguments,l=function(){i=null,a||t.apply(n,s)},r=a&&!i;clearTimeout(i),i=setTimeout(l,e),r&&t.apply(n,s)}}class V{constructor(t){this._core=t,this.pageToolsIcon=this.createIcon(),this._backdrop=null,this._page=null,this._mainImage=null,this._canvas=null,this._originalData=null,this.maxZoom=4,this.minZoom=1,this.zoom=1,this.rotate=0,this.mirrorHorizontal=1,this.mirrorVertical=1,this.boundEscapeListener=this.escapeListener.bind(this),this.currentImageURL=null}handleClick(t,e,a,i){if(document.body.style.overflow="hidden",this._backdrop=document.createElement("div"),this._backdrop.classList.add("manipulation-fullscreen"),this._sidebar=document.createElement("div"),this._sidebar.classList.add("manipulation-sidebar"),this._mainArea=document.createElement("div"),this._mainArea.classList.add("manipulation-main-area"),this._mainArea.classList.add("dragscroll"),this._mainArea.addEventListener("mousedown",()=>{this._mainArea.classList.add("grabbing")}),this._mainArea.addEventListener("mouseup",()=>{this._mainArea.classList.remove("grabbing")}),X.onDoubleClick(this._mainArea,this.handleDblClick.bind(this)),this._tools=document.createElement("div"),this._tools.classList.add("manipulation-tools"),this._backdrop.appendChild(this._sidebar),this._backdrop.appendChild(this._mainArea),this._backdrop.appendChild(this._tools),this._core.parentObject.appendChild(this._backdrop),document.addEventListener("keyup",this.boundEscapeListener),this._page=e.manifest.pages[i],this._canvas=document.createElement("canvas"),this._ctx=this._canvas.getContext("2d"),this._mainArea.appendChild(this._canvas),this._initializeSidebar(),this._initializeTools(),window.resetDragscroll(),this._loadImageInMainArea(t,this._page.url),e.inFullscreen&&(document.getElementById(e.selector+"tools").style.display="none"),window.innerWidth<=1e3){this._mainArea.classList.remove("manipulation-main-area"),this._mainArea.classList.add("manipulation-main-area-mobile"),this._sidebar.classList.remove("manipulation-sidebar"),this._sidebar.classList.add("manipulation-sidebar-mobile"),this._tools.classList.remove("manipulation-tools"),this._tools.classList.add("manipulation-tools-mobile");let t=document.createElement("div");t.classList.add("burger-menu");let e=document.createElement("div"),a=document.createElement("div"),i=document.createElement("div");e.classList.add("stripe"),a.classList.add("stripe"),i.classList.add("stripe"),t.appendChild(e),t.appendChild(a),t.appendChild(i),this.burgerClicked=!1,t.onclick=()=>{this.burgerClicked?(this._sidebar.style.display="none",this._tools.style.display="none",this._mainArea.style.display="block"):(this._sidebar.style.display="block",this._tools.style.display="block",this._mainArea.style.display="none"),this.burgerClicked=!this.burgerClicked},this._backdrop.appendChild(t)}}handleDblClick(t){let e=t.ctrlKey?this.zoom-1:this.zoom+1;e<this.minZoom||e>this.maxZoom||(document.getElementById("zoom-slider").value=e,this.handleZoom(t,e,!0))}createIcon(){const t=document.createElement("div");t.classList.add("diva-manipulation-icon");let e=document.createElementNS("http://www.w3.org/2000/svg","svg");e.setAttribute("x","0px"),e.setAttribute("y","0px"),e.setAttribute("viewBox","0 0 25 25"),e.id=this._core.settings.selector+"manipulation-icon";let a=document.createElementNS("http://www.w3.org/2000/svg","g");a.id=this._core.settings.selector+"manipulation-icon-glyph",a.setAttribute("transform","matrix(1, 0, 0, 1, -11.5, -11.5)"),a.setAttribute("class","diva-pagetool-icon");let i=document.createElementNS("http://www.w3.org/2000/svg","path");i.setAttribute("d","M27,21h-1v-9h-3v9h-1c-0.55,0-1,0.45-1,1v3c0,0.55,0.45,1,1,1h1h3h1c0.55,0,1-0.45,1-1v-3C28,21.45,27.55,21,27,21z M27,24h-5v-0.5h5V24z");let n=document.createElementNS("http://www.w3.org/2000/svg","path");n.setAttribute("d","M35,16h-1v-4h-3v4h-1c-0.55,0-1,0.45-1,1v3c0,0.55,0.45,1,1,1h1h3h1c0.55,0,1-0.45,1-1v-3C36,16.45,35.55,16,35,16z M35,19h-5v-0.5h5V19z");let s=document.createElementNS("http://www.w3.org/2000/svg","path");s.setAttribute("d","M19,26h-1V12h-3v14h-1c-0.55,0-1,0.45-1,1v3c0,0.55,0.45,1,1,1h1h3h1c0.55,0,1-0.45,1-1v-3C20,26.45,19.55,26,19,26zM19,29h-5v-0.5h5V29z");let l=document.createElementNS("http://www.w3.org/2000/svg","rect");l.setAttribute("x","23"),l.setAttribute("y","27"),l.setAttribute("width","3"),l.setAttribute("height","9");let r=document.createElementNS("http://www.w3.org/2000/svg","rect");r.setAttribute("x","31"),r.setAttribute("y","22"),r.setAttribute("width","3"),r.setAttribute("height","14");let o=document.createElementNS("http://www.w3.org/2000/svg","rect");return o.setAttribute("x","15"),o.setAttribute("y","32"),o.setAttribute("width","3"),o.setAttribute("height","4"),a.appendChild(i),a.appendChild(n),a.appendChild(l),a.appendChild(s),a.appendChild(r),a.appendChild(o),e.appendChild(a),t.appendChild(e),t}escapeListener(t){27===t.keyCode&&(document.removeEventListener("keyup",this.boundEscapeListener),document.body.style.overflow="auto",this._core.parentObject.removeChild(this._backdrop),document.getElementById(this._core.settings.selector+"tools").style.display="block")}_initializeSidebar(){let t=this._page.url+"full/150,/0/default.jpg",e=this._page.otherImages.map(t=>t.url+"full/150,/0/default.jpg"),a=document.createElement("div");a.classList.add("manipulation-sidebar-primary-image");let i=document.createElement("img");i.setAttribute("src",t);let n=document.createElement("div");n.textContent=this._page.il,a.appendChild(i),a.appendChild(n),this._sidebar.appendChild(a),a.addEventListener("click",()=>{this._loadImageInMainArea.call(this,event,this._page.url)}),e.map((t,e)=>{let a=document.createElement("div");a.classList.add("manipulation-sidebar-secondary-image");let i=document.createElement("img");i.setAttribute("src",t);let n=document.createElement("div");n.textContent=this._page.otherImages[e].il,a.appendChild(i),a.appendChild(n),this._sidebar.appendChild(a),a.addEventListener("click",()=>this._loadImageInMainArea.call(this,event,this._page.otherImages[e].url))})}_initializeTools(){let t=document.createElement("button");t.innerHTML="&#10006",t.classList.add("close-button"),t.setAttribute("style","display: absolute; top: 1em; right: 1em;"),t.onclick=()=>{document.body.style.overflow="auto",this._core.parentObject.removeChild(this._backdrop),document.getElementById(this._core.settings.selector+"tools").style.display="block"};let e=document.createElement("h2");e.setAttribute("style","margin-bottom: 0.3em;"),e.classList.add("manipulation-tools-text"),e.innerText="Image tools";let a=document.createElement("div"),i=document.createElement("input"),n=document.createElement("label");n.textContent="Zoom",n.setAttribute("for","zoom-slider"),a.classList.add("manipulation-tools-text"),i.setAttribute("type","range"),i.setAttribute("max",this.maxZoom),i.setAttribute("min",this.minZoom),i.setAttribute("value",this.zoom),i.id="zoom-slider",a.addEventListener("change",O(t=>this.handleZoom(t,t.target.value,!0),250)),a.appendChild(i),a.appendChild(n);let s=document.createElement("div"),l=document.createElement("input"),r=document.createElement("label");r.textContent="Rotation",r.setAttribute("for","rotate-slider"),s.classList.add("manipulation-tools-text"),l.id="rotate-slider",l.setAttribute("type","range"),l.setAttribute("max",359),l.setAttribute("min",0),l.setAttribute("value",0),s.addEventListener("input",t=>{this.handleTransform(t,null,t.target.value)}),s.appendChild(l),s.appendChild(r);let o=document.createElement("div"),c=document.createElement("button");c.id="vertical-mirror-button";let u=document.createElement("button");u.id="horizontal-mirror-button",c.textContent="Mirror Vertically",u.textContent="Mirror Horizontally",c.addEventListener("click",t=>this.handleTransform(t,"vertical",this.rotate)),u.addEventListener("click",t=>this.handleTransform(t,"horizontal",this.rotate)),o.appendChild(c),o.appendChild(u);let p=document.createElement("div");p.setAttribute("style","margin: 1em 0;");let b=document.createElement("h3");b.setAttribute("style","margin: 0;"),b.classList.add("manipulation-tools-text"),b.innerText="Filters",b.id="filters-title";let f=document.createElement("select");f.id="filter-select",f.style.backgroundColor="white",f.setAttribute("aria-labelledby","filters-title");let C=document.createElement("option");C.value="colours",C.innerText="Color Filters";let y=document.createElement("option");y.value="threshold",y.innerText="Threshold",f.addEventListener("change",(function(){let t=document.getElementsByClassName("color-filters");if("threshold"===this.value){for(let e=0,a=t.length;e<a;e++)t[e].style.display="none";ct.style.display="block"}else{for(let e=0,a=t.length;e<a;e++)t[e].style.display="block";ct.style.display="none"}})),f.appendChild(C),f.appendChild(y),p.appendChild(b),p.appendChild(f);let L=document.createElement("div");L.classList.add("color-filters");let w=document.createElement("button");w.textContent="Grayscale",w.addEventListener("click",t=>this._applyTransformationToImageData(t,d)),L.appendChild(w);let I=document.createElement("div");I.classList.add("color-filters"),I.classList.add("manipulation-tools-text");let k=document.createElement("input"),z=document.createElement("label");z.textContent="Saturation",z.setAttribute("for","saturation-slider"),k.setAttribute("type","range"),k.setAttribute("max",100),k.setAttribute("min",-100),k.setAttribute("value",0),k.id="saturation-slider",k.addEventListener("change",O(t=>this._applyTransformationToImageData(t,h,t.target.value),250)),I.appendChild(k),I.appendChild(z);let j=document.createElement("div");j.classList.add("color-filters"),j.classList.add("manipulation-tools-text");let X=document.createElement("input"),Y=document.createElement("label");Y.textContent="Vibrance",Y.setAttribute("for","vibrance-slider"),X.setAttribute("type","range"),X.setAttribute("max",100),X.setAttribute("min",-100),X.setAttribute("value",0),X.id="vibrance-slider",X.addEventListener("change",O(t=>this._applyTransformationToImageData(t,m,t.target.value),250)),j.appendChild(X),j.appendChild(Y);let B=document.createElement("div");B.classList.add("color-filters"),B.classList.add("manipulation-tools-text");let N=document.createElement("input"),V=document.createElement("label");V.setAttribute("for","brightness-slider"),V.textContent="Brightness",N.setAttribute("type","range"),N.setAttribute("max",100),N.setAttribute("min",-100),N.setAttribute("value",0),N.id="brightness-slider",N.addEventListener("change",O(t=>this._applyTransformationToImageData(t,g,t.target.value),250)),B.appendChild(N),B.appendChild(V);let R=document.createElement("div");R.classList.add("color-filters"),R.classList.add("manipulation-tools-text");let H=document.createElement("input"),Z=document.createElement("label");Z.textContent="Contrast",Z.setAttribute("for","contrast-slider"),H.setAttribute("type","range"),H.setAttribute("max",100),H.setAttribute("min",-100),H.setAttribute("value",0),H.id="contrast-slider",H.addEventListener("change",O(t=>this._applyTransformationToImageData(t,v,t.target.value),250)),R.appendChild(H),R.appendChild(Z);let P=document.createElement("div");P.classList.add("color-filters");let F=document.createElement("button");F.textContent="Invert Colours",F.addEventListener("click",t=>this._applyTransformationToImageData(t,_)),P.appendChild(F);let G=document.createElement("div");G.classList.add("color-filters"),G.classList.add("manipulation-tools-text");let U=document.createElement("input"),q=document.createElement("label");q.textContent="Sharpness",q.setAttribute("for","sharpness-slider"),U.setAttribute("type","range"),U.setAttribute("max",100),U.setAttribute("min",0),U.setAttribute("value",0),U.id="sharpness-slider",U.addEventListener("change",O(t=>this._applyTransformationToImageData(t,S,t.target.value),250)),G.appendChild(U),G.appendChild(q);let K=document.createElement("div");K.classList.add("color-filters"),K.classList.add("manipulation-tools-text");let W=document.createElement("input"),J=document.createElement("label");J.textContent="Hue",J.setAttribute("for","hue-slider"),W.setAttribute("type","range"),W.setAttribute("max",100),W.setAttribute("min",0),W.setAttribute("value",0),W.id="hue-slider",W.addEventListener("change",O(t=>this._applyTransformationToImageData(t,A,t.target.value),250)),K.appendChild(W),K.appendChild(J);let Q=document.createElement("div");Q.classList.add("color-filters"),Q.classList.add("manipulation-tools-text");let $=document.createElement("input"),tt=document.createElement("label");tt.textContent="Gamma",tt.setAttribute("for","gamma-slider"),$.setAttribute("type","range"),$.setAttribute("max",300),$.setAttribute("min",-100),$.setAttribute("value",0),$.id="gamma-slider",$.addEventListener("change",O(t=>this._applyTransformationToImageData(t,x,t.target.value),250)),Q.appendChild($),Q.appendChild(tt);let et=document.createElement("div");et.classList.add("color-filters"),et.classList.add("manipulation-tools-text");let at=document.createElement("input"),it=document.createElement("label");it.textContent="CC Red",it.setAttribute("for","cc-red-slider"),at.setAttribute("type","range"),at.setAttribute("max",100),at.setAttribute("min",-100),at.setAttribute("value",0),at.id="cc-red-slider";let nt=document.createElement("div");nt.classList.add("color-filters"),nt.classList.add("manipulation-tools-text");let st=document.createElement("input"),lt=document.createElement("label");lt.textContent="CC Green",lt.setAttribute("for","cc-green-slider"),st.setAttribute("type","range"),st.setAttribute("max",100),st.setAttribute("min",-100),st.setAttribute("value",0),st.id="cc-green-slider";let rt=document.createElement("div");rt.classList.add("color-filters"),rt.classList.add("manipulation-tools-text");let ot=document.createElement("input"),dt=document.createElement("label");dt.textContent="CC Blue",dt.setAttribute("for","cc-blue-slider"),ot.setAttribute("type","range"),ot.setAttribute("max",100),ot.setAttribute("min",-100),ot.setAttribute("value",0),ot.id="cc-blue-slider",at.addEventListener("change",O(t=>this._applyTransformationToImageData(t,T,t.target.value),250)),st.addEventListener("change",O(t=>this._applyTransformationToImageData(t,D,t.target.value),250)),ot.addEventListener("change",O(t=>this._applyTransformationToImageData(t,M,t.target.value),250)),et.appendChild(at),et.appendChild(it),nt.appendChild(st),nt.appendChild(lt),rt.appendChild(ot),rt.appendChild(dt);let ct=document.createElement("div");ct.style.display="none";let ht=document.createElement("input"),ut=document.createElement("label");ut.textContent="Threshold",ut.setAttribute("for","threshold-slider"),ct.classList.add("manipulation-tools-text"),ht.setAttribute("type","range"),ht.setAttribute("max",255),ht.setAttribute("min",64),ht.setAttribute("value",0),ht.id="threshold-slider",ht.addEventListener("change",O(t=>this._applyTransformationToImageData(t,E,t.target.value),250)),ct.appendChild(ht),ct.appendChild(ut);let mt=document.createElement("button");mt.setAttribute("style","margin-top: 1em;");let pt=document.createTextNode("Reset");mt.appendChild(pt),mt.onclick=t=>{this._loadImageInMainArea(t,this.currentImageURL)};let gt=document.createElement("div");gt.classList.add("manipulation-tools-text"),gt.innerHTML="<h3> Filter Application Order <h3>",gt.id="filter-log",this._tools.appendChild(t),this._tools.appendChild(e),this._tools.appendChild(a),this._tools.appendChild(s),this._tools.appendChild(o),this._tools.appendChild(p),this._tools.appendChild(L),this._tools.appendChild(P),this._tools.appendChild(I),this._tools.appendChild(j),this._tools.appendChild(B),this._tools.appendChild(R),this._tools.appendChild(G),this._tools.appendChild(K),this._tools.appendChild(Q),this._tools.appendChild(et),this._tools.appendChild(nt),this._tools.appendChild(rt),this._tools.appendChild(ct),this._tools.appendChild(mt),this._tools.appendChild(gt),this._tools.setAttribute("style","padding: 0 1em;")}_resetSliders(){for(let t=0,e=this._tools.children.length;t<e;t++){let e=this._tools.children[t].children[0];e&&"range"===e.type&&(e.value=0)}document.getElementById("filter-log").innerHTML="<h3> Filter Application Order <h3>",this.zoom=1,this.rotate=0,this.mirrorHorizontal=1,this.mirrorVertical=1,this.handleTransform(null,null,this.rotate),s()}_loadImageInMainArea(t,e){this.currentImageURL=e;let a=e+"full/full/0/default.jpg";this._mainImage=new Image,this._mainImage.crossOrigin="anonymous",this._mainImage.addEventListener("load",()=>{this._canvas.size=Math.sqrt(this._mainImage.width*this._mainImage.width+this._mainImage.height*this._mainImage.height),this._canvas.width=this._canvas.size,this._canvas.height=this._canvas.size,this._canvas.cornerX=(this._canvas.size-this._mainImage.width)/2,this._canvas.cornerY=(this._canvas.size-this._mainImage.height)/2,this._ctx.clearRect(0,0,this._canvas.width,this._canvas.height),this._ctx.drawImage(this._mainImage,this._canvas.cornerX,this._canvas.cornerY,this._mainImage.width,this._mainImage.height),this._originalData=this._ctx.getImageData(this._canvas.cornerX,this._canvas.cornerY,this._mainImage.width,this._mainImage.height),this._alteredData=this._originalData,this.dims={w:this._canvas.width,h:this._canvas.height},this._mainImage=null,this.centerView()}),this._mainImage.src=a,this._resetSliders()}_applyTransformationToImageData(t,e,a){let i,n=this._canvas.width,s=this._canvas.height;a&&(i=parseInt(a,10));let l=e(this._originalData,i);this._alteredData=l,this._ctx.clearRect(0,0,n,s),this._ctx.putImageData(l,this._canvas.cornerX,this._canvas.cornerY),this.handleZoom(t,this.zoom,!1)}handleZoom(t,e,a){let i=.5*e+.5,n=this.dims.w,s=this.dims.h,l=document.createElement("canvas"),r=l.getContext("2d");l.width=n,l.height=s,r.putImageData(this._alteredData,this._canvas.cornerX,this._canvas.cornerY),this._canvas.width=n*i,this._canvas.height=s*i,this._ctx.clearRect(0,0,this._canvas.width,this._canvas.height),this._ctx.scale(i,i),this._ctx.drawImage(l,0,0);let o=e>this.zoom;if(this.zoom=parseInt(e,10),a){let e=t.target.getBoundingClientRect(),a=t.clientX-e.left,i=t.clientY-e.top;if(!o){let t=(.5*this.zoom+.5)/(.5*(this.zoom+1)+.5);a*=t,i*=t}this.centerView(a,i,o)}}centerView(t,e,a){let i=document.getElementsByClassName("manipulation-main-area")[0];if(i||(i=document.getElementsByClassName("manipulation-main-area-mobile")[0]),a){let a=(.5*this.zoom+.5)/(.5*(this.zoom-1)+.5);t*=a,e*=a}let n=this._canvas.height/2,s=e-n,l=t-n,r=this._canvas.height,o=this._canvas.width,d=(r-i.clientHeight)/2,c=(o-i.clientWidth)/2,h=e?d+s:d,u=t?c+l:c;i.scrollTop=h,i.scrollLeft=u}handleTransform(t,e,a){let i=document.getElementsByClassName("manipulation-main-area")[0].children[0];"vertical"===e?this.mirrorVertical*=-1:"horizontal"===e&&(this.mirrorHorizontal*=-1),i.style.transform="scale("+this.mirrorHorizontal+","+this.mirrorVertical+") rotate("+a+"deg)",this.rotate=a}}V.prototype.pluginName="manipulation",V.prototype.isPageTool=!0,window.Diva.ManipulationPlugin=V}]);
//# sourceMappingURL=manipulation.js.map