  (function() {
    if (window.Event && !Event.prototype.preventDefault) {
      Event.prototype.preventDefault=function() {
        this.returnValue=false;
      };
    }
    if (window.Event && !Event.prototype.stopPropagation) {
      Event.prototype.stopPropagation=function() {
        this.cancelBubble=true;
      };
    }
    if (window.Element && !Element.prototype.addEventListener) {
      var eventListeners=[];
      
      var addEventListener=function(type,listener /*, useCapture (will be ignored) */) {
        var self=this;
        var wrapper=function(e) {
          e.target=e.srcElement;
          e.currentTarget=self;
          if (listener.handleEvent) {
            listener.handleEvent(e);
          } else {
            listener.call(self,e);
          }
        };
        if (type=="DOMContentLoaded") {
          var wrapper2=function(e) {
            if (document.readyState=="complete") {
              wrapper(e);
            }
          };
          document.attachEvent("onreadystatechange",wrapper2);
          eventListeners.push({object:this,type:type,listener:listener,wrapper:wrapper2});
          
          if (document.readyState=="complete") {
            var e=new Event();
            e.srcElement=window;
            wrapper2(e);
          }
        } else {
          this.attachEvent("on"+type,wrapper);
          eventListeners.push({object:this,type:type,listener:listener,wrapper:wrapper});
        }
      };
      var removeEventListener=function(type,listener /*, useCapture (will be ignored) */) {
        var counter=0;
        while (counter<eventListeners.length) {
          var eventListener=eventListeners[counter];
          if (eventListener.object==this && eventListener.type==type && eventListener.listener==listener) {
            if (type=="DOMContentLoaded") {
              this.detachEvent("onreadystatechange",eventListener.wrapper);
            } else {
              this.detachEvent("on"+type,eventListener.wrapper);
            }
            break;
          }
          ++counter;
        }
      };
      Element.prototype.addEventListener=addEventListener;
      Element.prototype.removeEventListener=removeEventListener;
      if (HTMLDocument) {
        HTMLDocument.prototype.addEventListener=addEventListener;
        HTMLDocument.prototype.removeEventListener=removeEventListener;
      }
      if (Window) {
        Window.prototype.addEventListener=addEventListener;
        Window.prototype.removeEventListener=removeEventListener;
      }
    }

    window.onload=function(){
      var ver = getInternetExplorerVersion();

      if ( ver > -1 ) {
        if ( ver < 9.0 ) {
            e("images/");
        }
      }
    };
  })();
  var msg1 = "รู้ไหม? Internet Explorer ของคุณล้าสมัยแล้ว";
  var msg2 = "เพื่อประสบการณ์ที่ดีที่สุด ในการใช้งานเว็บไซต์ของเรา เราขอแนะนำให้คุณปรับมันเป็นรุ่นใหม่ หรือเปลี่ยนไปใช้เบราว์เซอร์ตัวอื่น ด้านล่างคือเว็บเบราว์เซอร์จำนวนหนึ่งที่ได้รับความนิยมมากที่สุด";
  var msg3 = "คลิกที่ไอคอนเพื่อไปยังหน้าดาวน์โหลด";
  var msg1_en = "Did you know that your Internet Explorer is out of date?";
  var msg2_en = "To get the best possible experience using our website we recommend that you upgrade to a newer version or other web browser. A list of the most popular web browsers can be found below.";
  var msg3_en = "Just click on the icons to get to the download page";
  var br1 = "Internet Explorer 9+";
  var br2 = "Firefox 20+";
  var br3 = "Chrome 26+";
  // var br4 = "Opera 9.5+";
  // var br5 = "Chrome 2.0+";
  var url1 = "http://www.microsoft.com/windows/Internet-explorer/default.aspx";
  var url2 = "http://www.mozilla.com/firefox/";
  var url3 = "https://support.google.com/chrome/answer/95346?hl=en";
  // var url4 = "http://www.opera.com/download/";
  // var url5 = "http://www.google.com/chrome";
  var imgPath;

  function e(str) {
  imgPath = str;
  var _body = document.getElementsByTagName('body')[0];
  var _d = document.createElement('div');
  var _l = document.createElement('div');
  var _h = document.createElement('h1');
  var _p1 = document.createElement('p');
  var _p2 = document.createElement('p');

  var _h_en = document.createElement('h1');
  var _p1_en = document.createElement('p');
  var _p2_en = document.createElement('p');

  var _ul = document.createElement('ul');
  var _li1 = document.createElement('li');
  var _li2 = document.createElement('li');
  var _li3 = document.createElement('li');
  // var _li4 = document.createElement('li');
  // var _li5 = document.createElement('li');
  var _ico1 = document.createElement('div');
  var _ico2 = document.createElement('div');
  var _ico3 = document.createElement('div');
  var _ico4 = document.createElement('div');
  var _ico5 = document.createElement('div');
  var _lit1 = document.createElement('div');
  var _lit2 = document.createElement('div');
  var _lit3 = document.createElement('div');
  // var _lit4 = document.createElement('div');
  // var _lit5 = document.createElement('div');

  _body.appendChild(_l);
  _body.appendChild(_d);
  _d.appendChild(_h);
  _d.appendChild(_p1);
  _d.appendChild(_p2);

  _d.appendChild(_h_en);
  _d.appendChild(_p1_en);
  _d.appendChild(_p2_en);

  _d.appendChild(_ul);
  _ul.appendChild(_li1);
  _ul.appendChild(_li2);
  _ul.appendChild(_li3);
  // _ul.appendChild(_li4);
  // _ul.appendChild(_li5);
  _li1.appendChild(_ico1);
  _li2.appendChild(_ico2);
  _li3.appendChild(_ico3);
  // _li4.appendChild(_ico4);
  // _li5.appendChild(_ico5);
  _li1.appendChild(_lit1);
  _li2.appendChild(_lit2);
  _li3.appendChild(_lit3);
  // _li4.appendChild(_lit4);
  // _li5.appendChild(_lit5);

  _d.setAttribute('id','_d');
  _l.setAttribute('id','_l');
  _h.setAttribute('id','_h');
  _p1.setAttribute('id','_p1');
  _p2.setAttribute('id','_p2');

  _h_en.setAttribute('id','_h_en');
  _p1_en.setAttribute('id','_p1_en');
  _p2_en.setAttribute('id','_p2_en');

  _ul.setAttribute('id','_ul');
  _li1.setAttribute('id','_li1');
  _li2.setAttribute('id','_li2');
  _li3.setAttribute('id','_li3');
  // _li4.setAttribute('id','_li4');
  // _li5.setAttribute('id','_li5');
  _ico1.setAttribute('id','_ico1');
  _ico2.setAttribute('id','_ico2');
  _ico3.setAttribute('id','_ico3');
  // _ico4.setAttribute('id','_ico4');
  // _ico5.setAttribute('id','_ico5');
  _lit1.setAttribute('id','_lit1');
  _lit2.setAttribute('id','_lit2');
  _lit3.setAttribute('id','_lit3');
  // _lit4.setAttribute('id','_lit4');
  // _lit5.setAttribute('id','_lit5');

  var _width = document.documentElement.clientWidth;
  var _height = document.documentElement.clientHeight;

  var _dl = document.getElementById('_l');
  _dl.style.width =  "100%";
  _dl.style.height = "100%";
  _dl.style.minHeight = "900px";
  _dl.style.position = "absolute";
  _dl.style.top = "0px";
  _dl.style.left = "0px";
  _dl.style.filter = "progid:DXImageTransform.Microsoft.Alpha(Opacity=80)";
  _dl.style.backgroundColor = "#000";
  _dl.style.opacity = "0.9";
  _dl.style.zIndex = 1;

  var _dd = document.getElementById('_d');
  _ddw = 650;
  _ddh = 400;
  _dd.style.zIndex = 9999;
  _dd.style.width = _ddw+"px";
  _dd.style.height = _ddh+"px";
  _dd.style.position = "absolute";
  _dd.style.top = ((_height-_ddh)/2)+"px";
  _dd.style.left = ((_width-_ddw)/2)+"px";
  _dd.style.padding = "20px";
  _dd.style.background = "#fff";
  _dd.style.border = "1px solid #ccc";
  _dd.style.fontFamily = "'Lucida Grande','Lucida Sans Unicode',Arial,Verdana,sans-serif";
  _dd.style.listStyleType = "none";
  _dd.style.color = "#4F4F4F";
  _dd.style.fontSize = "12px";

  // _h.appendChild(document.createTextNode(msg1));
  // var _hd = document.getElementById('_h');
  // _hd.style.display = "block";
  // _hd.style.fontSize = "1.3em";
  // _hd.style.marginBottom = "0.5em";
  // _hd.style.color = "#333";
  // _hd.style.fontFamily = "Helvetica,Arial,sans-serif";
  // _hd.style.fontWeight = "bold";

  // _p1.appendChild(document.createTextNode(msg2));
  // var _p1d = document.getElementById('_p1');
  // _p1d.style.marginBottom = "1em";

  // _p2.appendChild(document.createTextNode(msg3));
  // var _p2d = document.getElementById('_p2');
  // _p2d.style.marginBottom = "1em";

  _h_en.appendChild(document.createTextNode(msg1_en));
  var _hd_end = document.getElementById('_h_en');
  _hd_end.style.display = "block";
  _hd_end.style.fontSize = "1.3em";
  _hd_end.style.marginBottom = "0.5em";
  _hd_end.style.color = "#333";
  _hd_end.style.fontFamily = "Helvetica,Arial,sans-serif";
  _hd_end.style.fontWeight = "bold";

  _p1_en.appendChild(document.createTextNode(msg2_en));
  var _p1d_en = document.getElementById('_p1_en');
  _p1d_en.style.marginBottom = "1em";

  _p2_en.appendChild(document.createTextNode(msg3_en));
  var _p2d_en = document.getElementById('_p2_en');
  _p2d_en.style.marginBottom = "1em";

  var _uld = document.getElementById('_ul');
  _uld.style.listStyleImage = "none";
  _uld.style.listStylePosition = "outside";
  _uld.style.listStyleType = "none";
  _uld.style.margin = "0 px auto";
  _uld.style.padding = "0px";
  _uld.style.paddingLeft = "10px";

  var _li1d = document.getElementById('_li1');
  var _li2d = document.getElementById('_li2');
  var _li3d = document.getElementById('_li3');
  // var _li4d = document.getElementById('_li4');
  // var _li5d = document.getElementById('_li5');
  var _li1ds = _li1d.style;
  var _li2ds = _li2d.style;
  var _li3ds = _li3d.style;
  // var _li4ds = _li4d.style;
  // var _li5ds = _li5d.style;
  _li1ds.background = _li2ds.background = _li3ds.background /*= _li4ds.background = _li5ds.background*/ = "transparent url('"+imgPath+"background_browser.gif') no-repeat scroll left top";
  _li1ds.cursor = _li2ds.cursor = _li3ds.cursor /*= _li4ds.cursor = _li5ds.cursor*/ = "pointer";
  _li1d.onclick = function() {window.location = url1 }; 
  _li2d.onclick = function() {window.location = url2 }; 
  _li3d.onclick = function() {window.location = url3 }; 
  // _li4d.onclick = function() {window.location = url4 }; 
  // _li5d.onclick = function() {window.location = url5 }; 

  _li1ds.styleFloat = _li2ds.styleFloat = _li3ds.styleFloat /*= _li4ds.styleFloat = _li5ds.styleFloat*/ = "left";
  _li1ds.cssFloat = _li2ds.cssFloat = _li3ds.cssFloat /*= _li4ds.styleFloat = _li5ds.styleFloat*/ = "left";
  _li1ds.width = _li2ds.width = _li3ds.width /*= _li4ds.width = _li5ds.width*/ = "120px";
  _li1ds.height = _li2ds.height = _li3ds.height = /*_li4ds.height = _li5ds.height =*/ "122px";
  _li1ds.margin = _li2ds.margin = _li3ds.margin = /*_li4ds.margin = _li5ds.margin =*/ "0 10px 10px 0";

  var _ico1d = document.getElementById('_ico1');
  var _ico2d = document.getElementById('_ico2');
  var _ico3d = document.getElementById('_ico3');
  // var _ico4d = document.getElementById('_ico4');
  // var _ico5d = document.getElementById('_ico5');
  var _ico1ds = _ico1d.style;
  var _ico2ds = _ico2d.style;
  var _ico3ds = _ico3d.style;
  // var _ico4ds = _ico4d.style;
  // var _ico5ds = _ico5d.style;
  _ico1ds.width = _ico2ds.width = _ico3ds.width /*= _ico4ds.width = _ico5ds.width */ = "100px";
  _ico1ds.height = _ico2ds.height = _ico3ds.height /*= _ico4ds.height = _ico5ds.height */ = "100px";
  _ico1ds.margin = _ico2ds.margin = _ico3ds.margin /*= _ico4ds.margin = _ico5ds.margin */ = "1px auto";
  _ico1ds.background = "transparent url(data:image/gif;base64,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) no-repeat scroll left top";
  _ico2ds.background = "transparent url(data:image/gif;base64,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) no-repeat scroll left top";
  _ico3ds.background = "transparent url(data:image/gif;base64,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) no-repeat scroll left top";
  // _ico4ds.background = "transparent url('"+imgPath+"browser_opera.gif') no-repeat scroll left top";
  // _ico5ds.background = "transparent url('"+imgPath+"browser_chrome.gif') no-repeat scroll left top";

  _lit1.appendChild(document.createTextNode(br1));
  _lit2.appendChild(document.createTextNode(br2));
  _lit3.appendChild(document.createTextNode(br3));
  // _lit4.appendChild(document.createTextNode(br4));
  // _lit5.appendChild(document.createTextNode(br5));
  var _lit1d = document.getElementById('_lit1');
  var _lit2d = document.getElementById('_lit2');
  var _lit3d = document.getElementById('_lit3');
  // var _lit4d = document.getElementById('_lit4');
  // var _lit5d = document.getElementById('_lit5');
  var _lit1ds = _lit1d.style;
  var _lit2ds = _lit2d.style;
  var _lit3ds = _lit3d.style;
  // var _lit4ds = _lit4d.style;
  // var _lit5ds = _lit5d.style;
  _lit1ds.color = _lit2ds.color = _lit3ds.color /*= _lit4ds.color = _lit5ds.color*/ = "#808080";
  _lit1ds.fontSize = _lit2ds.fontSize = _lit3ds.fontSize /*= _lit4ds.fontSize = _lit5ds.fontSize*/ = "0.8em";
  _lit1ds.height = _lit2ds.height = _lit3ds.height /*= _lit4ds.height = _lit5ds.height*/ = "18px";
  _lit1ds.lineHeight = _lit2ds.lineHeight = _lit3ds.lineHeight /*= _lit4ds.lineHeight = _lit5ds.lineHeight*/ = "17px";
  _lit1ds.margin = _lit2ds.margin = _lit3ds.margin /*= _lit4ds.margin = _lit5ds.margin*/ = "1px auto";
  _lit1ds.width = _lit2ds.width = _lit3ds.width /*= _lit4ds.width = _lit5ds.width*/ = "118px";
  _lit1ds.textAlign = _lit2ds.textAlign = _lit3ds.textAlign /*= _lit4ds.textAlign = _lit5ds.textAlign*/ = "center";

}

// Returns the version of Internet Explorer or a -1
// (indicating the use of another browser).
function getInternetExplorerVersion() {
    var rv = -1; // Return value assumes failure.

    if (navigator.appName == 'Microsoft Internet Explorer') {
        var ua = navigator.userAgent;
        var re  = new RegExp("MSIE ([0-9]{1,}[\.0-9]{0,})");

        if (re.exec(ua) != null) {
            rv = parseFloat( RegExp.$1 );
        }
    }

    return rv;
}