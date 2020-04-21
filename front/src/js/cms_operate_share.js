function CMSOpertaeShare() {

}

CMSOpertaeShare.prototype.initDatePicker = function () {
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

CMSOpertaeShare.prototype.listenDeleteEvent = function () {
    var deleteBtns = $(".delete-btn");
    deleteBtns.click(function () {
        var btn = $(this);
        var comment_id = btn.attr('data-share-id');
        myalert.alertConfirm({
            'text': '您是否要删除这个评论吗？',
            'confirmCallback': function () {
                console.log("this is log");
                myajax.post({
                    'url': '/cms/delete_share/',
                    'data': {
                        'comment_id': comment_id
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

CMSOpertaeShare.prototype.run = function () {
    var self = this;
    self.initDatePicker();
    self.listenDeleteEvent();
};

$(function () {
    var operateshare = new CMSOpertaeShare();
    operateshare.run();
});