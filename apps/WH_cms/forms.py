from apps.forms import FormMixin
from django import forms
from apps.WH_scene.models import Scenes
from apps.WH_goods.models import Goods
from apps.WH_index.models import Banner


class WriteScenesForms(forms.ModelForm, FormMixin):
    class Meta:
        model = Scenes
        exclude = ['pub_time', 'author', 'scene_desc']


class EditScenesForms(forms.ModelForm, FormMixin):
    pk = forms.IntegerField()

    class Meta:
        model = Scenes
        exclude = ['pub_time', 'author', 'scene_desc']


class EditGoodsForms(forms.ModelForm, FormMixin):
    pk = forms.IntegerField()

    class Meta:
        model = Goods
        exclude = ['pub_time', 'author']


class WriteGoodsForm(forms.ModelForm, FormMixin):
    class Meta:
        model = Goods
        exclude = ['pub_time', 'author']


class AddBannerForm(forms.ModelForm, FormMixin):
    class Meta:
        model = Banner
        fields = ('priority', 'link_to', 'image_url')


class EditBannerForm(forms.ModelForm, FormMixin):
    pk = forms.IntegerField()

    class Meta:
        model = Banner
        fields = ('priority', 'link_to', 'image_url')
