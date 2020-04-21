function CMSOpertaeOrder() {

}

CMSOpertaeOrder.prototype.initDatePicker = function () {
    var startPicker = $('#start-picker');
    var endPicker = $('#end-picker');

    var todayDate = new Date();
    var todayStr = todayDate.getFullYear() + '/' + (todayDate.getMonth() + 1) + '/' + todayDate.getDate();
    var options = {
        'showButtonPanel': true,
        'format': 'yyyy/mm/dd',
        'startDate': '2019/3/1',
        'endDate': todayStr,
        'language': 'zh-CN',
        'todayBtn': 'linked',
        'todayHighlight': true,
        'clearBtn': true,
        'autoclose': true
    };

    startPicker.datepicker(options);
    endPicker.datepicker(options);
};

CMSOpertaeOrder.prototype.listenDeleteEvent = function () {
    var deleteBtns = $(".delete-btn");
    deleteBtns.click(function () {
        var btn = $(this);
        var order_id = btn.attr('data-order-id');
        myalert.alertConfirm({
            'text': '您确定要处理这个订单吗？',
            'confirmCallback': function () {
                myajax.post({
                    'url': '/cms/deal_order/',
                    'data': {
                        'order_id': order_id
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            // window.location = window.location.href;
                            window.location.reload()
                        }
                    }
                });
            }
        });
    });
};

CMSOpertaeOrder.prototype.run = function () {
    var self = this;
    self.initDatePicker();
    self.listenDeleteEvent();
};

$(function () {
    var operateorder = new CMSOpertaeOrder();
    operateorder.run();
});