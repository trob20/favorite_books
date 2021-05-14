from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
    return render(request, "index.html")


def register(request):
    if(request.method=="POST"): 
        errors = User.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")

        password_input = request.POST["password"]
        pw_hash = bcrypt.hashpw(password_input.encode(), bcrypt.gensalt()).decode()
        print(pw_hash)
        
        user = User.objects.create(
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["email"],
            password=pw_hash
        )
        messages.success(request, "Registration complete! Please log in.")
    return redirect("/")


def login(request):
    if(request.method=="POST"): 
        email = request.POST["email"]
        password_input = request.POST["password"]

        user = User.objects.filter(email=email)
        if not user:
            messages.error(request, "Invalid credentials")
            return redirect ("/")

        logged_in_user = user[0]

        if bcrypt.checkpw(password_input.encode(), logged_in_user.password.encode()):
            request.session["u_id"] = logged_in_user.id
            return redirect("/books")
        else:
            messages.error(request, "Invalid credentials")
            return redirect ("/")
    return redirect ("/")


def logout(request):
    if(request.method=="POST"): 
        del request.session["u_id"]
        request.session.clear()
    return redirect ("/")


def dashboard(request):
    sessionTest = request.session.get("u_id", "no u_id")
    if sessionTest == "no u_id": 
        return redirect ("/")
    u_id = request.session["u_id"]
    user = User.objects.get(id=u_id)
    
    context = {
        "books": Book.objects.all(),
        "first_name": user.first_name,
        "u_id": u_id
    }
    return render(request, "dashboard.html", context)


def add_book(request):
    if(request.method=="POST"):
        user = User.objects.get(id=request.session["u_id"])

        book = Book.objects.create(title=request.POST["title"], desc=request.POST["desc"], uploaded_by=user)
        book.favorite.add(user)
        book.save()

        return redirect ("/books")
    return redirect ("/")


def display_all(request, b_id):
    sessionTest = request.session.get('u_id', 'no u_id')
    if sessionTest == 'no u_id': 
        return redirect ("/")
    
    u_id = request.session["u_id"]
    user = User.objects.get(id=u_id)

    if User.objects.filter(favorites__id__contains=b_id).count() > 0:
        favorite = True
    else:
        favorite = False

    context= {
        "book": Book.objects.get(id=b_id),
        "favorite": favorite,
        "first_name": user.first_name,
        "u_id": u_id
    }
    return render(request, "edit_display.html", context)


def display_one(request, u_id):
    sessionTest = request.session.get('u_id', 'no u_id')
    if sessionTest == 'no u_id': 
        return redirect ("/")
    
    user = User.objects.get(id=u_id)

    favorite_books = Book.objects.filter(favorite__id__contains=u_id)

    context= {
        "favorite_books": favorite_books,
        "first_name": user.first_name,
        "u_id": u_id
    }
    return render(request, "favorites.html", context)


def update(request, b_id):
    if(request.method=="POST"):
        errors = Book.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect ('/books/'+ str(b_id))

        book = Book.objects.get(id=b_id)
        user = User.objects.get(id=request.session["u_id"])

        book.title=request.POST['title']
        book.desc=request.POST['desc']
        book.uploaded_by=user
        book.save()
        return redirect ('/books/'+ str(b_id))
    return redirect ('/')


def delete(request, b_id):
    if(request.method=="POST"): 
        book = Book.objects.get(id=b_id)
        book.delete()
        return redirect ('/books')
    return redirect ('/')


def favor(request, b_id):
    if(request.method=="POST"):
        book = Book.objects.get(id=b_id)
        user = User.objects.get(id=request.session["u_id"])

        book.favorite.add(user)
        book.save()
    return redirect ('/books/'+ str(b_id))


def unfavor(request, b_id):
    if(request.method=="POST"):
        book = Book.objects.get(id=b_id)
        user = User.objects.get(id=request.session["u_id"])

        book.favorite.remove(user)
        book.save()
    return redirect ('/books/'+ str(b_id))

