from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import bcrypt
from django.http import HttpResponseRedirect
from django.db.models import Q
from . models import User, Quotes




def index(request):
    if "userId" not in request.session:
        request.session['userId'] = None
    return render(request, "index.html")

def addUser(request):
    print(request.POST)
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        securedPass= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        oneUser = User.objects.create(userName=request.POST['userName'],firstName=request.POST['firstName'],lastName=request.POST['lastName'],email=request.POST['email'],password=securedPass)
        request.session['userId'] = oneUser.id
        return redirect('/userPage')

    return redirect('/userPage')

def userPage(request):
    if "userId" not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['userId']),
            'allQuotes': Quotes.objects.all(),
            'likedQuotes': Quotes.objects.filter(Q(likes=User.objects.get(id=request.session['userId']))|Q(uploader=User.objects.get(id=request.session['userId']))),
            'unlikedQuotes': Quotes.objects.exclude(Q(likes=User.objects.get(id=request.session['userId']))|Q(uploader=User.objects.get(id=request.session['userId']))),
        }
    return render(request, "loginPage.html", context)

def loginUser(request):
    #send the request.POST to the validator
    valErrors = User.objects.loginValidator(request.POST)
    if len(valErrors) > 0:
        for value in valErrors.values():
            messages.error(request, value)
        return redirect('/')
    else:
        usersWithEmail = User.objects.filter(email = request.POST['email'])
        request.session['userId'] = usersWithEmail[0].id
        return redirect('/userPage')

def addQuote(request):
    errors = Quotes.objects.quoteValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/userPage')
    else:
        newQuote = Quotes.objects.create(author=request.POST['author'],quote=request.POST['quote'], uploader=User.objects.get(id=request.session['userId']))
        return redirect('/userPage')

def like(request, quoteId):
    user = User.objects.get(id=request.session['userId'])
    quote = Quotes.objects.get(id=quoteId)
    quote.likes.add(user)
    return redirect('/userPage')

def userQuote(request, userQuote):
    context = {
        'iUser': User.objects.get(id=request.session['userId']),
        'user': User.objects.get(id=int(userQuote)),
        'userQuotes': Quotes.objects.filter(uploader=User.objects.get(id=int(userQuote)))
    }
    return render(request, "userQuote.html", context)

def goHome(request):
    return redirect('/userPage')

def delete(request, quoteId):
    quote = Quotes.objects.get(id=int(quoteId))
    quote.delete()
    return redirect('/userPage')

def editUser(request):
    context = {
        'user': User.objects.get(id=request.session['userId'])
    }
    return render(request, "editUser.html", context)

def confirmEdit(request):
    errors = User.objects.editValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        securedPass= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.get(id=request.session['userId'])
        user.userName = request.POST['userName']
        user.firstName = request.POST['firstName']
        user.lastName = request.POST['lastName']
        user.userName = request.POST['userName']
        user.email = request.POST['email']
        user.password = securedPass
        user.save()
        return redirect('/userPage')

def destroySession(request):
    request.session.clear()
    return redirect('/')