$(function(){
  var hasLists = false;
  for(var i=0;true;i++){
    var key = lib.readCookie("tlid"+i);
    if(key){
      hasLists = true;
      $("#lists").append('<li><a href="/list/'+key+'">'+lib.readCookie("tlname"+i)+'</a></li>');
    }else{
      break;
    }
  }
  if(hasLists){
    $("#prevLists").show();
  }
  
  $("#name").keypress(function(){
    if(this.defaultValue === this.value){
      $(this).removeClass("default");
    }
  }).focus(function(){
    if(this.defaultValue === this.value){
      $(this).select();
    }
  });
});
