import datetime
import jwt
from django.shortcuts import render, redirect

from base.models import LoginVO, FeedbackVO
from project.settings import SECRET_KEY
from project.settings import admin_role
from project.settings import user_role
from .login_view import login_required


@login_required(admin_role)
def admin_view_feedback(request):
    try:
        feedback_vo_list = FeedbackVO.objects.select_related(
            "feedback_login_vo").all()
        return render(request, 'admin/viewFeedback.html',
                      context={"feedback_vo_list": feedback_vo_list})

    except Exception as ex:
        print("admin_view_feedback route exception occured>>>>>>>>>>", ex)
        return render(request, 'admin/viewError.html', context={'message': ex})


@login_required(admin_role)
def admin_delete_feedback(request):
    try:
        feedback_id = request.GET.get('feedbackId')
        feedback_vo = FeedbackVO.objects.get(feedback_id=feedback_id)
        feedback_vo.delete()
        return redirect('/admin/view_feedback')

    except Exception as ex:
        print("admin_delete_feedback route exception occured>>>>>>>>>>", ex)
        return render(request, 'admin/viewError.html', context={'message': ex})


@login_required(user_role)
def user_insert_feedback(request):
    try:
        feedback_description = request.POST.get('feedbackDescription')
        feedback_rating = request.POST.get('feedbackRating')

        refreshtoken = request.COOKIES.get('refreshtoken')
        data = jwt.decode(refreshtoken, SECRET_KEY, 'HS256')

        login_vo = LoginVO.objects.filter(
            login_username=data['public_id']).first()

        feedback_vo = FeedbackVO()
        feedback_vo.feedback_description = feedback_description
        feedback_vo.feedback_rating = feedback_rating
        feedback_vo.feedback_datetime = datetime.datetime.now()
        feedback_vo.feedback_login_vo = login_vo
        feedback_vo.save()
        return redirect('/user/view_feedback')

    except Exception as ex:
        print("user_insert_feedback route exception occured>>>>>>>>>>", ex)
        return render(request, 'user/viewError.html', context={'message': ex})


@login_required(user_role)
def user_view_feedback(request):
    try:
        refreshtoken = request.COOKIES.get('refreshtoken')
        data = jwt.decode(refreshtoken, SECRET_KEY, 'HS256')

        login_vo = LoginVO.objects.filter(
            login_username=data['public_id']).first()

        feedback_vo_list = FeedbackVO.objects \
            .select_related('feedback_login_vo') \
            .filter(feedback_login_vo=login_vo) \
            .all()
        return render(request, "user/addFeedback.html",
                      context={"feedback_vo_list": feedback_vo_list})

    except Exception as ex:
        print("user_view_feedback route exception occured>>>>>>>>>>", ex)
        return render(request, 'user/viewError.html', context={'message': ex})
