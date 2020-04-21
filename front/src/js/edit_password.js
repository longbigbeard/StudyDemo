function EditPassword() {

}

EditPassword.prototype.listenSubmitEvent = function () {
    var submitBtn = $('#submit-btn');
    submitBtn.click(function (event) {
        event.preventDefault();

        var author_name = $("input[name='author-name']").val();
        var author_passwd = $("input[name='author-password']").val();
        console.log("aaaaaaaa");
        console.log(author_name,author_passwd);
        myajax.post({
            'url': '/account/edit_author_info/',
            'data': {
                'author_name': author_name,
                'author_passwd': author_passwd,
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    myalert.alertSuccess("您的信息修改成功！请刷新页面。")
                }
            }
        });
    });
};


EditPassword.prototype.run = function () {
    var self = this;
    self.listenSubmitEvent();
};

$(function () {
    var editpassword = new EditPassword();
    editpassword.run();
});