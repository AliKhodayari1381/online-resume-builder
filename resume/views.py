from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, Skill, Experience, Education, Portfolio, Testimonial, ContactMessage
from .forms import ProfileEditForm,SkillForm,ExperienceForm,EducationForm,PortfolioForm
from django.contrib.auth.decorators import login_required


def home_view(request):
    profile = Profile.objects.first()  # فرض بر اینکه یک پروفایل داریم
    
    # بررسی اینکه آیا تصویر پروفایل وجود دارد یا خیر
    if not profile.profile_image:
        profile.profile_image = 'path/to/default-profile.jpg'  # مسیر تصویر پیش‌فرض

    skills = Skill.objects.all()
    experiences = Experience.objects.all()
    educations = Education.objects.all()
    portfolios = Portfolio.objects.all()
    testimonials = Testimonial.objects.all()

    context = {
        'profile': profile,
        'skills': skills,
        'experiences': experiences,
        'educations': educations,
        'portfolios': portfolios,
        'testimonials': testimonials,
    }
    return render(request, 'home.html', context)

def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        ContactMessage.objects.create(name=name, email=email, message=message)
        messages.success(request, "پیام شما با موفقیت ارسال شد!")
        return redirect("home")
    return redirect("home")
from django.shortcuts import render
from .models import Profile

def view_personal_resume(request):
    if not request.user.is_authenticated:
        return redirect('login')  # هدایت کاربر به صفحه ورود در صورت عدم ورود

    profile = Profile.objects.get(user=request.user)
    skills = Skill.objects.filter(user=request.user)
    experiences = Experience.objects.filter(user=request.user)
    educations = Education.objects.filter(user=request.user)
    portfolios = Portfolio.objects.filter(user=request.user)

    context = {
        'profile': profile,
        'skills': skills,
        'experiences': experiences,
        'educations': educations,
        'portfolios': portfolios,
    }
    
    return render(request, 'personal_resume.html', context)
def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "رمز عبور با تاییدیه مطابقت ندارد.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "نام کاربری قبلاً استفاده شده است.")
            return redirect("register")

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        messages.success(request, "ثبت‌نام با موفقیت انجام شد!")
        return redirect("dashboard")
    return render(request, "register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "ورود موفقیت‌آمیز بود!")
            return redirect("dashboard")
        else:
            messages.error(request, "نام کاربری یا رمز عبور اشتباه است.")
            return redirect("login")
    return render(request, "login.html")

def logout_view(request):
    logout(request)
    messages.success(request, "با موفقیت خارج شدید!")
    return redirect("home")

def dashboard_view(request):
    if not request.user.is_authenticated:
        messages.error(request, "ابتدا وارد حساب کاربری شوید.")
        return redirect("login")

    profile, created = Profile.objects.get_or_create(user=request.user)  # اطمینان از ایجاد پروفایل در صورت عدم وجود
    skills = Skill.objects.filter(user=request.user)
    experiences = Experience.objects.filter(user=request.user)
    educations = Education.objects.filter(user=request.user)
    portfolios = Portfolio.objects.filter(user=request.user)
    

    # فرم‌های ویرایش
    if request.method == 'POST':
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "پروفایل با موفقیت به‌روزرسانی شد!")

    else:
        profile_form = ProfileEditForm(instance=profile)

    context = {
        'profile': profile,
        'skills': skills,
        'experiences': experiences,
        'educations': educations,
        'portfolios': portfolios,
        'profile_form': profile_form,
    }
    return render(request, "dashboard.html", context)


def resume_view(request, username):
    user = User.objects.filter(username=username).first()
    if not user:
        messages.error(request, "کاربر مورد نظر یافت نشد.")
        return redirect('home')

    profile = Profile.objects.filter(user=user).first()
    skills = Skill.objects.filter(user=user)
    experiences = Experience.objects.filter(user=user)
    educations = Education.objects.filter(user=user)
    portfolios = Portfolio.objects.filter(user=user)

    context = {
        'profile': profile,
        'skills': skills,
        'experiences': experiences,
        'educations': educations,
        'portfolios': portfolios,
    }
    return render(request, "resume.html", context)


@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "پروفایل با موفقیت به‌روزرسانی شد.")
            return redirect('dashboard')
    else:
        form = ProfileEditForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})

@login_required
def manage_skills(request):
    skills = request.user.skills.all()

    if request.method == 'POST':
        if 'add' in request.POST:
            form = SkillForm(request.POST)
            if form.is_valid():
                skill = form.save(commit=False)
                skill.user = request.user
                skill.save()
                messages.success(request, "مهارت جدید با موفقیت اضافه شد.")
        elif 'delete' in request.POST:
            skill_id = request.POST.get('delete')
            Skill.objects.filter(id=skill_id).delete()
            messages.success(request, "مهارت با موفقیت حذف شد.")

    skills = request.user.skills.all()
    return render(request, 'manage_skills.html', {'skills': skills})

@login_required
def manage_experiences(request):
    experiences = request.user.experiences.all()

    if request.method == 'POST':
        if 'add' in request.POST:
            form = ExperienceForm(request.POST)
            if form.is_valid():
                experience = form.save(commit=False)
                experience.user = request.user
                experience.save()
                messages.success(request, "تجربه کاری جدید اضافه شد.")
        elif 'delete' in request.POST:
            experience_id = request.POST.get('delete')
            Experience.objects.filter(id=experience_id).delete()
            messages.success(request, "تجربه کاری حذف شد.")

    experiences = request.user.experiences.all()
    return render(request, 'manage_experiences.html', {'experiences': experiences})

