$(function(){
  var tlid = $('#tlid').val();
      tlname = $('#name').val();
  //Read cookies
  for(var i=0;true;i++){
    var key = lib.readCookie("tlid"+i);
    if(key){
      if(key==tlid){
        //update name
        lib.createCookie("tlname"+i,tlname,10000);
        break;
      }
    }else{
      //create new list cookie
      lib.createCookie("tlid"+i,tlid,10000);
      lib.createCookie("tlname"+i,tlname,10000);
      break;
    }
  }
  
  
  //TODO AJAX post on edit title
  $("#name").blur(function(){
    $.post($("#updateName").attr("action"),{name:$("#name").val()},function(data){
      if(data!="success"){
        alert(data);
      }
    });
  });
  
  var $li = $("#list li");
  if($li.length<=1){
    $("#add").addClass("alone").find(":text").focus();
    $("#add").submit(function(){
      $(this).removeClass("alone");
    });
  }
  
  $("#list").sortable({cursor: "-moz-grabbing", handle: ".handle", axis: "y",items:">li:not(#add)", 
    update:function(event, ui){
      var moved = ui.item;
      var pOrder = parseInt(moved.children().children(".torder").val(),10);
      var prevLi = moved.prev("li");
      var nOrder = NaN;
      if(prevLi.length > 0) {
        var bef = parseInt(prevLi.children().children(".torder").val(),10);
        nOrder = bef > pOrder ? bef : bef+1;
      } else {
        prevLi = moved.next("li");
        if(prevLi.length > 0) {
          var aft = parseInt(prevLi.children().children(".torder").val(),10);
          nOrder = aft > pOrder ? aft-1 : aft;
        }
      }
      if(nOrder != NaN && nOrder != pOrder) {
        var data = 'tkey='+moved.children().children(".tkey").val()+'&pOrder='+pOrder+'&nOrder='+nOrder;
        $.post('/list/'+tlid+'/order', data, function(data, textStatus){
          //do something?
        });
      }
    }
  });
  
  function replaceCheckboxes(){
    $(":checkbox").each(function(){
      if($(this).data("set"))return;
      var cb = $('<a role="checkbox" class="cb" />').data("cb",this)
        .click(function(){
          var chk = $(this).toggleClass("checked").data("cb");
          chk.checked = !chk.checked;
          $(chk).click();
        });
      if(this.checked) cb.addClass("checked");
      $(this).after(cb).data("set",true);
    });
  }
  
  function taskUpdate(e){
    var $this = $(this),
        $form = $this.parent("form"),
        params = $form.serialize();
    if($("#list li").length==1){return false;}
    if(e.target&&$(e.target).is(".delete")){
      params +="&delete=true";
    }
    $.post("/task/update",params,function(data){
      if(data==="deleted"){
        $form.parent().slideUp(200,function(){
          $(this).remove();
        });
      }else{
        var $newForm = $(data);
        $form.parent().before($newForm).remove();
        $newForm.each(bindListItemEvents);
      }
    });
    return false;
  }
  
  function textEdited(e){
    if(this.defaultValue != this.value)taskUpdate.call(this,e);
  }
  
  $("#newTask").submit(function(){
    $.post($(this).attr("action"),function(data,msg){
      $(data).hide().appendTo("#list").each(bindListItemEvents).slideDown(200,function(){
        $(this).find("input.text").focus();
      });
    });
    return false;
  })
  function bindListItemEvents(){
    var $this = $(this);
    $this.find(".delete").click(taskUpdate);
    $this.find("input.done").click(taskUpdate);
    $this.find("input.text").blur(textEdited)
    .keydown(function(e){
      var $t = $(this);
      if(e.keyCode == 38){
        var $prev=$t.parent().parent().prev().find(".text");
        if($prev.length){
          $t.blur();
          $prev.focus();
        }
      }else if(e.keyCode==40 || e.keyCode==13){
        $t.blur();
        var $li = $(this).parent().parent();
        var $next = $li.next();
        if($next.length==0){
          $("#newTask").submit();
        }else if($next.length>0){
          $next.find(".text").focus();
        }
      }else if(e.keyCode==8&&this.value.length==0){
        $t.parent().parent().prev().find(".text").focus();
        $t.siblings(".delete").trigger("click");
      }
    }).focus(function(){
      $(this).parent().parent().addClass("focus");
    }).blur(function(){
      $(this).parent().parent().removeClass("focus");
    });
    replaceCheckboxes();
  }

  $li.each(bindListItemEvents);
  
  $("#list form").live("submit",function(){
    return false;
  });
});
