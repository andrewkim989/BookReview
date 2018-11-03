from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt

from .models import *

def signin(request):
    request.session['login'] = 'logout'
    return render(request, "signin.html")

# Registration process

def reg_process(request):
    if request.method == 'POST':
        errors = User.objects.register_validate(request.POST)

        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = 'register')
            return redirect('/')
        else: 
            request.session['login'] = 'login'
            p = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name = request.POST['first_name'],
            last_name = request.POST['last_name'], email = request.POST['email'],
            password = p)
            
            messages.success(request, "You have successfully registered!", extra_tags = 'register')

            request.session['id'] = user.id
            return redirect('/books')

# Login process

def log_process(request):
    if request.method == 'POST':
        errors = User.objects.login_validate(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = 'login')
            return redirect('/')
        else: 
            request.session['login'] = 'login'
            user = User.objects.filter(email = request.POST['email'])[0]
            request.session['id'] = user.id

            messages.success(request, "You are logged in!", extra_tags = 'login')

            return redirect('/books')

# Homepage
def home(request):
    if request.session['login'] == 'logout':
        return redirect('/')
    else: 
        user = User.objects.get(id = request.session['id'])
        context = {
            "u": user,
            "reviews": Review.objects.all().order_by('-id')[:3],
            "books": Book.objects.all()
        }
        return render(request, "home.html", context)

def add(request):
    if request.session['login'] == 'logout':
        return redirect('/')
    else:
        context = {
            "authors": Author.objects.all()
        }
        return render(request, "new.html", context)

# Submitted new book

def add_process (request):
    if request.method == 'POST':
        errors = User.objects.review_validate(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = 'book')
            return redirect('/add')
        else: 
            user = User.objects.get(id = request.session['id'])
            if len(request.POST['add_name']) < 1:
                a = Author.objects.get(id = request.POST['name'])
                b = Book.objects.create(title = request.POST['title'], author = a, uploader = user)
                Review.objects.create(review = request.POST['review'], stars = int(request.POST['stars']), reviewer = user, book = b)
                return redirect('/books/' + str(b.id))
            else:
                a = Author.objects.create(name = request.POST['add_name'])
                b = Book.objects.create(title = request.POST['title'], author = a, uploader = user)
                Review.objects.create(review = request.POST['review'], stars = int(request.POST['stars']), reviewer = user, book = b)
            return redirect('/books/' + str(b.id))

def show(request, num):
    if request.session['login'] == 'logout':
        return redirect('/')
    else:
        b = Book.objects.get(id = num)
        context = {
            "book": b,
            "all_reviews": Review.objects.filter(book = b),
            "users": User.objects.all(),
        }
        return render (request, "books.html", context)

def add_review(request, num):
    if request.method == 'POST':
        errors = User.objects.small_review_validate(request.POST)
        b = Book.objects.get(id = num)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value, extra_tags = 'review')
            return redirect('/books/' + str(b.id))
        else:
            user = User.objects.get(id = request.session['id'])
            Review.objects.create(review = request.POST['review'], stars = int(request.POST['stars']), reviewer = user, book = b)
            return redirect ('/books/' + str(b.id))

def delete_review(request, num, num2):
    review = Review.objects.get(id = num2)
    review.delete()
    return redirect('/books/' + str(num))

def profile(request, num):
    if request.session['login'] == 'logout':
        return redirect('/')
    else:
        user = User.objects.get(id = num)
        book_list = set()
        reviews = Review.objects.filter(reviewer = user)
        for review in reviews: 
            book_list.add(review.book)
        context = {
            "user": user,
            "books": book_list
        }
        return render(request, "profile.html", context)

def clear(request):
    User.objects.all().delete()
    return redirect('/')

'''
purplesmart@eq.net
Twily123
http://127.0.0.1:8000/books/7

20cooler@eq.net
Dashie20
http://127.0.0.1:8000/books/8

partypony@eq.net
Pinkie30

'''