@login_required
def manage_educations(request):
    educations = request.user.educations.all()

    if request.method == 'POST':
        if 'add' in request.POST:
            form = EducationForm(request.POST)
            if form.is_valid():
                education = form.save(commit=False)
                education.user = request.user
                education.save()
                messages.success(request, "سوابق تحصیلی جدید اضافه شد.")
        elif 'delete' in request.POST:
            education_id = request.POST.get('delete')
            Education.objects.filter(id=education_id).delete()
            messages.success(request, "مدرک تحصیلی حذف شد.")

    educations = request.user.educations.all()
    return render(request, 'manage_educations.html', {'educations': educations})
@login_required
def manage_portfolios(request):
    portfolios = request.user.portfolios.all()

    if request.method == 'POST':
        if 'add' in request.POST:
            form = PortfolioForm(request.POST, request.FILES)
            if form.is_valid():
                portfolio = form.save(commit=False)
                portfolio.user = request.user
                portfolio.save()
                messages.success(request, "نمونه‌کار جدید اضافه شد.")
        elif 'delete' in request.POST:
            portfolio_id = request.POST.get('delete')
            Portfolio.objects.filter(id=portfolio_id).delete()
            messages.success(request, "نمونه‌کار حذف شد.")

    portfolios = request.user.portfolios.all()
    return render(request, 'manage_portfolios.html', {'portfolios': portfolios})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "با موفقیت از حساب خارج شدید.")
    return redirect('home')

def add_skill(request):
    if request.method == 'POST':
        skill_name = request.POST.get('skill_name')
        skill_level = request.POST.get('skill_level')
        
        # ذخیره مهارت جدید
        Skill.objects.create(name=skill_name, level=skill_level, user=request.user)

        return redirect('dashboard')  # یا صفحه‌ای که می‌خواهید کاربر بعد از افزودن مهارت به آن هدایت شود.
    
    return render(request, 'dashboard.html')

def add_experience(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        position = request.POST.get('position')
        description = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date', None)
        
        # ذخیره تجربه کاری جدید
        Experience.objects.create(
            user=request.user,
            company_name=company_name,
            position=position,
            description=description,
            start_date=start_date,
            end_date=end_date
        )

        return redirect('dashboard')  # هدایت به داشبورد بعد از افزودن تجربه کاری
    
    return render(request, 'dashboard.html')  # می‌توانید این بخش را به صفحه دیگری هم تغییر دهید

def add_education(request):
    if request.method == 'POST':
        institution_name = request.POST.get('institution_name')
        degree = request.POST.get('degree')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date', None)
        
        # ذخیره سوابق تحصیلی جدید
        Education.objects.create(
            user=request.user,
            institution_name=institution_name,
            degree=degree,
            start_date=start_date,
            end_date=end_date
        )

        return redirect('dashboard')  # هدایت به داشبورد بعد از افزودن سوابق تحصیلی
    
    return render(request, 'dashboard.html') 

@login_required
def add_portfolio(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST, request.FILES)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user = request.user  # تنظیم کاربر به نمونه‌کار
            portfolio.save()  # ذخیره نمونه‌کار
            messages.success(request, "نمونه‌کار جدید با موفقیت اضافه شد.")
            return redirect('dashboard')  # هدایت به داشبورد بعد از افزودن نمونه‌کار
    else:
        form = PortfolioForm()

    return render(request, 'add_portfolio.html', {'form': form})

@login_required
def edit_skill(request, id):
    skill = get_object_or_404(Skill, id=id, user=request.user)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "مهارت با موفقیت به‌روزرسانی شد!")
            return redirect('dashboard')
    else:
        form = SkillForm(instance=skill)

    return render(request, 'edit_skill.html', {'form': form, 'skill': skill})

from django.contrib.auth.decorators import login_required

@login_required
def delete_skill(request, id):
    skill = get_object_or_404(Skill, id=id, user=request.user)
    skill.delete()
    messages.success(request, "مهارت با موفقیت حذف شد!")
    return redirect('dashboard')

@login_required
def edit_experience(request, id):
    experience = get_object_or_404(Experience, id=id, user=request.user)

    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            messages.success(request, "تجربه کاری با موفقیت به‌روزرسانی شد!")
            return redirect('dashboard')
    else:
        form = ExperienceForm(instance=experience)

    return render(request, 'edit_experience.html', {'form': form})

@login_required
def delete_experience(request, id):
    experience = get_object_or_404(Experience, id=id, user=request.user)
    experience.delete()
    messages.success(request, "تجربه کاری با موفقیت حذف شد!")
    return redirect('dashboard')

@login_required
def edit_education(request, id):
    education = get_object_or_404(Education, id=id, user=request.user)

    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            messages.success(request, "سابقه تحصیلی با موفقیت به‌روزرسانی شد!")
            return redirect('dashboard')
    else:
        form = EducationForm(instance=education)

    return render(request, 'edit_education.html', {'form': form})

@login_required
def delete_education(request, id):
    education = get_object_or_404(Education, id=id, user=request.user)
    education.delete()
    messages.success(request, "سابقه تحصیلی با موفقیت حذف شد!")
    return redirect('dashboard')

def portfolio_list(request):
    portfolios = Portfolio.objects.all()
    return render(request, 'portfolio_list.html', {'portfolios': portfolios})

@login_required
def delete_portfolio(request, id):
    portfolio = get_object_or_404(Portfolio, id=id, user=request.user)
    portfolio.delete()
    messages.success(request, "نمونه‌کار با موفقیت حذف شد!")
    return redirect('dashboard')
