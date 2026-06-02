from django import  forms

class Bootsrap:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环modelform中的所有字段，给每个字段的插件设置
        for name, field in self.fields.items():
            # 字段中有属性，保留属性，没有属性需要增加属性
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
                field.widget.attrs["placeholder"] = field.label
            else:
                field.widget.attrs = {
                    "class": "form-control",
                    "placeholder": field.label}


#直接导入数据库字段
class BootsrapModel(Bootsrap,forms.ModelForm):
    pass


#直接写字段进行验证等，与数据库无连接
class BootsrapForm(Bootsrap,forms.Form):
    pass