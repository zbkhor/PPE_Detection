(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-7bb5062c"],{"0d71":function(e,t,i){},6062:function(e,t,i){"use strict";var n=i("6d61"),s=i("6566");e.exports=n("Set",(function(e){return function(){return e(this,arguments.length?arguments[0]:void 0)}}),s)},6711:function(e,t,i){},6889:function(e,t,i){"use strict";var n=i("6711"),s=i.n(n);s.a},"78c1":function(e,t,i){"use strict";i.r(t);var n=function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("v-row",[i("v-col",{attrs:{cols:"3"}},[i("testing")],1)],1)},s=[],a=function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("v-card",[i("v-sheet",{staticClass:"v-sheet--offset d-flex mx-auto",attrs:{elevation:"6","max-width":"calc(100% - 32px)",color:"navigation"}},[i("span",{staticClass:"pl-4 d-flex align-center white--text"},[e._v("Live Camera Feed")]),i("v-spacer"),i("v-card-actions",{staticClass:"pr-4 d-flex align-center"},[i("v-treeview",{staticClass:"videoSourceSelect mr-6",class:e.videoOn?"videoEnabled":"videoDisabled",attrs:{items:e.myVideoSources,"item-text":"deviceName","item-value":"deviceId",label:"Select Camera",dense:"",outlined:"",disabled:!e.videoOn},on:{change:e.changeMedia},model:{value:e.selectedVideoSource,callback:function(t){e.selectedVideoSource=t},expression:"selectedVideoSource"}})],1)],1),i("testing-2")],1)},r=[],c=(i("4160"),i("45fc"),i("b0c0"),i("d3b7"),i("96cf"),i("1da1")),o=function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("div",{attrs:{id:"camera"}},[i("video",{ref:"video",attrs:{id:"video",autoplay:""}})])},d=[],l={name:"Testing2",props:["video"],mounted:function(){this.video=this.$refs.video,this.$emit("toggleCamera")}},h=l,u=i("2877"),v=Object(u["a"])(h,o,d,!1,null,null,null),p=v.exports,f={name:"Testing",components:{Testing2:p},data:function(){return{video:null,track:null,stream:null,videoOn:!1,defaultConstraints:{video:{width:{ideal:4096},height:{ideal:2160},frameRate:{ideal:30}}},myVideoSources:[{deviceName:"Camera is disabled",deviceId:0}],selectedVideoSource:0}},methods:{getDevices:function(e){var t=this;console.log("getDevices: true");for(var i=[],n=[this.selectedVideoSource],s=0;s!==e.length;++s){var a=e[s],r={};r.deviceId=a.deviceId,"videoinput"===a.kind?(r.deviceName=a.label||"camera ".concat(i.length+1),i.push(r)):console.log("Some other kind of source/device: ",a),this.myVideoSources=i;var c=[i];c.forEach((function(e,s){if(e.some((function(e){return e.deviceId===n[s]})))switch(s){case 0:t.selectedVideoSource=n[s];break}else if(e.length>0)switch(s){case 0:t.selectedVideoSource=i[0].deviceId;break}}))}},toggleCamera:function(){var e=this;return Object(c["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:if(e.videoOn=!e.videoOn,!e.videoOn){t.next=7;break}return t.next=4,navigator.mediaDevices.enumerateDevices().then((function(t){e.getDevices(t)})).catch(e.handleError);case 4:e.getMedia(e.defaultConstraints),t.next=11;break;case 7:e.stream.getVideoTracks()[0].stop(),e.video.srcObject=null,e.myVideoSources=[{deviceName:"Camera is disabled",deviceId:0}],e.selectedVideoSource=0;case 11:case"end":return t.stop()}}),t)})))()},getMedia:function(e){var t=this;console.log("getMedia: true"),null!=this.stream&&(this.stream.getVideoTracks()[0].stop(),this.video.srcObject=null);var i=this.selectedVideoSource;console.log(JSON.stringify(i)),e.video.deviceId=i?{exact:i}:void 0,navigator.mediaDevices.getUserMedia(e).then(this.gotStream).then((function(e){t.getDevices(e)})).then(this.resolveVideo).catch(this.handleError)},gotStream:function(e){return console.log("gotStream: true"),this.stream=window.stream=e,this.video.srcObject=e,this.track=e.getVideoTracks()[0],navigator.mediaDevices.enumerateDevices()},resolveVideo:function(){var e=this;return console.log("resolveVideo: true"),new Promise((function(t){return e.video.onplaying=t}))},handleError:function(e){console.log("navigator.MediaDevices.getUserMedia error: ",e.message,e.name)},changeMedia:function(){this.getMedia(this.defaultConstraints)}}},m=f,g=(i("b859"),i("6889"),i("6544")),b=i.n(g),O=i("b0af"),C=i("99d9"),S=i("8dd9"),y=i("2fa4"),w=(i("4de4"),i("d81d"),i("13d5"),i("4ec9"),i("b64b"),i("ac1f"),i("6062"),i("3ca3"),i("841c"),i("159b"),i("ddb0"),i("3835")),j=i("b85c"),I=i("2909"),x=i("5530"),k=(i("fa9e"),i("caad"),i("a9e3"),i("ade3")),A=i("0789"),V=i("132d"),$=i("3206"),T=i("a9ad"),E=i("58df"),_=i("80d2"),q=Object(E["a"])(T["a"],Object($["a"])("treeview")),D={activatable:Boolean,activeClass:{type:String,default:"v-treeview-node--active"},color:{type:String,default:"primary"},expandIcon:{type:String,default:"$subgroup"},indeterminateIcon:{type:String,default:"$checkboxIndeterminate"},itemChildren:{type:String,default:"children"},itemDisabled:{type:String,default:"disabled"},itemKey:{type:String,default:"id"},itemText:{type:String,default:"name"},loadChildren:Function,loadingIcon:{type:String,default:"$loading"},offIcon:{type:String,default:"$checkboxOff"},onIcon:{type:String,default:"$checkboxOn"},openOnClick:Boolean,rounded:Boolean,selectable:Boolean,selectedColor:{type:String,default:"accent"},shaped:Boolean,transition:Boolean,selectionType:{type:String,default:"leaf",validator:function(e){return["leaf","independent"].includes(e)}}},K=q.extend().extend({name:"v-treeview-node",inject:{treeview:{default:null}},props:Object(x["a"])({level:Number,item:{type:Object,default:function(){return null}},parentIsDisabled:Boolean},D),data:function(){return{hasLoaded:!1,isActive:!1,isIndeterminate:!1,isLoading:!1,isOpen:!1,isSelected:!1}},computed:{disabled:function(){return Object(_["q"])(this.item,this.itemDisabled)||this.parentIsDisabled&&"leaf"===this.selectionType},key:function(){return Object(_["q"])(this.item,this.itemKey)},children:function(){var e=this,t=Object(_["q"])(this.item,this.itemChildren);return t&&t.filter((function(t){return!e.treeview.isExcluded(Object(_["q"])(t,e.itemKey))}))},text:function(){return Object(_["q"])(this.item,this.itemText)},scopedProps:function(){return{item:this.item,leaf:!this.children,selected:this.isSelected,indeterminate:this.isIndeterminate,active:this.isActive,open:this.isOpen}},computedIcon:function(){return this.isIndeterminate?this.indeterminateIcon:this.isSelected?this.onIcon:this.offIcon},hasChildren:function(){return!!this.children&&(!!this.children.length||!!this.loadChildren)}},created:function(){this.treeview.register(this)},beforeDestroy:function(){this.treeview.unregister(this)},methods:{checkChildren:function(){var e=this;return new Promise((function(t){if(!e.children||e.children.length||!e.loadChildren||e.hasLoaded)return t();e.isLoading=!0,t(e.loadChildren(e.item))})).then((function(){e.isLoading=!1,e.hasLoaded=!0}))},open:function(){this.isOpen=!this.isOpen,this.treeview.updateOpen(this.key,this.isOpen),this.treeview.emitOpen()},genLabel:function(){var e=[];return this.$scopedSlots.label?e.push(this.$scopedSlots.label(this.scopedProps)):e.push(this.text),this.$createElement("div",{slot:"label",staticClass:"v-treeview-node__label"},e)},genPrependSlot:function(){return this.$scopedSlots.prepend?this.$createElement("div",{staticClass:"v-treeview-node__prepend"},this.$scopedSlots.prepend(this.scopedProps)):null},genAppendSlot:function(){return this.$scopedSlots.append?this.$createElement("div",{staticClass:"v-treeview-node__append"},this.$scopedSlots.append(this.scopedProps)):null},genContent:function(){var e=[this.genPrependSlot(),this.genLabel(),this.genAppendSlot()];return this.$createElement("div",{staticClass:"v-treeview-node__content"},e)},genToggle:function(){var e=this;return this.$createElement(V["a"],{staticClass:"v-treeview-node__toggle",class:{"v-treeview-node__toggle--open":this.isOpen,"v-treeview-node__toggle--loading":this.isLoading},slot:"prepend",on:{click:function(t){t.stopPropagation(),e.isLoading||e.checkChildren().then((function(){return e.open()}))}}},[this.isLoading?this.loadingIcon:this.expandIcon])},genCheckbox:function(){var e=this;return this.$createElement(V["a"],{staticClass:"v-treeview-node__checkbox",props:{color:this.isSelected||this.isIndeterminate?this.selectedColor:void 0,disabled:this.disabled},on:{click:function(t){t.stopPropagation(),e.isLoading||e.checkChildren().then((function(){e.$nextTick((function(){e.isSelected=!e.isSelected,e.isIndeterminate=!1,e.treeview.updateSelected(e.key,e.isSelected),e.treeview.emitSelected()}))}))}}},[this.computedIcon])},genLevel:function(e){var t=this;return Object(_["i"])(e).map((function(){return t.$createElement("div",{staticClass:"v-treeview-node__level"})}))},genNode:function(){var e=this,t=[this.genContent()];return this.selectable&&t.unshift(this.genCheckbox()),this.hasChildren?t.unshift(this.genToggle()):t.unshift.apply(t,Object(I["a"])(this.genLevel(1))),t.unshift.apply(t,Object(I["a"])(this.genLevel(this.level))),this.$createElement("div",this.setTextColor(this.isActive&&this.color,{staticClass:"v-treeview-node__root",class:Object(k["a"])({},this.activeClass,this.isActive),on:{click:function(){e.openOnClick&&e.hasChildren?e.checkChildren().then(e.open):e.activatable&&!e.disabled&&(e.isActive=!e.isActive,e.treeview.updateActive(e.key,e.isActive),e.treeview.emitActive())}}}),t)},genChild:function(e,t){return this.$createElement(K,{key:Object(_["q"])(e,this.itemKey),props:{activatable:this.activatable,activeClass:this.activeClass,item:e,selectable:this.selectable,selectedColor:this.selectedColor,color:this.color,expandIcon:this.expandIcon,indeterminateIcon:this.indeterminateIcon,offIcon:this.offIcon,onIcon:this.onIcon,loadingIcon:this.loadingIcon,itemKey:this.itemKey,itemText:this.itemText,itemDisabled:this.itemDisabled,itemChildren:this.itemChildren,loadChildren:this.loadChildren,transition:this.transition,openOnClick:this.openOnClick,rounded:this.rounded,shaped:this.shaped,level:this.level+1,selectionType:this.selectionType,parentIsDisabled:t},scopedSlots:this.$scopedSlots})},genChildrenWrapper:function(){var e=this;if(!this.isOpen||!this.children)return null;var t=[this.children.map((function(t){return e.genChild(t,e.disabled)}))];return this.$createElement("div",{staticClass:"v-treeview-node__children"},t)},genTransition:function(){return this.$createElement(A["a"],[this.genChildrenWrapper()])}},render:function(e){var t=[this.genNode()];return this.transition?t.push(this.genTransition()):t.push(this.genChildrenWrapper()),e("div",{staticClass:"v-treeview-node",class:{"v-treeview-node--leaf":!this.hasChildren,"v-treeview-node--click":this.openOnClick,"v-treeview-node--disabled":this.disabled,"v-treeview-node--rounded":this.rounded,"v-treeview-node--shaped":this.shaped,"v-treeview-node--selected":this.isSelected},attrs:{"aria-expanded":String(this.isOpen)}},t)}}),L=K,P=i("7560"),N=i("d9bd");i("c975");function B(e,t,i){var n=Object(_["q"])(e,i);return n.toLocaleLowerCase().indexOf(t.toLocaleLowerCase())>-1}function M(e,t,i,n,s,a,r){if(e(t,i,s))return!0;var c=Object(_["q"])(t,a);if(c){for(var o=!1,d=0;d<c.length;d++)M(e,c[d],i,n,s,a,r)&&(o=!0);if(o)return!0}return r.add(Object(_["q"])(t,n)),!1}var W=Object(E["a"])(Object($["b"])("treeview"),P["a"]).extend({name:"v-treeview",provide:function(){return{treeview:this}},props:Object(x["a"])({active:{type:Array,default:function(){return[]}},dense:Boolean,filter:Function,hoverable:Boolean,items:{type:Array,default:function(){return[]}},multipleActive:Boolean,open:{type:Array,default:function(){return[]}},openAll:Boolean,returnObject:{type:Boolean,default:!1},search:String,value:{type:Array,default:function(){return[]}}},D),data:function(){return{level:-1,activeCache:new Set,nodes:{},openCache:new Set,selectedCache:new Set}},computed:{excludedItems:function(){var e=new Set;if(!this.search)return e;for(var t=0;t<this.items.length;t++)M(this.filter||B,this.items[t],this.search,this.itemKey,this.itemText,this.itemChildren,e);return e}},watch:{items:{handler:function(){var e=this,t=Object.keys(this.nodes).map((function(t){return Object(_["q"])(e.nodes[t].item,e.itemKey)})),i=this.getKeys(this.items),n=Object(_["c"])(i,t);if(n.length||!(i.length<t.length)){n.forEach((function(t){return delete e.nodes[t]}));var s=Object(I["a"])(this.selectedCache);this.selectedCache=new Set,this.activeCache=new Set,this.openCache=new Set,this.buildTree(this.items),Object(_["k"])(s,Object(I["a"])(this.selectedCache))||this.emitSelected()}},deep:!0},active:function(e){this.handleNodeCacheWatcher(e,this.activeCache,this.updateActive,this.emitActive)},value:function(e){this.handleNodeCacheWatcher(e,this.selectedCache,this.updateSelected,this.emitSelected)},open:function(e){this.handleNodeCacheWatcher(e,this.openCache,this.updateOpen,this.emitOpen)}},created:function(){var e=this,t=function(t){return e.returnObject?Object(_["q"])(t,e.itemKey):t};this.buildTree(this.items);var i,n=Object(j["a"])(this.value.map(t));try{for(n.s();!(i=n.n()).done;){var s=i.value;this.updateSelected(s,!0,!0)}}catch(o){n.e(o)}finally{n.f()}var a,r=Object(j["a"])(this.active.map(t));try{for(r.s();!(a=r.n()).done;){var c=a.value;this.updateActive(c,!0)}}catch(o){r.e(o)}finally{r.f()}},mounted:function(){var e=this;(this.$slots.prepend||this.$slots.append)&&Object(N["c"])("The prepend and append slots require a slot-scope attribute",this),this.openAll?this.updateAll(!0):(this.open.forEach((function(t){return e.updateOpen(e.returnObject?Object(_["q"])(t,e.itemKey):t,!0)})),this.emitOpen())},methods:{updateAll:function(e){var t=this;Object.keys(this.nodes).forEach((function(i){return t.updateOpen(Object(_["q"])(t.nodes[i].item,t.itemKey),e)})),this.emitOpen()},getKeys:function(e){for(var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:[],i=0;i<e.length;i++){var n=Object(_["q"])(e[i],this.itemKey);t.push(n);var s=Object(_["q"])(e[i],this.itemChildren);s&&t.push.apply(t,Object(I["a"])(this.getKeys(s)))}return t},buildTree:function(e){for(var t=this,i=arguments.length>1&&void 0!==arguments[1]?arguments[1]:null,n=0;n<e.length;n++){var s=e[n],a=Object(_["q"])(s,this.itemKey),r=Object(_["q"])(s,this.itemChildren,[]),c=this.nodes.hasOwnProperty(a)?this.nodes[a]:{isSelected:!1,isIndeterminate:!1,isActive:!1,isOpen:!1,vnode:null},o={vnode:c.vnode,parent:i,children:r.map((function(e){return Object(_["q"])(e,t.itemKey)})),item:s};if(this.buildTree(r,a),!this.nodes.hasOwnProperty(a)&&null!==i&&this.nodes.hasOwnProperty(i)?o.isSelected=this.nodes[i].isSelected:(o.isSelected=c.isSelected,o.isIndeterminate=c.isIndeterminate),o.isActive=c.isActive,o.isOpen=c.isOpen,this.nodes[a]=o,r.length){var d=this.calculateState(a,this.nodes),l=d.isSelected,h=d.isIndeterminate;o.isSelected=l,o.isIndeterminate=h}!this.nodes[a].isSelected||"independent"!==this.selectionType&&0!==o.children.length||this.selectedCache.add(a),this.nodes[a].isActive&&this.activeCache.add(a),this.nodes[a].isOpen&&this.openCache.add(a),this.updateVnodeState(a)}},calculateState:function(e,t){var i=t[e].children,n=i.reduce((function(e,i){return e[0]+=+Boolean(t[i].isSelected),e[1]+=+Boolean(t[i].isIndeterminate),e}),[0,0]),s=!!i.length&&n[0]===i.length,a=!s&&(n[0]>0||n[1]>0);return{isSelected:s,isIndeterminate:a}},emitOpen:function(){this.emitNodeCache("update:open",this.openCache)},emitSelected:function(){this.emitNodeCache("input",this.selectedCache)},emitActive:function(){this.emitNodeCache("update:active",this.activeCache)},emitNodeCache:function(e,t){var i=this;this.$emit(e,this.returnObject?Object(I["a"])(t).map((function(e){return i.nodes[e].item})):Object(I["a"])(t))},handleNodeCacheWatcher:function(e,t,i,n){var s=this;e=this.returnObject?e.map((function(e){return Object(_["q"])(e,s.itemKey)})):e;var a=Object(I["a"])(t);Object(_["k"])(a,e)||(a.forEach((function(e){return i(e,!1)})),e.forEach((function(e){return i(e,!0)})),n())},getDescendants:function(e){var t,i=arguments.length>1&&void 0!==arguments[1]?arguments[1]:[],n=this.nodes[e].children;(t=i).push.apply(t,Object(I["a"])(n));for(var s=0;s<n.length;s++)i=this.getDescendants(n[s],i);return i},getParents:function(e){var t=this.nodes[e].parent,i=[];while(null!==t)i.push(t),t=this.nodes[t].parent;return i},register:function(e){var t=Object(_["q"])(e.item,this.itemKey);this.nodes[t].vnode=e,this.updateVnodeState(t)},unregister:function(e){var t=Object(_["q"])(e.item,this.itemKey);this.nodes[t]&&(this.nodes[t].vnode=null)},isParent:function(e){return this.nodes[e].children&&this.nodes[e].children.length},updateActive:function(e,t){var i=this;if(this.nodes.hasOwnProperty(e)){this.multipleActive||this.activeCache.forEach((function(e){i.nodes[e].isActive=!1,i.updateVnodeState(e),i.activeCache.delete(e)}));var n=this.nodes[e];n&&(t?this.activeCache.add(e):this.activeCache.delete(e),n.isActive=t,this.updateVnodeState(e))}},updateSelected:function(e,t){var i=arguments.length>2&&void 0!==arguments[2]&&arguments[2];if(this.nodes.hasOwnProperty(e)){var n=new Map;if("independent"!==this.selectionType){var s,a=Object(j["a"])(this.getDescendants(e));try{for(a.s();!(s=a.n()).done;){var r=s.value;Object(_["q"])(this.nodes[r].item,this.itemDisabled)&&!i||(this.nodes[r].isSelected=t,this.nodes[r].isIndeterminate=!1,n.set(r,t))}}catch(g){a.e(g)}finally{a.f()}var c=this.calculateState(e,this.nodes);this.nodes[e].isSelected=t,this.nodes[e].isIndeterminate=c.isIndeterminate,n.set(e,t);var o,d=Object(j["a"])(this.getParents(e));try{for(d.s();!(o=d.n()).done;){var l=o.value,h=this.calculateState(l,this.nodes);this.nodes[l].isSelected=h.isSelected,this.nodes[l].isIndeterminate=h.isIndeterminate,n.set(l,h.isSelected)}}catch(g){d.e(g)}finally{d.f()}}else this.nodes[e].isSelected=t,this.nodes[e].isIndeterminate=!1,n.set(e,t);var u,v=Object(j["a"])(n.entries());try{for(v.s();!(u=v.n()).done;){var p=Object(w["a"])(u.value,2),f=p[0],m=p[1];this.updateVnodeState(f),"leaf"===this.selectionType&&this.isParent(f)||(!0===m?this.selectedCache.add(f):this.selectedCache.delete(f))}}catch(g){v.e(g)}finally{v.f()}}},updateOpen:function(e,t){var i=this;if(this.nodes.hasOwnProperty(e)){var n=this.nodes[e],s=Object(_["q"])(n.item,this.itemChildren);s&&!s.length&&n.vnode&&!n.vnode.hasLoaded?n.vnode.checkChildren().then((function(){return i.updateOpen(e,t)})):s&&s.length&&(n.isOpen=t,n.isOpen?this.openCache.add(e):this.openCache.delete(e),this.updateVnodeState(e))}},updateVnodeState:function(e){var t=this.nodes[e];t&&t.vnode&&(t.vnode.isSelected=t.isSelected,t.vnode.isIndeterminate=t.isIndeterminate,t.vnode.isActive=t.isActive,t.vnode.isOpen=t.isOpen)},isExcluded:function(e){return!!this.search&&this.excludedItems.has(e)}},render:function(e){var t=this,i=this.items.length?this.items.filter((function(e){return!t.isExcluded(Object(_["q"])(e,t.itemKey))})).map((function(e){var i=L.options.methods.genChild.bind(t);return i(e,Object(_["q"])(e,t.itemDisabled))})):this.$slots.default;return e("div",{staticClass:"v-treeview",class:Object(x["a"])({"v-treeview--hoverable":this.hoverable,"v-treeview--dense":this.dense},this.themeClasses)},i)}}),R=Object(u["a"])(m,a,r,!1,null,"134ad64e",null),F=R.exports;b()(R,{VCard:O["a"],VCardActions:C["a"],VSheet:S["a"],VSpacer:y["a"],VTreeview:W});var J={name:"Test",components:{Testing:F}},U=J,z=i("62ad"),G=i("0fd9"),H=Object(u["a"])(U,n,s,!1,null,null,null);t["default"]=H.exports;b()(H,{VCol:z["a"],VRow:G["a"]})},"841c":function(e,t,i){"use strict";var n=i("d784"),s=i("825a"),a=i("1d80"),r=i("129f"),c=i("14c3");n("search",1,(function(e,t,i){return[function(t){var i=a(this),n=void 0==t?void 0:t[e];return void 0!==n?n.call(t,i):new RegExp(t)[e](String(i))},function(e){var n=i(t,e,this);if(n.done)return n.value;var a=s(e),o=String(this),d=a.lastIndex;r(d,0)||(a.lastIndex=0);var l=c(a,o);return r(a.lastIndex,d)||(a.lastIndex=d),null===l?-1:l.index}]}))},b859:function(e,t,i){"use strict";var n=i("0d71"),s=i.n(n);s.a},fa9e:function(e,t,i){}}]);
//# sourceMappingURL=chunk-7bb5062c.1a35b82e.js.map