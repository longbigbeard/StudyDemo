from apps.forms import FormMixin
from django import forms
from apps.WH_order.models import GoodsOrder


class NewOrderForms(forms.ModelForm, FormMixin):
    goods_pk = forms.CharField()
    which_time = forms.CharField()

    class Meta:
        model = GoodsOrder
        fields = ['which_date', 'person_nums', 'order_tel']
