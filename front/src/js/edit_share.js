function EditShare() {

}

EditShare.prototype.listenDeleteEvent = function () {
    var deleteBtns = $(".delete-btn");
    deleteBtns.click(function () {
        var btn = $(this);
        var comment_id = btn.attr('data-comment-id');
        myalert.alertConfirm({
            'text': '您是否要删除这条评论吗？',
            'confirmCallback': function () {
                myajax.post({
                    'url': '/account/edit_share_info/',
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

EditShare.prototype.run = function () {
    var self = this;
    self.listenDeleteEvent();
};

$(function () {
    var editshare = new EditShare();
    editshare.run();
});