from .forms import SignupForm, EditUserProfileForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
# Create your views here.


def signup(request):
    if request.method == 'POST':
        fr = SignupForm(request.POST, request.FILES)
        if fr.is_valid():
            messages.success(request, 'Account created successfullly ')
            fr.save()
    else:
        fr = SignupForm()
    return render(request, 'blogreg.html', {'form': fr})


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            fl = AuthenticationForm(request=request, data=request.POST)
            if fl.is_valid():
                uname = fl.cleaned_data['username']
                upass = fl.cleaned_data['password']
                # request.session['name'] = uname
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'You login Successfully  ')
                    return HttpResponseRedirect('/profile/')
        else:
            fl = AuthenticationForm()
        return render(request, 'login.html', {'form': fl})
    else:
        return HttpResponseRedirect('/profile/')


def profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fp = EditUserProfileForm(request.POST, instance=request.user)
            users = None
            if fp.is_valid():
                messages.success(request, 'Profile Update !!  ')
                fp.save()
        else:
            fp = EditUserProfileForm(instance=request.user)
            users = None

        # name = request.session['name']
        # request.session.modified = True
        return render(request, 'profile.html', {'name': request.user.username, 'form': fp, 'users': users})
    else:
        return HttpResponseRedirect('/login/')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def user_change_pass(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fc = PasswordChangeForm(user=request.user, data=request.POST)
            if fc.is_valid():
                fc.save()
                update_session_auth_hash(request, fc.user)
                messages.success(request, 'Password Change Suceesfuuly !!')
                return HttpResponseRedirect('/profile/')
        else:
            fc = PasswordChangeForm(user=request.user)
        return render(request, 'changepass.html', {'form': fc})
    else:
        return HttpResponseRedirect('/profile/')
