function PayOrder() {

}

PayOrder.prototype.listenSubmitEvent = function () {
    var submitBtn = $('#submit-btn');
    submitBtn.click(function (event) {
        event.preventDefault();

        var istype = $("input[type=radio]:checked").val();
        console.log("aaaaaaaa");
        var btn = $(this);
        var order_pk = btn.attr('data-order-id');
        console.log(istype,order_pk);
        myajax.post({
            'url': '/order/pay_order/',
            'data': {
                'istype': istype,
                'order_pk': order_pk,
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    myalert.alertConfirm({
                        'text': "订单支付完成，您可以在个人中心查看订单！稍后有工作人员与您联系。",
                        'confirmCallback': function () {
                            window.location.href = "/good/";
                        },
                        'cancelCallback': function () {
                            window.location.href = "/good/";
                        },
                    })
                }
            }
        });
    });
};

PayOrder.prototype.run = function () {
    var self = this;
    self.listenSubmitEvent();
};

$(function () {
    var payorder = new PayOrder();
    payorder.run();

});