from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from Blog.models import Profile, Blog
import random
from django.utils import timezone
from django.contrib import messages

# Create your views here.
def home_view(request):
    blogs = Blog.objects.all()
    return render(request, 'home.html', {"blogs": blogs})

@login_required(login_url='login_url')
def profile_view(request):
    # Get the existing Profile for the current user, or create one
    # with a default fullname based on the username if it does not exist.
    profile, _ = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            'fullname': request.user.username,
        }
    )

    if request.method == 'POST':
        action = request.POST.get('action', '')

        if action == 'update_profile':
            fullname = request.POST.get('fullname', '').strip()
            profile_pic = request.FILES.get('profile_pic')

            if not fullname:
                messages.error(request, "Full name is required!")
                return redirect('profile_url')
            if len(fullname) < 5:
                messages.error(request, "Full name must consist of at least 5 characters!")
                return redirect('profile_url')
            if not fullname.replace(' ', '').isalpha():
                messages.error(request, "Full name should only contain letters!")
                return redirect('profile_url')

            profile.fullname = fullname
            if profile_pic:
                profile.profile_pic = profile_pic
            profile.updated_at = timezone.now()
            profile.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile_url')

        if action == 'create_blog':
            title = request.POST.get('title', '').strip()
            description = request.POST.get('description', '').strip()
            blog_poster = request.FILES.get('blog_poster')

            if not title:
                messages.error(request, "Title is required!")
                return redirect('profile_url')
            if len(title) > 100:
                messages.error(request, "Title cannot exceed 100 characters!")
                return redirect('profile_url')
            if len(title) < 40:
                messages.error(request, "Title must be at least 40 characters!")
                return redirect('profile_url')
            if not description:
                messages.error(request, "Description is required!")
                return redirect('profile_url')
            if len(description) > 1000:
                messages.error(request, "Description cannot exceed 1000 characters!")
                return redirect('profile_url')
            if len(description) < 400:
                messages.error(request, "Description must be at least 400 characters!")
                return redirect('profile_url')
            if not blog_poster:
                messages.error(request, "Blog poster image is required!")
                return redirect('profile_url')

            Blog.objects.create(
                user=request.user,
                title=title,
                description=description,
                blog_poster=blog_poster,
                created_at=timezone.now()
            )
            messages.success(request, 'Blog created successfully!')
            return redirect('profile_url')

        if action == 'update_blog':
            blog_id = request.POST.get('blog_id')
            blog = Blog.objects.filter(id=blog_id, user=request.user).first()

            if not blog:
                messages.error(request, "Blog not found!")
                return redirect('profile_url')

            title = request.POST.get('title', '').strip()
            description = request.POST.get('description', '').strip()
            blog_poster = request.FILES.get('blog_poster')

            if not title:
                messages.error(request, "Title is required!")
                return redirect('profile_url')
            if len(title) > 100:
                messages.error(request, "Title cannot exceed 100 characters!")
                return redirect('profile_url')
            if len(title) < 40:
                messages.error(request, "Title must be at least 40 characters!")
                return redirect('profile_url')
            if not description:
                messages.error(request, "Description is required!")
                return redirect('profile_url')
            if len(description) > 1000:
                messages.error(request, "Description cannot exceed 1000 characters!")
                return redirect('profile_url')
            if len(description) < 400:
                messages.error(request, "Description must be at least 400 characters!")
                return redirect('profile_url')

            blog.title = title
            blog.description = description
            if blog_poster:
                blog.blog_poster = blog_poster
            blog.updated_at = timezone.now()
            blog.save()
            messages.success(request, 'Blog updated successfully!')
            return redirect('profile_url')

    blogs = Blog.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'profile.html', {'profile': profile, 'blogs': blogs})


@login_required(login_url='login_url')
def reset_password_view(request):
    if request.method != 'POST':
        return redirect('profile_url')

    old_password = request.POST.get('old_password', '').strip()
    new_password = request.POST.get('new_password', '').strip()
    confirm_password = request.POST.get('confirm_password', '').strip()

    if not (old_password and new_password and confirm_password):
        messages.error(request, "All password fields are required!")
        return redirect('profile_url')

    if not request.user.check_password(old_password):
        messages.error(request, "Current password is incorrect!")
        return redirect('profile_url')

    if len(new_password) < 8:
        messages.error(request, "New password must be at least 8 characters!")
        return redirect('profile_url')

    if new_password != confirm_password:
        messages.error(request, "New password and confirm password do not match!")
        return redirect('profile_url')

    if old_password == new_password:
        messages.error(request, "New password must be different from the current password!")
        return redirect('profile_url')

    request.user.set_password(new_password)
    request.user.save()
    # Keeps the user logged in after changing their password hash,
    # otherwise Django would invalidate the current session.
    update_session_auth_hash(request, request.user)

    messages.success(request, "Password reset successfully!")
    return redirect('profile_url')

