function CMSOpertaeScene() {

}

CMSOpertaeScene.prototype.initDatePicker = function () {
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

CMSOpertaeScene.prototype.listenDeleteEvent = function () {
    var deleteBtns = $(".delete-btn");
    deleteBtns.click(function () {
        var btn = $(this);
        var scene_id = btn.attr('data-scene-id');
        myalert.alertConfirm({
            'text': '您是否要删除这个景点吗？',
            'confirmCallback': function () {
                myajax.post({
                    'url': '/cms/delete_scene/',
                    'data': {
                        'scene_id': scene_id
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

CMSOpertaeScene.prototype.run = function () {
    var self = this;
    self.initDatePicker();
    self.listenDeleteEvent();
};

$(function () {
    var operatescene = new CMSOpertaeScene();
    operatescene.run();
});