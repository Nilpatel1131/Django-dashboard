from django.shortcuts import render, redirect

from project.settings import admin_role
from .login_view import login_required
from .models import CategoryVO, SubCategoryVO


@login_required(admin_role)
def admin_load_subcategory(request):
    try:
        category_vo_list = CategoryVO.objects.all()
        return render(request, "admin/addSubCategory.html",
                      context={'category_vo_list': category_vo_list})

    except Exception as ex:
        print("in admin_load_subcategory function exception occured>>>>>", ex)
        return render(request, 'admin/viewError.html', context={'message': ex})


@login_required(admin_role)
def admin_insert_subcategory(request):
    try:
        subcategory_vo = SubCategoryVO()
        subcategory_vo.subcategory_name = request.POST.get(
            "subCategoryName")
        subcategory_vo.subcategory_description = request.POST.get(
            "subCategoryDescription")
        subcategory_category_id = request.POST.get("subCategoryCategoryId")
        category_vo = CategoryVO.objects.get(
            category_id=subcategory_category_id)
        subcategory_vo.subcategory_category_vo = category_vo
        subcategory_vo.save()
        return admin_view_subcategory(request)

    except Exception as ex:
        print("in admin_insert_subcategory function exception occured>>>>>",
              ex)
        return render(request, 'admin/viewError.html', context={'message': ex})


@login_required(admin_role)
def admin_view_subcategory(request):
    try:
        subcategory_vo_list = SubCategoryVO.objects.select_related(
            'subcategory_category_vo').all()
        return render(request, "admin/viewSubCategory.html",
                      context={'subcategory_vo_list': subcategory_vo_list})

    except Exception as ex:
        print("in admin_insert_subcategory function exception occured>>>>>",
              ex)
        return render(request, 'admin/viewError.html', context={'message': ex})


@login_required(admin_role)
def admin_delete_subcategory(request):
    try:
        subcategory_id = request.GET.get('subcategoryId')
        subcategory_vo = SubCategoryVO.objects.get(
            subcategory_id=subcategory_id)
        subcategory_vo.delete()
        return redirect('/admin/view_subcategory')

    except Exception as ex:
        print("in admin_delete_subcategory function exception occured>>>>>",
              ex)
        return render(request, 'admin/viewError.html', context={'message': ex})


@login_required(admin_role)
def admin_edit_subcategory(request):
    try:
        subcategory_id = request.GET.get('subCategoryId')
        subcategory_vo_list = SubCategoryVO.objects.filter(
            subcategory_id=subcategory_id)
        category_vo_list = CategoryVO.objects.all()
        context = {"subcategory_vo_list": subcategory_vo_list,
                   "category_vo_list": category_vo_list}
        return render(request, "admin/editSubCategory.html", context)

    except Exception as ex:
        print("in admin_edit_subcategory function exception occured>>>>>", ex)
        return render(request, 'admin/viewError.html', context={'message': ex})


@login_required(admin_role)
def admin_update_subcategory(request):
    try:
        subcategory_id = request.POST.get('subCategoryId')
        subcategory_name = request.POST.get("subCategoryName")
        subcategory_description = request.POST.get(
            "subCategoryDescription")
        subcategory_category_id = request.POST.get("subCategoryCategoryId")

        subcategory_vo = SubCategoryVO()

        category_vo = CategoryVO.objects.get(
            category_id=subcategory_category_id)
        subcategory_vo.subcategory_id = subcategory_id
        subcategory_vo.subcategory_name = subcategory_name
        subcategory_vo.subcategory_description = subcategory_description
        subcategory_vo.subcategory_category_vo = category_vo
        subcategory_vo.save()
        return redirect(admin_view_subcategory)

    except Exception as ex:
        print("in admin_update_category function exception occured>>>>>", ex)
        return render(request, 'admin/viewError.html', context={'message': ex})
