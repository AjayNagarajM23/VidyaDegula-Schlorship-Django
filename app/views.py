from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Annoucement


# Create your views here.

def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        fname = request.POST['fname']
        lname = request.POST['lname']

        if User.objects.filter(username=username):
            messages.error(request, "Username Already Exists")
            return redirect('signup')
        if User.objects.filter(email=email):
            messages.error(request, "Email Already Exists")
            return redirect('signup')

        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()
        messages.success(request, "Your account has successfully Created, Please Login To Continue")

        return render(request, 'signin.html')

    return render(request, 'signup.html')


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, username + " Successfully Logged In")
            return redirect('index')
        else:
            messages.error(request, "Bad credentials ( Wrong Username Or Password )")
            return redirect('signin')

    return render(request, 'signin.html')


def signout(request):
    logout(request)
    messages.success(request, " Logged out Successfully ")
    return redirect('index')


def conus(request):
    if request.method == 'POST':
        name = request.POST['conName']
        mail = request.POST['email']
        query = request.POST['query']
        phno = request.POST['phno']

        subject = name + " : " + mail
        message = query + "   :    " + phno
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['ajaynagarajm23@gmail.com']
        send_mail(subject, message, email_from, recipient_list)
        messages.success(request, "Mail sent Successfully")
        return redirect('index')

    return render(request, 'conus.html')


def afs(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        dob = request.POST['dob']
        mail = request.POST['mail']
        phno = request.POST['phno']
        gender = request.POST['Gender']
        address = request.POST['address']
        city = request.POST['city']
        pincode = request.POST['code']
        state = request.POST['state']
        country = request.POST['country']
        per10 = request.POST['per10']
        per12 = request.POST['per12']
        bach = request.POST['bach']
        course = request.POST['crs']

        html_content = render_to_string('eTemplate.html',
                                        {'fname': fname,
                                         'lname': lname,
                                         'dob': dob,
                                         'mail': mail,
                                         'phno': phno,
                                         'gender': gender,
                                         'address': address,
                                         'city': city,
                                         'pincode': pincode,
                                         'state': state,
                                         'country': country,
                                         'per10': per10,
                                         'per12': per12,
                                         'bach': bach,
                                         'course': course})
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            "Application For Scholarship Has Been Submitted",
            text_content,
            settings.EMAIL_HOST_USER,
            ['ajaynagarajm23@gmail.com', mail]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        messages.success(request, "Your Application For Scholarship has been Submitted")
        return redirect('afs')

    return render(request, 'apply.html')


def forms(request):
    return render(request, 'form.html')


def ans(request):
    announcement = Annoucement.objects.all()
    return render(request, 'ans.html', {'data':announcement})


def enterans(request):
    if request.method == "POST":
        annou = request.POST['announcement']
        img = request.FILES["photo"]
        desc = request.POST['desc']
        ans_info = Annoucement(title=annou, img=img, description=desc)
        ans_info.save()
        messages.success(request, "New Announcement Added")
    return render(request, 'enterans.html')
