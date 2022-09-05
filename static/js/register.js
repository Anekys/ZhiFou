function bindCaptchaBtnClick(){
    $("#btn-captcha").on("click",function(event) {
        const $this = $(this)
        const email = $("input[name=email]").val();
        if(!email){
            alert("邮箱不能为空!");
            return;
        }
        // 正则验证邮箱格式
        reg = /^\w+((.\w+)|(-\w+))@[A-Za-z0-9]+((.|-)[A-Za-z0-9]+).[A-Za-z0-9]+$/;
        if(!reg.test(email)){
            alert("邮箱格式不正确!");
            return;
        }
        $this.off("click")
        let count = 60
        timer = setInterval(function (){
            if(count>0){
                $this.text(count+"秒后重新发送")
                count-=1
            }else{
                $this.text("获取验证码")
                bindCaptchaBtnClick()
                clearInterval(timer)
            }
        },1000)
        $.ajax({
            url:"/user/get_captcha",
            method:"post",
            data:{
                "email":email
            },
            success:function (data){
                let stats = data["stats"]
                if(stats == 200){
                    alert(data["message"])
                }else if(stats == 400){
                    alert(data["message"])
                }else {
                    alert("遇到未知错误,请稍后重试!")
                    console.log(data)
                }
            }
        })
    })
}
// 等待网页文档加载完毕后才执行
$(function (){
    bindCaptchaBtnClick();
})