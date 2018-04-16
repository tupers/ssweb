var g_chart;

function init_order_list(csrf)
{
    var orders = $("div.order_list").find("li");
    orders.each(function(index,el){
        $(el).click(function () {
		if(!$(el).hasClass("order_list_selected"))
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
            if (msg.ret == 'success') {
                //set port and password
                $('#attr_table tr:eq(0) td:eq(1)').html(msg.port);
		$('#attr_table tr:eq(1) td:eq(1)').html(msg.password);
                //update chart and data usage
                $('#attr_table tr:eq(3) td:eq(1)').html(((msg.dataUsage/1024.0)/1024.0).toFixed(2));
		if(msg.dataLimit == -1)
		{
			$('#attr_table tr:eq(4) td:eq(1)').html(-1);
		    update_usage_chart(1,100);
		}
		else
		{
			$('#attr_table tr:eq(4) td:eq(1)').html(msg.dataLimit-msg.dataUsage);
			update_usage_chart(msg.dataUsage,msg.dataLimit-msg.dataUsage);
		}

		//update status
		if(msg.used == 1)
			$('#attr_table tr:eq(5) td:eq(1)').html("启用");
		else
			$('#attr_table tr:eq(5) td:eq(1)').html("停用");

		//update ip addr
		var ip_table = $('#node_table').children("tbody");
		ip_table.empty();
		var ip_arr = msg.ip;
		var len = ip_arr.length;
		for(var i=0;i<len;i++)
		{
			var addr;
			if(ip_arr[i] == "127.0.0.1")
				addr = "35.200.82.164";
			else
				addr = ip_arr[i];
			ip_table.append("<tr><td>地址:"+i+"</td><td>"+addr+"</td></tr>");
		}

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
