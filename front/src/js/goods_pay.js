function Ordering() {

}

Ordering.prototype.listenSubmitEvent = function () {
    var submitBtn = $('#submit-order');
    submitBtn.click(function (event) {
        event.preventDefault();
        var which_time = $("input[type=radio]:checked").val();
        var which_date = $('input[name="which-date"]').val();
        var person_nums = $('select[name="person-nums"]').val();
        var order_tel = $('input[name="telephone"]').val();
        var order_info = $('input[name="order_info"]').val();

        var btn = $(this);
        var goods_pk = btn.attr('data-goods-id');
        if (!order_tel) {
            order_tel = '0';
        }
        which_date = which_date.replace(/-/g, '/');
        var data = new Date(which_date);
        var nowdate = new Date();
        if (which_time && which_date && person_nums) {
            if (nowdate > data) {
                window.messageBox.showError("您选择的时间有误！")
            } else {
                myajax.post({
                    'url': '/order/new_order/',
                    'data': {
                        'which_time': which_time,
                        'which_date': which_date,
                        'person_nums': person_nums,
                        'order_tel': order_tel,
                        'order_info': order_info,
                        'goods_pk': goods_pk,
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            var order_id = result['data']['order_id'];
                            console.log(order_id);
                            myalert.alertConfirm({
                                'text': "订单创建完成，即将跳转到支付界面！",
                                'confirmCallback': function () {
                                    window.location.href = "/order/" + order_id;
                                },
                                'cancelCallback': function () {
                                    window.messageBox.showError("您可以在个人中心查看订单并付款！");
                                },
                            })
                        }
                    }
                });
            }
        } else {
            window.messageBox.showError("你的选择有误，请重新选择！")
        }
    });
};

Ordering.prototype.run = function () {
    var self = this;
    self.listenSubmitEvent();
};

$(function () {
    var ordering = new Ordering();
    ordering.run();
});