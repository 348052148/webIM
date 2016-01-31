/**
 * Created by Administrator on 2016/1/19.
 */
var userInfo={};

function SocketIm(url)
{
    var ws= new WebSocket(url);
    var reData;
    this.send=function(data,uid,flag){
        if(flag==1)
        {
            ws.send('>_'+uid+'_'+data);
        }
        else if(flag==2)
        {
            ws.send('<_'+uid+'_'+data);
        }
    }
    this.recv=function(){
        return reData;
    }
    this.instance=function()
    {
        return ws;
    }
    this.date=function(){
        var myDate = new Date();
        return (1900+myDate.getYear()+"-"+(myDate.getMonth()+1)+"-"+myDate.getDate()+" "+myDate.getHours()+":"+myDate.getMinutes()+":"+myDate.getSeconds());
    }
    //通过id发送消息给好友
    this.sendFriend=function(data,uid)
    {
        this.send(data,uid,1);
    }
    //发送登录消息 返回uid
    this.sendLogin=function(name,pass){
        ws.send('&_login_'+name+'_'+pass);
    }
    //搜索好友
    this.sendSearch=function(name){
        ws.send('$_search_'+name);
    }
    //添加好友
    this.sendAddFriend=function(uid,name){
        ws.send('!_addfri_'+uid+'_'+name);
    }
    //发送获取最近联系人请求
    this.sendNearFriend=function(){

    }
    //关闭
    this.sendClose=function(){
        ws.send('^_close_kill');
    }
}
var Utils={

};
Utils.encode=function(data){
    return encodeURI(data);
}
Utils.decode=function(data){
    return decodeURI(data);
}
Utils.enBiaoq=function(val)
{
    var bq=new Array();
    bq['wx']='images/biaoq/wx.png';
    bq['pz']='images/biaoq/pz.png';
    bq['se']='images/biaoq/se.png';
    bq['bz']='images/biaoq/bz.png';
    bq['cy']='images/biaoq/cy.png';
    bq['dk']='images/biaoq/dk.png';
    bq['dy']='images/biaoq/dy.png';
    bq['fd']='images/biaoq/fd.png';
    bq['fn']='images/biaoq/fn.png';
    bq['gg']='images/biaoq/gg.png';
    bq['hx']='images/biaoq/hx.png';
    bq['jy']='images/biaoq/jy.png';
    bq['ll']='images/biaoq/ll.png';
    bq['shui']='images/biaoq/shui.png';
    bq['tp']='images/biaoq/tp.png';
    return '<img src="'+bq[val]+'">';
}
IMView={};
IMView.friendList=function(friends){
    for(var i=0;i<friends.length;i++) {
        //alert(friends[i].uid);
        var MsgDiag = '<li>' +
            '<a href="javascript:void(0);">' +
            '<div class="lk" name="'+friends[i].uid+'">' +
            '<img src="'+friends[i].avater+'" alt="" name="'+friends[i].uid+'" class="toux-img"/>' +
            '<span class="name" name="'+friends[i].uid+'">'+friends[i].name+'</span>' +
            '<div class="dz" name="'+friends[i].uid+'"><img src="images/dizhi.png" alt="" name="'+friends[i].uid+'" class="dizhi"/></div>' +
            '</div>' +
            '</a>' +
            '</li>';
        $('#friends').append(MsgDiag);
    }
    //好友数目显示
    $('#friends_avg').html($('#friends_avg').html()+"(0/"+friends.length+")");
}
IMView.addFriendList=function(fri){
    var MsgDiag = '<li>' +
        '<a href="javascript:void(0);">' +
        '<div class="lk" id="lk_'+fri.uid+'" name="'+fri.uid+'">' +
        '<img src="'+fri.avater+'" alt="" name="'+fri.uid+'" class="toux-img"/>' +
        '<span class="name" name="'+fri.uid+'">'+fri.name+'</span>' +
        '<div class="dz" name="'+fri.uid+'"><img src="images/dizhi.png" alt="" name="'+fri.uid+'" class="dizhi"/></div>' +
        '</div>' +
        '</a>' +
        '</li>';
    $('#friends').append(MsgDiag);
    $('#lk_'+fri.uid).click(function(evt){
        evt.stopPropagation();
        var id=$(evt.target).attr('name');
        //alert($(evt.target).attr('name'));
        IMView.mainMsgDialog(id,evt);

        //对话框标题
        $("#kill"+id+" #ming").html($(evt.target).children(".name").html());
        //对话框头像
        $("#kill"+id+" .chuankou").attr("src",$(evt.target).children("img").attr('src'));
    })
}
IMView.mainMsgDialog=function(id){
    if ( $("#kill"+id).length <= 0 ) {
        $('.main').append('<div class="neir" id="kill' + id + '"></div>');
        $("#kill" + id).append($('#wincopy').html());
        //发送事件
        $("#kill"+id+" .fasong").click(function(){
            var textarea=$("#kill"+id+" .textarea").html();
            if(textarea==""){
                alert("不能为空");
            }else{
                $("#kill"+id+" .xqnr .namei:last").css("padding-bottom","0");
                $("#kill"+id+" .xqnr").append('<div class="namei" ><div class="you" style="color:rebeccapurple;"><span style="color:rebeccapurple;">'+userInfo.getUserName()+'</span><span style="color:rebeccapurple;">'+Im.date()+'</span></div><div class="neirong" style="color:rebeccapurple;">'+textarea+'</div></div>');
                $("#kill"+id+" .xqnr .namei:last").css("padding-bottom","10px");
            }
            Im.sendFriend(Utils.encode(textarea),id);
            $("#kill"+id+" .textarea").html('')
        })
        //表情事件
        $("#kill"+id+" .biaoq").click (function(){
            var ht=$("#kill"+id+" .textarea").html();
            //$("#kill"+id+" .textarea").html(ht+Utils.enBiaoq('bq'));
            $("#kill"+id+" .bq").stop().fadeToggle("slow");
        });
        $("#kill"+id+" .bq ul .bqs img").click(function(){
            //alert($(this).attr('data'));
            var ht=$("#kill"+id+" .textarea").html();
            $("#kill"+id+" .textarea").html(ht+Utils.enBiaoq($(this).attr('data')));
            $("#kill"+id+" .bq").stop().fadeToggle("slow");
        });
        //关闭窗口事件
        $("#kill"+id+" .delete").click(function(){
            $("#kill"+id).css({display:'none'})
        })
    }else{
        $("#kill"+id).css({display:'block'})
    }

}
IMView.addMsgs=function(uid,name,tim,msg){
    $("#kill"+uid+" .xqnr .namei:last").css("padding-bottom","0");
    $("#kill"+uid+" .xqnr").append('<div class="namei"><div class="you"><span>'+name+'</span><span>'+tim+'</span></div><div class="neirong">'+Utils.decode(msg)+'</div></div>');
    $("#kill"+uid+" .xqnr .namei:last").css("padding-bottom","10px");
}
function UserInfo(name,uid,gid,friend)
{
    var _name=name;
    var _uid=uid;
    var _gid=gid;
    var _friend=friend;
    this.getFriend=function()
    {
        return _friend;
    }
    this.getUserName=function(){
        return _name;
    }
}