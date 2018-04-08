$(function () {
    $('#form_password').on('blur',function () {
        var text = $('#form_password').val();
        if(text == '')
            $('#form_password_err').removeClass("_hide");
        else
            $('#form_password_err').addClass("_hide");
    })
});

function _select_plan(group,plan){
    var opt = "{'group':"+group+",'plan':"+plan+"}";
    $('#form_plan').val(opt);
}

function addService(csrf){
    if($('#form_password').val() != '') {
        $.ajaxSetup({
            data: {csrfmiddlewaretoken: csrf}
        });
        $.ajax({
            url: "/users/service_list/",
            type: 'POST',
            data: {password: $("#form_password").val(), plan: $("#form_plan").val()},
            success: function (arg) {
                $('#service_form').addClass("_hide");
                var msg = $.parseJSON(arg);
                //service_info.append("<p>添加服务失败</p>");
                if (msg.ret == 'success')
                    $('#service_success').removeClass("_hide");
                else
                    $('#service_failed').removeClass("_hide");

            }
        });
    }
    else
        $('#form_password_err').removeClass("_hide");
}

