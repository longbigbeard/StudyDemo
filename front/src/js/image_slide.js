function Banner() {
    this.bannerWidth = 1150;
    this.bannerGroup = $("#banner-group");
    this.index = 1;
    this.leftArrow = $(".left-arrow");
    this.rightArrow = $(".right-arrow");
    this.bannerUl = $("#banner-ul");
    this.liList = this.bannerUl.children("li");
    this.bannerCount = this.liList.length;
    this.pageControl = $(".page-control");
}

Banner.prototype.initBanner = function () {
    var self = this;
    var firstBanner = self.liList.eq(0).clone();
    var lastBanner = self.liList.eq(self.bannerCount - 1).clone();
    self.bannerUl.append(firstBanner);
    self.bannerUl.prepend(lastBanner);
    self.bannerUl.css({"width": self.bannerWidth * (self.bannerCount + 2), 'left': -self.bannerWidth});
};

Banner.prototype.initPageControl = function () {
    var self = this;
    for (var i = 0; i < self.bannerCount; i++) {
        var circle = $("<li></li>");
        self.pageControl.append(circle);
        if (i === 0) {
            circle.addClass("active");
        }
    }
    self.pageControl.css({"width": self.bannerCount * 12 + 8 * 2 + 16 * (self.bannerCount - 1)});
};

Banner.prototype.toggleArrow = function (isShow) {
    var self = this;
    if (isShow) {
        self.leftArrow.show();
        self.rightArrow.show();
    } else {
        self.leftArrow.hide();
        self.rightArrow.hide();
    }
};

Banner.prototype.animate = function () {
    var self = this;
    self.bannerUl.stop().animate({"left": -1150 * self.index}, 800);
    var index = self.index;
    if (index === 0) {
        index = self.bannerCount - 1;
    } else if (index === self.bannerCount + 1) {
        index = 0;
    } else {
        index = self.index - 1;
    }
    self.pageControl.children('li').eq(index).addClass("active").siblings().removeClass('active');
};

Banner.prototype.loop = function () {
    var self = this;
    this.timer = setInterval(function () {
        if (self.index >= self.bannerCount + 1) {
            self.bannerUl.css({"left": -self.bannerWidth});
            self.index = 2;
        } else {
            self.index++;
        }
        self.animate();
    }, 2000);
};


Banner.prototype.listenArrowClick = function () {
    var self = this;
    self.leftArrow.click(function () {
        if (self.index === 0) {
            // ==：1 == '1'：true
            // ==== 1 != '1'
            self.bannerUl.css({"left": -self.bannerCount * self.bannerWidth});
            self.index = self.bannerCount - 1;
        } else {
            self.index--;
        }
        self.animate();
    });

    self.rightArrow.click(function () {
        if (self.index === self.bannerCount + 1) {
            self.bannerUl.css({"left": -self.bannerWidth});
            self.index = 2;
        } else {
            self.index++;
        }
        self.animate();
    });
};

Banner.prototype.listenBannerHover = function () {
    var self = this;
    this.bannerGroup.hover(function () {
        // 第一个函数是，把鼠标移动到banner上会执行的函数
        clearInterval(self.timer);
        self.toggleArrow(true);
    }, function () {
        // 第二个函数是，把鼠标从banner上移走会执行的函数
        self.loop();
        self.toggleArrow(false);
    });
};

Banner.prototype.listenPageControl = function () {
    var self = this;
    self.pageControl.children("li").each(function (index, obj) {
        $(obj).click(function () {
            self.index = index;
            self.animate();
        });
    });
};


Banner.prototype.run = function () {
    console.log("sss");
    this.initBanner();
    this.initPageControl();
    this.loop();
    this.listenBannerHover();
    this.listenArrowClick();
    this.listenPageControl();
};

$(function () {
    var banner = new Banner();
    banner.run();
});