(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-0183e12a"],{"0d71":function(e,t,i){},"2ebf":function(e,t,i){"use strict";var a=i("b92f"),n=i.n(a);n.a},"472a":function(e,t,i){},"5eb9":function(e,t,i){"use strict";var a=i("472a"),n=i.n(a);n.a},"78c1":function(e,t,i){"use strict";i.r(t);var a=function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("v-row",[i("v-col",{attrs:{cols:"3"}},[i("testing")],1)],1)},n=[],o=function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("v-card",[i("v-sheet",{staticClass:"v-sheet--offset d-flex mx-auto",attrs:{elevation:"6","max-width":"calc(100% - 32px)",color:"navigation"}},[i("span",{staticClass:"pl-4 d-flex align-center white--text"},[e._v("Live Camera Feed")]),i("v-spacer"),i("v-card-actions",{staticClass:"pr-4 d-flex align-center"},[i("v-select",{staticClass:"videoSourceSelect mr-6",class:e.videoOn?"videoEnabled":"videoDisabled",attrs:{items:e.myVideoSources,"item-text":"deviceName","item-value":"deviceId",label:"Select Camera",dense:"",outlined:"",disabled:!e.videoOn},on:{change:e.changeMedia},model:{value:e.selectedVideoSource,callback:function(t){e.selectedVideoSource=t},expression:"selectedVideoSource"}})],1)],1),i("testing-2")],1)},s=[],c=(i("4160"),i("45fc"),i("b0c0"),i("d3b7"),i("96cf"),i("1da1")),r=function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("div",{attrs:{id:"camera"}},[i("video",{ref:"video",attrs:{id:"video",autoplay:""}})])},d=[],l={name:"Testing2",props:["video","stream","videoOn","track","defaultConstraints","myVideoSources","selectedVideoSource"],mounted:function(){this.$emit("toggleCamera")}},u=l,v=(i("2ebf"),i("2877")),f=Object(v["a"])(u,r,d,!1,null,"4301ff99",null),m=f.exports,h={name:"Testing",components:{Testing2:m},data:function(){return{video:null,track:null,stream:null,videoOn:!1,defaultConstraints:{video:{width:{ideal:4096},height:{ideal:2160},frameRate:{ideal:30}}},myVideoSources:[{deviceName:"Camera is disabled",deviceId:0}],selectedVideoSource:0}},mounted:function(){this.video=this.$refs.video,this.toggleCamera()},methods:{getDevices:function(e){var t=this;console.log("getDevices: true");for(var i=[],a=[this.selectedVideoSource],n=0;n!==e.length;++n){var o=e[n],s={};s.deviceId=o.deviceId,"videoinput"===o.kind?(s.deviceName=o.label||"camera ".concat(i.length+1),i.push(s)):console.log("Some other kind of source/device: ",o),this.myVideoSources=i;var c=[i];c.forEach((function(e,n){if(e.some((function(e){return e.deviceId===a[n]})))switch(n){case 0:t.selectedVideoSource=a[n];break}else if(e.length>0)switch(n){case 0:t.selectedVideoSource=i[0].deviceId;break}}))}},toggleCamera:function(){var e=this;return Object(c["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:if(e.videoOn=!e.videoOn,!e.videoOn){t.next=7;break}return t.next=4,navigator.mediaDevices.enumerateDevices().then((function(t){e.getDevices(t)})).catch(e.handleError);case 4:e.getMedia(e.defaultConstraints),t.next=11;break;case 7:e.stream.getVideoTracks()[0].stop(),e.video.srcObject=null,e.myVideoSources=[{deviceName:"Camera is disabled",deviceId:0}],e.selectedVideoSource=0;case 11:case"end":return t.stop()}}),t)})))()},getMedia:function(e){var t=this;console.log("getMedia: true"),null!=this.stream&&(this.stream.getVideoTracks()[0].stop(),this.video.srcObject=null);var i=this.selectedVideoSource;console.log(JSON.stringify(i)),e.video.deviceId=i?{exact:i}:void 0,navigator.mediaDevices.getUserMedia(e).then(this.gotStream).then((function(e){t.getDevices(e)})).then(this.resolveVideo).catch(this.handleError)},gotStream:function(e){return console.log("gotStream: true"),this.stream=window.stream=e,this.video.srcObject=e,this.track=e.getVideoTracks()[0],navigator.mediaDevices.enumerateDevices()},resolveVideo:function(){var e=this;return console.log("resolveVideo: true"),new Promise((function(t){return e.video.onplaying=t}))},handleError:function(e){console.log("navigator.MediaDevices.getUserMedia error: ",e.message,e.name)},changeMedia:function(){this.getMedia(this.defaultConstraints)}}},g=h,b=(i("b859"),i("5eb9"),i("6544")),p=i.n(b),V=i("b0af"),S=i("99d9"),w=i("b974"),C=i("8dd9"),k=i("2fa4"),x=Object(v["a"])(g,o,s,!1,null,"5d29e226",null),O=x.exports;p()(x,{VCard:V["a"],VCardActions:S["a"],VSelect:w["a"],VSheet:C["a"],VSpacer:k["a"]});var D={name:"Test",components:{Testing:O}},M=D,y=i("62ad"),E=i("0fd9"),I=Object(v["a"])(M,a,n,!1,null,null,null);t["default"]=I.exports;p()(I,{VCol:y["a"],VRow:E["a"]})},b859:function(e,t,i){"use strict";var a=i("0d71"),n=i.n(a);n.a},b92f:function(e,t,i){}}]);
//# sourceMappingURL=chunk-0183e12a.efdc0457.js.map