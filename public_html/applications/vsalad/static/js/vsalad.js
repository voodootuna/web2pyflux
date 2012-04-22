$(document).ready(function() {
var css = ".comment{"+
"    -moz-border-radius:7px !important;"+
"    -webkit-border-radius:7px !important;"+
"   margin-left:10px!important;"+
"   margin-right:110px!important;"+
"   margin-top:0px!important;"+
"   margin-bottom:8px!important;"+

"   background-color:#ffffff !important;"+
"   border:1px solid #bbbcbf !important;"+
"   padding-left:5px!important;"+
"   padding-top:5px!important;"+
"   padding-right:8px!important;"+
"   padding-bottom:0px!important;"+
"}"+
".comment .comment{"+
"   margin-right:0px!important;"+
"   background-color:#F7F7F8 !important;"+  
"}"+
".comment .comment .comment{"+
"   background-color:#ffffff !important;"+  
"}"+
".comment .comment .comment .comment{"+
"   background-color:#F7F7F8 !important;"+  
"}"+
".comment .comment .comment .comment .comment{"+
"   background-color:#ffffff !important;"+  
"}"+
".comment .comment .comment .comment .comment .comment{"+
"   background-color:#F7F7F8 !important;"+  
"}"+
".comment .comment .comment .comment .comment .comment .comment{"+
"   background-color:#ffffff !important;"+  
"}"+ 
"body > .content {"+ 
" padding-right:0px; !important;"; 
"}"; 

if (typeof GM_addStyle != "undefined") {
    GM_addStyle(css);
} else if (typeof PRO_addStyle != "undefined") {
    PRO_addStyle(css);
} else if (typeof addStyle != "undefined") {
    addStyle(css);
} else {
    var heads = document.getElementsByTagName("head");
    if (heads.length > 0) {
        var node = document.createElement("style");
        node.type = "text/css";
        node.appendChild(document.createTextNode(css));
        heads[0].appendChild(node); 
    }
}

function prettyDate(time){
    var date = new Date((time || "").replace(/-/g,"/").replace(/[TZ]/g," ")),
        diff = (((new Date()).getTime() - date.getTime()) / 1000),
        day_diff = Math.floor(diff / 86400);
            
    if ( isNaN(day_diff) || day_diff < 0 || day_diff >= 31 )
        return;
            
    return day_diff == 0 && (
            diff < 60 && "just now" ||
            diff < 120 && "1 minute ago" ||
            diff < 3600 && Math.floor( diff / 60 ) + " minutes ago" ||
            diff < 7200 && "1 hour ago" ||
            diff < 86400 && Math.floor( diff / 3600 ) + " hours ago") ||
        day_diff == 1 && "Yesterday" ||
        day_diff < 7 && day_diff + " days ago" ||
        day_diff < 31 && Math.ceil( day_diff / 7 ) + " weeks ago" ||
        day_diff < 365 && Math.ceil( day_diff / 30 ) + " months ago" ||
        day_diff > 365 && Math.ceil( day_diff / 365 ) + " years ago";
}


    var links = document.getElementsByTagName("a"); 
    for ( var i = 0; i < links.length; i++ )
        if ( links[i].title ) {
            var date = prettyDate(links[i].title);
            if ( date )
                links[i].innerHTML = date;
        }


 })
