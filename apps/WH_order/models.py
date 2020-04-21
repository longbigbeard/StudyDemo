from django.db import models
from shortuuidfield import ShortUUIDField


class GoodsOrder(models.Model):
    uid = ShortUUIDField(primary_key=True)
    goods = models.ForeignKey("WH_goods.Goods", on_delete=models.DO_NOTHING)
    buyer = models.ForeignKey("WH_auth.User", on_delete=models.DO_NOTHING)
    # 选择出行的时间
    which_time = models.CharField(max_length=100, null=True)
    # 选择的是出行日期
    which_date = models.CharField(max_length=100, null=True)
    # 出行的人数
    person_nums = models.IntegerField(default=0)
    # 需要支付的费用
    amount = models.FloatField(default=0)
    pub_time = models.DateTimeField(auto_now_add=True)
    # 1：代表的是支付宝支付。2：代表的是微信支付
    istype = models.SmallIntegerField(default=0)
    # 1：代表的是未支付。2：代表的是支付成功.3:代表的是退款.4:代表退款中
    status = models.SmallIntegerField(default=1)
    # 0:代表处理了。1：代表未处理
    isdeal = models.SmallIntegerField(default=0)
    # 用户提交订单时候的留言。
    order_info = models.TextField(null=True)
    # 用户提交的手机号码
    order_tel = models.CharField(max_length=11, null=True)

    class Meta:
        ordering = ['pub_time']
