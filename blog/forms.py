from django import forms
from .models import Account,Comment

class AccountForm(forms.Form):
    GENDER_CHOICES=(
        ('آقا','آقا'),
        ('خانم','خانم'),
    )
    name=forms.CharField(max_length=25,required=True,label='نام')
    last_name=forms.CharField(max_length=50,required=True,label='نام خانوادگی')
    phone=forms.CharField(max_length=11,min_length=11,required=True,label='شماره همراه')
    gender=forms.ChoiceField(choices=GENDER_CHOICES,widget=forms.RadioSelect,label='جنسیت')
    address=forms.CharField(max_length=250,widget=forms.Textarea,label='آدرس')
    age=forms.IntegerField(min_value=1,max_value=120,required=False,label='سن')
    
    def clean_phone(self):
        phone=self.cleaned_data['phone']
        if not phone.isdigit():
            raise forms.ValidationError(" شماره همراه باید از نوع عددی باشد ")
        if not phone.startswith('09'):
            raise forms.ValidationError(
                'شماره همراه باید با 09 شروع شود.')

        return phone



class ContactusForm(forms.Form):

    SUBJECT_CHOICES = (
        ('انتقاد و پیشنهاد', 'انتقاد و پیشنهاد'),
        ('شکایات', 'شکایات'),
    )
    message = forms.CharField(widget=forms.Textarea,required=True,label='پیام')
    name = forms.CharField(max_length=25,required=True,label='نام و نام خانوادگی')
    email = forms.EmailField(required=True,label='ایمیل')
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES,required=True,label='موضوع')
    phone = forms.CharField(max_length=11,required=False,label='شماره تماس')
    
class ShareForm(forms.Form):
    name=forms.CharField(widget=forms.TextInput,max_length=25,required=True,label='نام و نام خانوادگی')
    message=forms.CharField(widget=forms.Textarea,label='پیام')
    to=forms.EmailField(required=True,label='ایمیل')
    
    
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('name','body')