function Scene() {

}

Scene.prototype.listenUploadThumbnailFileEvent = function () {

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

Scene.prototype.listenUploadBigFileEvent = function () {
    var uploadBtn = $('#big-img-btn');
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
                    var thumbnailInput = $('#big-img-form');
                    thumbnailInput.val(url);
                }
            }
        });
    });
};


Scene.prototype.listenUploadVideoFileEvent = function () {
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

Scene.prototype.initInfoSceneUeditor = function(){
    window.infosceneue = UE.getEditor('info-editor', {
        'initialFrameHeight': 400,
        'serverUrl': '/ueditor/upload/',
    });
};

Scene.prototype.initAttentionSceneUeditor = function(){
    window.attentionsceneue = UE.getEditor('attention-editor', {
        'initialFrameHeight': 400,
        'serverUrl': '/ueditor/upload/',
    });
};

Scene.prototype.initMoreImgSceneUeditor = function(){
    window.moreimgsceneue = UE.getEditor('more-img-editor', {
        'initialFrameHeight': 400,
        'serverUrl': '/ueditor/upload/',
    });
};

Scene.prototype.listenSubmitEvent = function(){
    var submitBtn = $('#submit-btn');
    submitBtn.click(function (event) {
        event.preventDefault();

        var btn = $(this);
        var pk = btn.attr("data-scene-id");
        var url = '';
        if(pk){
            url = '/cms/edit_scene/';
        }else{
            url = '/cms/write_scenes/';
        }

        var title = $("input[name='title']").val();
        var ranking = $("input[name='ranking']").val();
        var prices = $("input[name='prices']").val();
        var grade = $("input[name='grade']").val();
        var scene_info = window.infosceneue.getContent();
        var danger_info = window.attentionsceneue.getContent();
        var moreimage = window.moreimgsceneue.getContent();
        var thumbnail = $("input[name='thumbnail-img']").val();
        var bigimage = $("input[name='big-img']").val();
        var scene_video = $("input[name='video']").val();


        myajax.post({
            'url': url,
            'data':{
                'title':title,
                'ranking':ranking,
                'grade':grade,
                'prices':prices,
                'scene_info':scene_info,
                'danger_info':danger_info,
                'moreimage':moreimage,
                'thumbnail':thumbnail,
                'bigimage':bigimage,
                'scene_video':scene_video,
                'pk':pk,
            },
            'success':function (result) {
                if(result['code'] === 200){
                    myalert.alertSuccess('景点增加成功！',function () {
                        window.location.reload();
                    });

                }
            }

        })

    });
};

Scene.prototype.run = function () {
    self = this;
    self.listenUploadThumbnailFileEvent();
    self.listenUploadBigFileEvent();
    // self.listenUploadMoreFileEvent();
    self.listenUploadVideoFileEvent();
    // self.handleFileUploadProcess();
    self.initInfoSceneUeditor();
    self.initAttentionSceneUeditor();
    self.initMoreImgSceneUeditor();
    self.listenSubmitEvent();
};

Scene.prototype.handleFileUploadProcess = function (response) {
    var total = response.total;
    var precent = total.percent;
    var progressGroup = $("#progress-group");
    progressGroup.show();
    var processBar = $('.progress-bar');
    processBar.css({"width":precent+'%'});

};

$(function () {
    var scene = new Scene();
    scene.run();
});