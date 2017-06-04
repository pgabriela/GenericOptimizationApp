from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login


def loginPage(request):
    if(request.method == "POST"):
        form = LoginForm(data=request.POST)
        if(form.is_valid()):
            form = form.clean()
            currentUser = authenticate(username=form['username'],
                                       password=form['password'])
            if(currentUser):
                login(request, currentUser)
                return redirect('/tripPlanner')
            else:
                return redirect('/')
        else:
            return redirect('/')
    else:
        if(request.user.is_authenticated):
            return redirect('/tripPlanner')
        else:
            form = LoginForm()
            return render(request, 'login/loginPage.html', {'form': form})
