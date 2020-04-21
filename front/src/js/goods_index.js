function Index() {
    var self = this;
    self.page = 2;
}

Index.prototype.litenLoadMoreEvent = function () {
    var self = this;
    var loadMoreBtn = $('#load-more-btn');
    loadMoreBtn.click(function () {
        myajax.get({
            'url': '/good/list/',
            'data': {
                'p': self.page
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    console.log(result['data']);
                    var goods = result['data'];
                    if (goods.length > 0) {
                        var tpl = template("goods-item", {"goods": goods});
                        var ul = $('.goods-list-contain-ul');
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
