from django.shortcuts import render, redirect, HttpResponse
from .models import User, Friends
from django.contrib import messages
from django.db.models import Q
import bcrypt

# Create your views here.
def index(request):
    return redirect('/main')
def main(request):
    if 'user' in request.session:
        return redirect('/friends')
    return render(request, 'index.html')
def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['passwd'].encode(), logged_user.password.encode()):
            request.session['user'] = logged_user.email
            return redirect('/friends')
    messages.error(request, 'the email and password do not match')
    return redirect('/main')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash messagecopy
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/main')
    password = request.POST['passwd']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    User.objects.create(firstname=request.POST['firstname'],alias= request.POST['alias'],  password=pw_hash, email = request.POST['email'], birthday= request.POST['birthday'])
    request.session['user'] = request.POST['email']
    messages.success(request, "User successfully created")
    return redirect('/friends')
def logout(request):
    if 'user' in request.session:
        request.session.clear()
    return redirect('/main')

def friends(request):
    if 'user' not in request.session:
        return redirect('/main')
    user = User.objects.get(email=request.session['user'])
    list =[]
    flag =0
    for u in User.objects.all():
        if u.id != user.id:
            for f in Friends.objects.all():
                if f.my_id == user and f.f_id==u:
                    flag=1
                if f.my_id == u and f.f_id==user:
                    flag=1
            if flag ==1:
                flag=0
            else:
                list.append(u)
    context = {
        'theuser': User.objects.get(email=request.session['user']),
        'users': User.objects.all(),
        'friends': Friends.objects.all(),
        'list': list,
        'count': Friends.objects.filter(Q(my_id = user) | Q(f_id = user)).count()
    }
    return render(request, 'friends.html', context)

def remove(request, id):
    if 'user' not in request.session:
        return redirect('/main')
    c = Friends.objects.get(id=id)
    c.delete()

    return redirect('/friends')
def add(request, id):
    if 'user' not in request.session:
        return redirect('/main')
    user = User.objects.get(email=request.session['user'])
    Friends.objects.create(my_id=user, f_id=User.objects.get(id=id))
    return redirect('/friends')
def user(request, id):
    if 'user' not in request.session:
        return redirect('/main')
    context = {
        'theuser': User.objects.get(email=request.session['user']),
        'user': User.objects.get(id=id)
    }
    return render(request, 'user.html', context)