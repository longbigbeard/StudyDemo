function Share() {
    var self = this;
    self.page = 2;

    template.defaults.imports.timeSince = function (dateValue) {
            var date = new Date(dateValue);
            var datets = date.getTime(); // 得到的是毫秒的
            var nowts = (new Date()).getTime(); //得到的是当前时间的时间戳
            var timestamp = (nowts - datets)/1000; // 除以1000，得到的是秒
            if(timestamp < 60) {
                return '刚刚';
            }
            else if(timestamp >= 60 && timestamp < 60*60) {
                minutes = parseInt(timestamp / 60);
                return minutes+'分钟前';
            }
            else if(timestamp >= 60*60 && timestamp < 60*60*24) {
                hours = parseInt(timestamp / 60 / 60);
                return hours+'小时前';
            }
            else if(timestamp >= 60*60*24 && timestamp < 60*60*24*30) {
                days = parseInt(timestamp / 60 / 60 / 24);
                return days + '天前';
            }else{
                var year = date.getFullYear();
                var month = date.getMonth();
                var day = date.getDay();
                var hour = date.getHours();
                var minute = date.getMinutes();
                return year+'/'+month+'/'+day+" "+hour+":"+minute;
            }
        }

}

Share.prototype.initInfoShareUeditor = function () {
    window.infoshareue = UE.getEditor('share-content-editor', {
        'initialFrameHeight': 300,
        'serverUrl': '/ueditor/upload/',
    });
};

Share.prototype.listenSubmitEvent = function () {
    var submitBtn = $('#submit-btn');
    submitBtn.click(function (event) {
        event.preventDefault();

        var content = window.infoshareue.getContent();


        myajax.post({
            'url': '/share/',
            'data': {
                'content': content,
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    myalert.alertSuccess('评论增加成功！', function () {
                        window.location.reload();
                    });

                }
            }

        })

    });
};

Share.prototype.litenLoadMoreEvent = function () {
    var self = this;
    var loadMoreBtn = $('#load-more-btn');
    loadMoreBtn.click(function () {
        myajax.get({
            'url': '/share/list/',
            'data': {
                'p': self.page
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    console.log(result['data']);
                    var comments = result['data'];
                    if (comments.length > 0) {
                        var tpl = template("share-content-item", {"comments": comments});
                        var ul = $('.comment-list');
                        ul.append(tpl);
                        self.page += 1;
                    } else {
                        loadMoreBtn.hide();
                    }

                }
            }
        })
    })
};


Share.prototype.run = function () {
    self = this;
    self.initInfoShareUeditor();
    self.listenSubmitEvent();
    self.litenLoadMoreEvent();
};

$(function () {
    var share = new Share();
    share.run();
});