from django.urls import path, include
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path("", lambda request: redirect("login/"), name="redirect_to_login"),
    path("login/", views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
    path("myaccount/", views.myaccount, name="myaccount"),
    path("course-detail/list/", views.list, name="list"),
    path("home/", views.index, name="index"),
    path("stu_by_ins/<int:ins_no>", views.students_by_ins, name="students_by_ins"),
    path("<int:category_no>", views.detail, name="category_detail"),
    path("about/", views.about, name="about"),
    path("detail/", views.main_detail, name="detail"),
    path("course-detail/<int:course_id>", views.course_detail, name="course-detail"),
    path("courses/", views.courses, name="courses"),
    path("place-order/", views.place_order, name="place-order"),
    path(
        "courses_ordered/<int:studentId>",
        views.courses_ordered,
        name="courses_ordered",
    ),
    path("ins/<int:instructor_no>", views.instructor_detail, name="ins_detail"),
]
