function CMSOpertaeGoods() {

}

CMSOpertaeGoods.prototype.initDatePicker = function () {
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

CMSOpertaeGoods.prototype.listenDeleteEvent = function () {
    var deleteBtns = $(".delete-btn");
    deleteBtns.click(function () {
        var btn = $(this);
        var goods_id = btn.attr('data-goods-id');
        myalert.alertConfirm({
            'text': '您是否要删除这条线路吗？',
            'confirmCallback': function () {
                myajax.post({
                    'url': '/cms/delete_goods/',
                    'data': {
                        'goods_id': goods_id
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

CMSOpertaeGoods.prototype.run = function () {
    var self = this;
    self.initDatePicker();
    self.listenDeleteEvent();
};

$(function () {
    var operategoods = new CMSOpertaeGoods();
    operategoods.run();
});