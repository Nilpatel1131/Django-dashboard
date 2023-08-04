from django.shortcuts import render, redirect
from .login_view import login_required
from .models import AreaVO
from project.settings import admin_role

@login_required(admin_role)
def admin_load_area(request):
    try:
        return render(request, "admin/addArea.html")

    except Exception as ex:
        print("in admin_load_area function exception occured>>>>>", ex)
        return render(request, 'admin/viewError.html', context={'message': ex})

@login_required('admin')
def admin_insert_area(request):
    try:
        area_vo = AreaVO()
        area_vo.area_name = request.POST.get('areaName')
        area_vo.area_pincode = request.POST.get('areaPincode')
        area_vo.save()
        return redirect("/admin/view_area")

    except Exception as ex:
        print("in admin_insert_area function exception occured>>>>>", ex)
        return render(request, 'admin/viewError.html', context={'message': ex})

@login_required('admin')
def admin_view_area(request):
    try:
        area_vo_list = AreaVO.objects.all()
        return render(request, 'admin/viewArea.html',
                      context={'area_vo_list': area_vo_list})

    except Exception as ex:
        print("in admin_view_category function exception occured>>>>>", ex)
        return render(request, 'admin/viewError.html', context={'message': ex})

@login_required('admin')
def admin_delete_area(request):
    try:
        area_id = request.GET.get('areaId')
        area_vo = AreaVO.objects.get(area_id=area_id)
        area_vo.delete()
        return redirect("/admin/view_area")
    except Exception as ex:
        print("in admin_delete_area function exception occured>>>>>", ex)
        return render(request, 'admin/viewError.html', context={'message': ex})

@login_required('admin')
def admin_edit_area(request):
    try:
        area_id = request.GET.get('areaId')
        area_vo_list = AreaVO.objects.filter(area_id=area_id)
        return render(request, "admin/editArea.html",
                      context={'area_vo_list': area_vo_list})
    except Exception as ex:
        print("in admin_edit_area function exception occured>>>>>", ex)
        return render(request, 'admin/viewError.html', context={'message': ex})

@login_required('admin')
def admin_update_area(request):
    try:
        area_id = request.POST.get('areaId')
        area_name = request.POST.get('areaName')
        area_pincode = request.POST.get('areaPincode')

        area_vo = AreaVO.objects.get(area_id=area_id)
        area_vo.area_name = area_name
        area_vo.area_pincode = area_pincode
        area_vo.save()
        return redirect("/admin/view_area")

    except Exception as ex:
        print("in admin_update_category function exception occured>>>>>", ex)
        return render(request, 'admin/viewError.html', context={'message': ex})
