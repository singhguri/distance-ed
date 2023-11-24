from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import AuthUserManager


# Create your models here.
class Student(AbstractBaseUser, PermissionsMixin):
    STUDENT_STATUS_CHOICES = [
        ("ER", "Enrolled"),
        ("SP", "Suspended"),
        ("GD", "Graduated"),
    ]

    status = models.CharField(
        max_length=10, choices=STUDENT_STATUS_CHOICES, default="ER"
    )

    name = models.CharField(max_length=255, blank=True, default="")
    email = models.EmailField(default="", unique=True, blank=True, max_length=255)
    password = models.CharField(max_length=100)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    is_student = models.BooleanField(default=False)

    interested_courses = models.ManyToManyField(
        "Course", related_name="interested_students"
    )

    objects = AuthUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUERIES_FIELD = []

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name or self.email.split("@")[0]


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Instructor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField()
    student = models.ManyToManyField(Student)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Course(models.Model):
    LEVEL_CHOICES = [
        ("BE", "Beginner"),
        ("IN", "Intermediate"),
        ("AD", "Advanced"),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, default=None)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default="BE")
    level = models.PositiveIntegerField(default=0)
    interested = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class Order(models.Model):
    ORDER_CHOICES = [(0, "Order Confirmed"), (1, "Order Cancelled")]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    order_status = models.IntegerField(choices=ORDER_CHOICES, default=1)
    order_date = models.DateField()
    order_price = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    levels = models.PositiveIntegerField(default=0)

    def discount(self):
        print(self.order_price, self.order_status)
        if self.order_price > 0:
            new_order_price = self.order_price - ((10 * self.order_price) / 100)
            if new_order_price > 0:
                self.order_price = new_order_price

    def __str__(self):
        status_str = "Order Confirmed" if self.order_status == 0 else "Order Cancelled"
        return f"{self.student} : {self.course} - {status_str}"
