function EditOrder() {

}

EditOrder.prototype.listenSubmitEvent = function () {
    var submitBtn = $('.delete-btn');
    submitBtn.click(function (event) {
        event.preventDefault();
        var btn = $(this);
        var order_id = btn.attr('data-order-id');
        var status = btn.attr('data-status');

        if(status === "已付款"){
            myalert.alertConfirm({
                'text':"确认退订？",
                'confirmCallback':function () {
                   myajax.post({
                'url': '/account/edit_order_info/',
                'data': {
                    'order_id': order_id,
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        myalert.alertSuccess("申请成功，1-2个工作日内会后工作人员和您联系。")
                    }
                }
            });
                }
            });

        }else {
            myalert.alertError("您的订单未支付或已经退款，请勿重复操作！")
        }

    });
};


EditOrder.prototype.run = function () {
    var self = this;
    self.listenSubmitEvent();
};

$(function () {
    var editorder = new EditOrder();
    editorder.run();
});