def forgetpassword(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        otp = request.POST.get('otp', '').strip()
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if otp and new_password and confirm_password:
            if not email:
                messages.error(request, "Email is required!")
                return render(request, 'forget_password.html')

            session_otp = request.session.get('forget_password_otp')
            session_user_id = request.session.get('forget_password_user_id')

            if not session_otp or not session_user_id:
                messages.error(request, "No OTP request found. Please request a new OTP.")
                return render(request, 'forget_password.html')

            if otp != str(session_otp):
                messages.error(request, "OTP is incorrect!")
                return render(request, 'forget_password.html')

            if len(new_password) < 8:
                messages.error(request, "New password must be at least 8 characters!")
                return render(request, 'forget_password.html')

            if new_password != confirm_password:
                messages.error(request, "New password and confirm password do not match!")
                return render(request, 'forget_password.html')

            try:
                user = User.objects.get(id=session_user_id)
            except User.DoesNotExist:
                messages.error(request, "User not found for this request.")
                return render(request, 'forget_password.html')

            user.set_password(new_password)
            user.save()
            request.session.pop('forget_password_otp', None)
            request.session.pop('forget_password_user_id', None)

            messages.success(request, "Password reset successfully! You can now log in.")
            return redirect('login_url')

        if not email:
            messages.error(request, "Email is required!")
            return render(request, 'forget_password.html')

        user = User.objects.filter(email=email).first()
        if not user:
            messages.error(request, "No user found with that email!")
            return render(request, 'forget_password.html')

        otp_value = random.randint(100000, 999999)
        request.session['forget_password_otp'] = str(otp_value)
        request.session['forget_password_user_id'] = user.id
        print(f"Password reset OTP for {user.username} ({email}): {otp_value}")

        messages.success(request, "OTP generated and shown in terminal. Enter it with your new password.")
        return render(request, 'forget_password.html')

    return render(request, 'forget_password.html')

@login_required(login_url='login_url')
def blog_create_view(request):
    if request.method == 'POST':
        title = request.POST.get('blog_title', '').strip()
        description = request.POST.get('blog_content', '').strip()
        blog_poster = request.FILES.get('blog_image')

        if not title:
            messages.error(request, "Title is required!")
            return redirect("blog_create_url")

        if len(title) > 100:
            messages.error(request, "Title cannot exceed 100 characters!")
            return redirect("blog_create_url")

        if not len(title) > 40:
            messages.error(request, "Title must be atleast 40  characters!")
            return redirect("blog_create_url")
        if not description:
            messages.error(request, "Description is required!")
            return redirect("blog_create_url")

        if len(description) > 1000:
            messages.error(request, "Description cannot exceed 1000 characters!")
            return redirect("blog_create_url")
        if not len(description) > 400:
            messages.error(request, "Description must be atleast 400  characters!!")
            return redirect("blog_create_url")

        if not blog_poster:
            messages.error(request, "Blog poster image is required!")
            return redirect("blog_create_url")

        blog=Blog.objects.create(
            user=request.user,
            title=title,
            description=description,
            blog_poster=blog_poster,
            created_at=timezone.now()
        )
        if blog is None:
            messages.error(request, "internal server error !")
            return redirect("blog_create_url")
        messages.success(request,'blog is created succedssfly!!')
        return redirect("home_url")

    return render(request, 'blog_create.html')

@login_required(login_url='login_url')
def blog_detail_view(request,id):
    try:
        blog = Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        messages.error(request, "Blog not found!")
        return redirect("home_url")

    
    can_delete = request.user.is_authenticated and blog.user == request.user

    return render(request, 'blog_detail.html',{'context':blog, 'can_delete': can_delete})


@login_required(login_url='login_url')
def blog_delete_view(request, id):
    try:
        blog = Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        messages.error(request, "Blog not found!")
        return redirect("home_url")
 
    if blog.user != request.user:
        messages.error(request, "You are not authorized to delete this blog!")
        return redirect("blog_detail_url", id=id)

    if request.method == 'POST':
        blog.delete()
        messages.success(request, "Blog deleted successfully.")
        return redirect("home_url")

   
    return render(request, 'blog_confirm_delete.html', {'context': blog})
@login_required(login_url='login_url')
def edit_view(request,id):
    try:
        blog = Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        messages.error(request, "Blog not found!")
        return redirect("home_url")
 
    if blog.user != request.user:
        messages.error(request, "You are not authorized to edit this blog!")
        return redirect("blog_detail_url", id=id)

    
    return redirect("edit_blog_url", id=id)


@login_required(login_url='login_url')
def edit_page_view(request, id):
    """Render the edit page for a blog post."""
    try:
        blog = Blog.objects.get(id=id)
    except Blog.DoesNotExist:
        messages.error(request, "Blog not found!")
        return redirect("home_url")

    if blog.user != request.user:
        messages.error(request, "You are not authorized to edit this blog!")
        return redirect("blog_detail_url", id=id)

    return render(request, 'editblog.html', {'context': blog})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not (username and password):
            messages.error(request, "Username & password should not be empty!")
            return redirect("login_url")

        if not username.strip().isalnum():
            messages.error(request, "Username must consists of alpha numeric characters!")
            return redirect("login_url")

        if len(password.strip()) < 8:
            messages.error(request, "Password must consists of at least 8 characters!")
            return redirect("login_url")

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password!")
            return redirect("login_url")

        login(request, user)
        return redirect("home_url")

    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        if fullname and len(fullname.strip()) < 5:
            messages.error(request, "Fullname must consists of atleast 5 characters!")
            return redirect("signup_url")

        if not fullname.strip().isalpha():
            messages.error(request, "Fullname should consists of only alphabets!")
            return redirect("signup_url")

        if email and len(email.strip()) < 10:
            messages.error(request, "Invalid Email length!")
            return redirect("signup_url")

        if username and len(username.strip()) < 5:
            messages.error(request, "Username must consists of at least 5 characters!")
            return redirect("signup_url")

        if not username.strip().isalnum():
            messages.error(request, "Username should be alphanumeric!")
            return redirect("signup_url")

        if password and len(password.strip()) < 8:
            messages.error(request, "Password must consists of at least 8 characters!")
            return redirect("signup_url")

        try:
            User.objects.get(username=username)
            messages.error(request, "User already exists!")
            return redirect("signup_url")
        except:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            Profile.objects.create(
                fullname=fullname,
                user=user
            )
            return redirect("login_url")
    return render(request, 'signup.html')

@login_required(login_url='login_url')
def logout_view(request):
    logout(request)
    return redirect("home_url")