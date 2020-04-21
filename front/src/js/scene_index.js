function Index() {
    var self = this;
    self.page = 2;
}

Index.prototype.litenLoadMoreEvent = function () {
    var self = this;
    var loadMoreBtn = $('#load-more-btn');
    loadMoreBtn.click(function () {
        myajax.get({
            'url': '/scene/list/',
            'data': {
                'p': self.page
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    console.log(result['data']);
                    var scenes = result['data'];
                    if (scenes.length > 0) {
                        var tpl = template("scenes-item", {"scenes": scenes});
                        var ul = $('.scene-list-contain-ul');
                        ul.append(tpl);
                        self.page += 1;
                    }else {
                        loadMoreBtn.hide();
                    }

                }
            }
        })
    })
};

Index.prototype.run = function () {
    var self = this;
    self.litenLoadMoreEvent();
};

$(function () {
    var index = new Index();
    index.run();
});
