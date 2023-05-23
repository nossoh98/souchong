from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text="Required. Add a valid email address")
    class Meta:
        model = Account
        fields = ('email','username','password1','password2')
        
    def clean_email(self):      #유효성 검증 method   아래 AccountAuthenticationForm과 같이 한개의 clean 함수만 사용해도 됨.
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"Email {email} is already in user")
    
    def clean_username(self):      #유효성 검증 method
        username = self.cleaned_data['username']
        try:
            account = Account.objects.get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"username {username} is already in user")
        
class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput) #password 위젯
    class Meta:
        model = Account
        fields = ("email",'password')
    def clean(self):                                          #여러 clean_XX를 만들지 않고 하나의 clean만 만들어도 됨.
        if self.is_valid():
            email       = self.cleaned_data['email']
            password    = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Login")
            
class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('username','email','profile_image','hide_email')
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError(f"Email {email} is already in use")
    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError(f"User {username} is already in user")
    # save overriding
    def save(self, commit=True):
        # 1. db를 읽어 Obejct를 생성
        # 2. 이후 일련의 데이터들에 작업을 마친 후 (여기서는 db의 값을 바꿔줌, Update profile) -> .
        # 3. 다시 Save
        account = super(AccountUpdateForm, self).save(commit=False)
        account.username = self.cleaned_data["username"]
        account.email = self.cleaned_data["email"]
        account.profile_image = self.cleaned_data['profile_image']
        account.hide_email = self.cleaned_data['hide_email']
        if commit:
            account.save()
        return account