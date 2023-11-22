from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
    reverse,
)
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from datetime import datetime


from .models import Student, Course, Category, Instructor, Order
from .forms import OrderForm, InterestForm, LoginForm

# Create your views here.


def set_test_cookie(request):
    # Set a test cookie
    response = HttpResponse("Setting test cookie")
    response.set_cookie("test_cookie", "test_value")
    return response


def check_test_cookie(request):
    # Check if the test cookie worked
    test_cookie = request.COOKIES.get("test_cookie")
    if test_cookie == "test_value":
        # Delete the test cookie
        response = HttpResponse("Test cookie worked. Deleting cookie.")
        response.delete_cookie("test_cookie")
        return response
    else:
        return HttpResponse("Test cookie not found.")


@login_required(login_url="/myappF23/login/")
def index(request):
    category_list = Category.objects.all().order_by("id")[:10]
    course_list = Course.objects.all().order_by("-price")[:5]
    order_list = Order.objects.all().order_by("-order_date")[:10]
    ins_list = Instructor.objects.all()[:5]

    last_login_info = request.session.get("last_login_info", None)
    if last_login_info:
        login_info = "Your last login was: " + last_login_info
    else:
        login_info = "Your last login was more than 5 minutes ago"

    user_visits = request.COOKIES.get("user_visits", 0)
    user_visits = int(user_visits) + 1
    response = render(
        request,
        "myapp/index.html",
        {
            "course_list": course_list,
            "category_list": category_list,
            "order_list": order_list,
            "ins_list": ins_list,
            "user_visits": user_visits,
            "login_info": login_info,
        },
    )
    response.set_cookie("user_visits", user_visits, max_age=10)
    return response


@login_required(login_url="/myappF23/login/")
def main_detail(request):
    category_list = Category.objects.all().order_by("id")[:10]
    ins_list = Instructor.objects.all()[:5]

    return render(
        request,
        "myapp/detail.html",
        {
            "category_list": category_list,
            "ins_list": ins_list,
        },
    )


@login_required(login_url="/myappF23/login/")
def about(request):
    return render(request, "myapp/about.html")


@login_required(login_url="/myappF23/login/")
def detail(request, category_no):
    category_name = get_object_or_404(Category, pk=category_no)
    course_list = Course.objects.filter(categories=category_no).order_by("id")

    return render(request, "myapp/category_detail.html", {"course_list": course_list})


@login_required(login_url="/myappF23/login/")
def instructor_detail(request, instructor_no):
    instructor_name = get_object_or_404(Instructor, pk=instructor_no)
    course_list = Course.objects.filter(instructor=instructor_no)

    stu_course_lst = []

    for course in course_list:
        students = []
        for st in course.students.all():
            students.append(st)

        stu_course = {"name": course.title, "students": tuple(students)}

        stu_course_lst.append(stu_course)

    # print(stu_course_lst)

    return render(
        request,
        "myapp/ins_detail.html",
        {"instructor_name": instructor_name, "course_list": stu_course_lst},
    )


def students_by_ins(request, ins_no):
    ins = get_object_or_404(Instructor, pk=ins_no)
    students = ins.student.all()

    return render(
        request,
        "myapp/stu_by_ins.html",
        {"st_list": students},
    )


@login_required(login_url="/myappF23/login/")
def courses(request):
    course_list = Course.objects.all().order_by("-price")
    return render(request, "myapp/courses.html", {"course_list": course_list})


@login_required(login_url="/myappF23/login/")
def place_order(request):
    msg = ""
    course_list = Course.objects.all()
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)

            # set order status to confirmed
            order.order_status = 0

            # set order price to course price
            order.order_price = order.course.price

            # Check if the ordered level exceeds the number of levels for the course
            if order.levels > order.course.level:
                msg = "You exceeded the number of levels for this course."
                return render(request, "myapp/order_response.html", {"msg": msg})

            msg = "Your course has been ordered successfully."

            # Check if the course price is greater than $150.00
            if order.course.price > 150.00:
                order.discount()

            order.save()

        else:
            msg = "You exceeded the number of levels for this course."
            return render(request, "myapp/order_response.html", {"msg": msg})

    else:
        form = OrderForm()

    return render(
        request,
        "myapp/place_order.html",
        {"form": form, "msg": msg, "course_list": course_list},
    )


@login_required(login_url="/myappF23/login/")
def courses_ordered(request, studentId):
    order_list = Order.objects.filter(student=studentId)

    return render(request, "myapp/ordered.html", {"order_list": order_list})


@login_required(login_url="/myappF23/login/")
def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method == "POST":
        form = InterestForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["interested"] == "1":
                # Increment interested field for the course
                course.interested += 1
                course.save()

                comment = form.cleaned_data["comments"]

                # Redirect to the main index page
                # return redirect("index")
                url = "list/?data=" + comment
                return redirect(url)
    else:
        form = InterestForm()

    return render(
        request,
        "myapp/course-detail.html",
        {
            "course": course,
            "form": form,
        },
    )


def list(request):
    comment = request.GET.get("data", "")

    c = Course.objects.get(title=comment)
    ins = c.instructor

    return render(request, "myapp/list.html", {"course": c, "ins": ins})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)

            if user:
                if user.is_active:
                    login(request, user)

                    # Generate the date and time of the current login
                    current_login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Store this value as a session parameter (last_login_info)
                    request.session["last_login_info"] = current_login_time

                    # # Set the session expiry to 5 minutes
                    # request.session.set_expiry(300)

                    return HttpResponseRedirect(reverse("index"))
                else:
                    return HttpResponse("Your account is disabled.")
            else:
                return HttpResponse("Invalid login details.")
        else:
            form = LoginForm()
    else:
        form = LoginForm()

    return render(request, "myapp/login.html", {"form": form})


@login_required(login_url="/myappF23/login/")
def user_logout(request):
    # Log out the current user by deleting the request session
    del request.session["last_login_info"]

    # Since SESSION_EXPIRE_AT_BROWSER_CLOSE is True, we don't need to set session expiry here.
    # # Make the user’s session cookies expire when the user’s web browser is closed
    # request.session.set_expiry(0)

    logout(request)

    return HttpResponseRedirect(reverse("user_login"))


@login_required(login_url="/myappF23/login/")
def myaccount(request):
    user = request.user
    if hasattr(user, "student"):
        # User is a student
        student = user.student
        courses_ordered = student.courses_ordered.all()
        courses_interested = student.courses_interested.all()
        context = {
            "full_name": user.get_full_name(),
            "courses_ordered": courses_ordered,
            "courses_interested": courses_interested,
        }
        return render(request, "myappF23/myaccount.html", context)
    else:
        # User is not a student
        return HttpResponse("You are not a registered student!")
