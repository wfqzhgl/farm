/**
  * jQuery Cookie Plugin v0.2
  * Easily get/add/delete/modify browser cookies.
  * @Author: Phoetry (http://phoetry.me)
  * @Url: http://phoetry.me/archives/jquery-cookie.html
  **/
~function(doc){
jQuery.cookie=function(key,val,opt){
	if(null==key)return doc.cookie;
	if(val!==''+val&&val!==+val)
	return unescape((doc.cookie.match(key+'=(.*?);')||0)[1]||'');
	opt=opt||{};
	var it,date=new Date,cookie=key+'='+encodeURIComponent(val);
	date.setDate(date.getDate()+(''!==val?opt.expires||30:-1));
	opt.expires=date.toUTCString();
	for(it in opt)opt.hasOwnProperty(it)&&opt[it]&&(cookie+=';'+it+'='+opt[it]);
	doc.cookie=cookie;
}
}(window.document);