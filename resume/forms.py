from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, Skill, Experience, Education, Portfolio, ContactMessage
from .models import Testimonial

# فرم ثبت‌نام
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

# فرم ورود
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)

# فرم ویرایش پروفایل
from django import forms
from .models import Profile

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'job_title', 'bio', 'profile_image', 'linkedin', 'github', 'twitter', 'telegram']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 5}),
        }

    def save(self, commit=True):
        profile = super().save(commit=False)
        if not profile.user:
            profile.user = self.instance.user  # اطمینان از اینکه user تنظیم شود
        if commit:
            profile.save()
        return profile



# فرم مهارت‌ها
class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'level']

# فرم تجربیات کاری
class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['company_name', 'position', 'description', 'start_date', 'end_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

# فرم تحصیلات
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institution_name', 'degree', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

# فرم نمونه کارها


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['title', 'description', 'image', 'link']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }


# فرم تماس (برای کاربران مهمان)
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']



