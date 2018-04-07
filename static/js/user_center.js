var g_chart;

function init_order_list(csrf)
{
    var orders = $("div.order_list").find("li");
    orders.each(function(index,el){
        $(el).click(function () {
            select_order('div.order_list',index,csrf);
        })
    })
}

function init_order_list_mobile(csrf)
{
    var order_select = $("#order_select");
    order_select.change(function () {
        get_order_information(order_select.val(),csrf);
    });
}

function create_usage_chart(used,unused){
    var ctx = $('#usage_chart');
    g_chart = new Chart(ctx,{
        type:'pie',
        data:{
            datasets: [{
                data: [used, unused],
                backgroundColor: [
                    'rgba(50,155,255,1)',
                    'rgba(155,155,155,1)'
                ]
            }],

            // These labels appear in the legend and in the tooltips when hovering different arcs
            labels: [
                'used',
                'unused'
            ]
        }
    });
}

function get_order_information(order_id,csrf) {
    $.ajaxSetup({
        data: {csrfmiddlewaretoken: csrf}
    });
    $.ajax({
        url: "/users/get_order_info/",
        type: 'POST',
        data: {id:order_id},
        success: function (arg) {
            var msg = $.parseJSON(arg);
            if (msg.result == 'success') {
                //set port
                $('#attr_table tr:eq(0) td:eq(1)').html(msg.port)
                //set usage
                $('#attr_table tr:eq(2) td:eq(1)').html(msg.dataUsage)
                $('#attr_table tr:eq(3) td:eq(1)').html(msg.dataLimit-msg.dataUsage)
                //update chart
                update_usage_chart(msg.dataUsage,msg.dataLimit-msg.dataUsage);
                $('#info').removeClass("_hide");
                $('#info_none').addClass("_hide");
            }
            else{
                $('#info').addClass("_hide");
                $('#info_none').removeClass("_hide");
            }
        }
    });
}

function update_usage_chart(used,unused)
{
    g_chart.data.datasets[0].data[0] = used;
    g_chart.data.datasets[0].data[1] = unused;
    g_chart.update()
}

function select_order(order_ul,index,csrf){
    var orders = $(order_ul).find("li");
    orders.each(function(idx,el){
        if(index==idx)
            $(el).addClass("order_list_selected");
        else
            $(el).removeClass("order_list_selected");
    });
    var order_id = orders.eq(index).find("span").eq(0).html();
    get_order_information(order_id,csrf);
}

function select_order_mobile(order_select,index,csrf){
    var orders = $(order_select).find("option");
    var order_id = orders.eq(index).val();
    $(order_select).val(order_id);
    get_order_information(order_id,csrf);
}