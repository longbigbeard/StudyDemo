function Goods() {

}

Goods.prototype.listenUploadThumbnailFileEvent = function () {

    var uploadBtn = $('#thumbnail-btn');
    uploadBtn.change(function () {
        var file = uploadBtn[0].files[0];
        var formData = new FormData();
        formData.append('file', file);
        myajax.post({
            'url': '/cms/upload_img_file/',
            'data': formData,
            'processData': false,
            'contentType': false,
            'success': function (result) {
                if (result['code'] === 200) {
                    console.log(result['data']);
                    var url = result['data']['url'];
                    var thumbnailInput = $('#thumbnail-img-form');
                    thumbnailInput.val(url);
                }
            }
        });
    });

};

Goods.prototype.listenUploadVideoFileEvent = function () {
    var uploadBtn = $('#video-btn');
    uploadBtn.change(function () {
        var file = uploadBtn[0].files[0];
        var formData = new FormData();
        formData.append('file', file);
        myajax.post({
            'url': '/cms/upload_img_file/',
            'data': formData,
            'processData': false,
            'contentType': false,
            'success': function (result) {
                if (result['code'] === 200) {
                    console.log(result['data']);
                    var url = result['data']['url'];
                    var thumbnailInput = $('#video-form');
                    thumbnailInput.val(url);
                }
            }
        });
    });
};

Goods.prototype.initInfoGoodsUeditor = function () {
    window.infogoodsue = UE.getEditor('info-editor', {
        'initialFrameHeight': 400,
        'serverUrl': '/ueditor/upload/',
    });
};

Goods.prototype.initFeatureGoodsUeditor = function () {
    window.featuregoodsue = UE.getEditor('feature-editor', {
        'initialFrameHeight': 400,
        'serverUrl': '/ueditor/upload/',
    });
};

Goods.prototype.initscheduleGoodsUeditor = function () {
    window.schedulegoodsue = UE.getEditor('schedule-editor', {
        'initialFrameHeight': 400,
        'serverUrl': '/ueditor/upload/',
    });
};

Goods.prototype.initAttentionGoodsUeditor = function () {
    window.attentiongoodsue = UE.getEditor('attention-editor', {
        'initialFrameHeight': 400,
        'serverUrl': '/ueditor/upload/',
    });
};

Goods.prototype.listenSubmitEvent = function () {
    var submitBtn = $('#submit-btn');
    submitBtn.click(function (event) {
        event.preventDefault();

        var btn = $(this);
        var pk = btn.attr("data-goods-id");
        var url = '';
        if(pk){
            url = '/cms/edit_goods/';
        }else{
            url = '/cms/write_goods/';
        }

        var title = $("input[name='title']").val();
        var sales = $("input[name='sales']").val();
        var prices = $("input[name='prices']").val();
        var goods_info = window.infogoodsue.getContent();
        var feature_info = window.featuregoodsue.getContent();
        var schedule_goods = window.schedulegoodsue.getContent();
        var attention_goods = window.attentiongoodsue.getContent();
        var thumbnail = $("input[name='thumbnail-img']").val();
        var goods_video = $("input[name='video']").val();

        myajax.post({
            'url': url,
            'data': {
                'title': title,
                'sales': sales,
                'prices': prices,
                'goods_info': goods_info,
                'feature_info': feature_info,
                'schedule_goods': schedule_goods,
                'attention_goods': attention_goods,
                'thumbnail': thumbnail,
                'goods_video': goods_video,
                'pk':pk,
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    myalert.alertSuccess('线路增加成功！', function () {
                        window.location.reload();
                    });

                }
            }

        })

    });
};

Goods.prototype.run = function () {
    self = this;
    self.listenUploadThumbnailFileEvent();
    self.listenUploadVideoFileEvent();
    self.initInfoGoodsUeditor();
    self.initFeatureGoodsUeditor();
    self.initscheduleGoodsUeditor();
    self.initAttentionGoodsUeditor();
    self.listenSubmitEvent();
};

$(function () {
    var goods = new Goods();
    goods.run();
});