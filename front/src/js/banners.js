function Banners() {

}

Banners.prototype.createBannerItem = function (banner) {
    var self = this;
    var tpl = template('banner-item', {"banner": banner});
    var bannerListGroup = $(".banner-list-group");
    var bannerItem = null;

    if (banner) {
        bannerListGroup.append(tpl);
        bannerItem = bannerListGroup.find(".banner-items:last");
    } else {
        bannerListGroup.prepend(tpl);
        bannerItem = bannerListGroup.find(".banner-items:first");
    }

    self.addImageSelectEvent(bannerItem);
    self.addRemoveBannerEvent(bannerItem);
    self.addSaveBannerEvent(bannerItem);
};

Banners.prototype.loadData = function () {
    var self = this;
    myajax.get({
        'url': '/cms/banner_list/',
        'success': function (result) {
            if (result['code'] === 200) {
                var banners = result['data'];
                for (var i = 0; i < banners.length; i++) {
                    var banner = banners[i];
                    self.createBannerItem(banner);
                }
            }
        }
    })
};

Banners.prototype.listenAddBannerEvent = function () {
    var self = this;

    var addBtn = $("#add-banner-btn");
    addBtn.click(function () {
        var bannerListGroup = $('.banner-list-group');
        var list_length = bannerListGroup.children().length;
        if (list_length >= 6) {
            window.messageBox.showInfo("最多只能添加6张图片！");
            return;
        }
        self.createBannerItem();
    })
};

Banners.prototype.addImageSelectEvent = function (bannerItem) {
    var image = bannerItem.find('.thumbnail');
    var imageInput = bannerItem.find('.image-input');
    // 图片不能打开文件选择
    image.click(function () {
        imageInput.click();
    });

    imageInput.change(function () {
        var file = this.files[0];
        var formData = new FormData();
        formData.append("file", file);
        myajax.post({
            'url': '/cms/upload_img_file/',
            'data': formData,
            'processData': false,
            'contentType': false,
            'success': function (result) {
                if (result['code'] === 200) {
                    var url = result['data']['url'];
                    image.attr('src', url);
                }
            }
        });
    })

};

Banners.prototype.addRemoveBannerEvent = function (bannerItem) {
    var closeBtn = bannerItem.find(".close-btn");

    closeBtn.click(function () {
        var bannerId = bannerItem.attr('data-banner-id');
        if (bannerId) {
            myalert.alertConfirm({
                'text': "您确定要删除这个轮播图吗？",
                'confirmCallback': function () {

                    myajax.post({
                        'url': '/cms/delete_banner/',
                        'data': {
                            'banner_id': bannerId
                        },
                        'success': function (result) {
                            if (result['code'] === 200) {
                                bannerItem.remove();
                                window.messageBox.showSuccess("删除成功！");
                            }
                        }
                    });
                }
            });
        } else {
            bannerItem.remove();
        }
    });

};

Banners.prototype.addSaveBannerEvent = function (bannerItem) {
    var saveBtn = bannerItem.find('.save-btn');
    var imageTag = bannerItem.find('.thumbnail');
    var priorityTag = bannerItem.find("input[name='priority']");
    var linktoTag = bannerItem.find("input[name='link_to']");
    var prioritySpan = bannerItem.find("span[class='priority']");

    var bannerId = bannerItem.attr("data-banner-id");
    var url = '';
    if (bannerId) {
        url = '/cms/edit_banner/';
    } else {
        url = '/cms/add_banner/';
    }

    saveBtn.click(function () {
        var image_url = imageTag.attr('src');
        var priority = priorityTag.val();
        var link_to = linktoTag.val();

        myajax.post({
            'url': url,
            'data': {
                'image_url': image_url,
                'priority': priority,
                'link_to': link_to,
                'pk': bannerId,
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    if (bannerId) {
                        window.messageBox.showSuccess("轮播图修改完成！");
                    } else {
                        bannerId = result['data']['banner_id'];
                        bannerItem.attr("data-banner-id", bannerId);
                        window.messageBox.showSuccess("轮播图添加完成！");
                    }
                    prioritySpan.text("优先级：" + priority);

                }
            },
        });
    });
};

Banners.prototype.run = function () {
    var self = this;
    self.listenAddBannerEvent();
    self.loadData();

};

$(function () {
    banners = new Banners();
    banners.run();
});