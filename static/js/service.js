        function requirePort(){
            $.ajaxSetup({
                data:{csrfmiddlewaretoken:'{{ csrf_token }}'}
            });
            $.ajax({
                url:"{% url 'users:requireport' %}",
                type:'POST',
                data:{user:"{{user.username}}"},
                success: function(arg){
                    var ret = $.parseJSON(arg);
                    var service_info = $("#service_info");
                    if(ret.port!="None")
                    {
                        service_info.empty();
                        service_info.append("<p id=\"port\">"+ret.port+"</p>");
                        service_info.append("<p>设置密码:</p>");
                        service_info.append("<input type=\"text\" id=\"pwd\"/>");
                        service_info.append("<button class=\"btn btn-default\" onclick=\"addService();\">提交</button>");
                    }
                    else
                    {
                        service_info.empty();
                        service_info.append("<p>no available port.</p>");
                    }

                }
            });
        }
        function addService(){
            $.ajaxSetup({
                data:{csrfmiddlewaretoken:'{{ csrf_token }}'}
            });
            $.ajax({
                url:"{% url 'users:addservice' %}",
                type:'POST',
                data:{password:$("#pwd").val(),port:$("#port").html()},
                success:function(arg){
                    var ret = $.parseJSON(arg);
                    var service_info = $("#service_info");
                    if(ret.status!="ok")
                    {
                        service_info.empty();
                        service_info.append("<p>添加服务失败</p>");
                    }
                    else
                    {
                        service_info.empty();
                        service_info.append("<p>添加服务成功</p>")
                    }
                }
            });
        }