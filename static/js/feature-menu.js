$(document).ready(function () {
    var plan_tabs = $("div.plan-head").find("li");
    var plans = $("div.plan-detail");
    //link each list to ctx by index
    plan_tabs.each(function(index,el){
        $(el).mouseover(function(){
            plans.each(function(i,_el){
                if(i==index)
                {
                    $(_el).addClass("plan-detail-selected");
                    plan_tabs.eq(i).addClass("plan-head-selected");
                }
                else
                {
                    $(_el).removeClass("plan-detail-selected");
                    plan_tabs.eq(i).removeClass("plan-head-selected");
                }
            });
        });
    });

    //display first ctx as default
    plan_tabs.eq(0).addClass("plan-head-selected");
    plans.eq(0).addClass("plan-detail-selected");

})