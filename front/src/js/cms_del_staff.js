function EditStaff() {

}

EditStaff.prototype.listenDeleteEvent = function () {
    var deleteBtns = $(".btn-del");
    deleteBtns.click(function () {
        var btn = $(this);
        var staff_id = btn.attr('data-staff-id');
        myalert.alertConfirm({
            'text': '您是否要删除管理员？',
            'confirmCallback': function () {
                myajax.post({
                    'url': '/cms/delete_staff/',
                    'data': {
                        'staff_id': staff_id
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

EditStaff.prototype.run = function () {
    var self = this;
    self.listenDeleteEvent();
};

$(function () {
    var editstaff = new EditStaff();
    editstaff.run();
});