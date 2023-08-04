import bcrypt
import random
import smtplib
import string
from django.contrib import messages
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from project.settings import admin_role
from .login_view import login_required
from .models import AreaVO, LoginVO, UserVO


def user_load_user(request):
    try:
        area_vo_list = AreaVO.objects.all()
        return render(request, 'user/addUser.html',
                      context={'area_vo_list': area_vo_list})
    except Exception as ex:
        print("user_load_user route exception occured>>>>>>>>>>", ex)
        return render(request, 'user/viewError.html', context={'message': ex})


def user_insert_user(request):
    try:
        login_username = request.POST.get('loginUsername')
        user_firstname = request.POST.get('userFirstname')
        user_lastname = request.POST.get('userLastname')
        user_address = request.POST.get('userAddress')
        user_gender = request.POST.get('userGender')
        user_area_id = request.POST.get('userArea')
        hobbies_list = request.POST.getlist('userHobby')
        user_hobby = ",".join(hobbies_list)

        login_vo_list = LoginVO.objects.all()
        login_username_list = [model_to_dict(i)['login_username'] for i in
                               login_vo_list]

        if login_username in login_username_list:
            error_message = "The username is already exists !"
            messages.info(request, error_message)
            return redirect('/user/load_user')

        login_password = ''.join(
            (random.choice(string.ascii_letters + string.digits)) for x in
            range(8))
        salt = bcrypt.gensalt(rounds=12)
        hashed_login_password = bcrypt.hashpw(login_password.encode("utf-8"),
                                              salt)

        sender = "noreplypython@yahoo.com"
        receiver = login_username
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = "YOUR SYSTEM GENERATED LOGIN PASSWORD IS:"
        msg.attach(MIMEText(login_password, 'plain'))

        server = smtplib.SMTP('smtp.mail.yahoo.com', 587)
        server.starttls()
        server.login(sender, "dbzivjinwbndvvey")
        text = msg.as_string()
        server.sendmail(sender, receiver, text)
        server.quit()

        login_vo = LoginVO()
        login_vo.login_username = login_username
        login_vo.login_password = hashed_login_password.decode("utf-8")
        login_vo.login_role = "user"
        login_vo.login_status = True
        login_vo.save()

        area_vo = AreaVO.objects.get(area_id=user_area_id)

        user_vo = UserVO()
        user_vo.user_firstname = user_firstname
        user_vo.user_lastname = user_lastname
        user_vo.user_gender = user_gender
        user_vo.user_address = user_address
        user_vo.user_hobby = user_hobby
        user_vo.user_area_vo = area_vo
        user_vo.user_login_vo = login_vo
        user_vo.save()
        return redirect("/")
    except Exception as ex:
        print("user_insert_user route exception occured>>>>>>>>>>", ex)
        return render(request, 'user/viewError.html', context={'message': ex})


@login_required(admin_role)
def admin_view_user(request):
    try:
        user_vo_list = UserVO.objects.select_related(
            'user_login_vo').select_related('user_area_vo').all()
        return render(request, 'admin/viewUser.html',
                      context={'user_vo_list': user_vo_list})

    except Exception as ex:
        print("admin_view_user route exception occured>>>>>>>>>>", ex)
        return render(request, 'admin/viewError.html', context={'message': ex})
