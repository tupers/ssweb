function _jump(id){
    var timer = null;
    clearInterval(timer);

    timer = setInterval(function () {
        var pos = document.getElementById(id).getBoundingClientRect().top;
        if(pos>0)
        {
            var speed = Math.ceil(pos/60);
            scrollTo(0,speed+document.documentElement.scrollTop);
        }
        else
            clearInterval(timer);
    },1)
}

function jumpToService()
{
    _jump('service_plan')
}