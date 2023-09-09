from random import random

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView, CreateView, DetailView, ListView
from django.utils.translation import gettext_lazy as _, ngettext

from myauth.forms import ProfileUploaFileForm
from myauth.models import Profile


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return (self.request.user.is_superuser or
                self.request.user.is_staff or
                self.get_object().pk == self.request.user.pk
                )


class HelloView(View):
    welcome_message = _("welcome hello word")
    def get(self, request: HttpRequest) -> HttpResponse:
        items_str = self.request.GET.get("items") or 0
        items = int(items_str)
        products_line = ngettext(
            "one product",
            "{count} products",
            items,
        )
        product_line = products_line.format(count=items)
        return HttpResponse(
            f"<h1>{self.welcome_message}</h1>" 
            f"<h2>{product_line}</h2>"
        )


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/admin/')
        return render(request, 'myauth/login.html')
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect ('/admin/')
    return render(request, "myauth/login.html", {"error": "Invalid login credentials"})


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect(reverse("myauth:login"))


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")


class AccountslistView(ListView):
    template_name = "myauth/accounts.html"
    model = User
    context_object_name = "users"


class AccountDetailView(StaffRequiredMixin, DetailView):
    template_name = "myauth/user-details.html"
    model = User
    context_object_name = "user"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        if hasattr(user, 'profile'):
            profile = user.profile
        else:
            profile = Profile.objects.create(user=user)
        context['profile'] = profile
        context['form'] = ProfileUploaFileForm(instance=profile)
        return context

    def post(self, request, *args, **kwargs):
        pk = kwargs['pk']
        user = get_object_or_404(User, id=pk)
        form = ProfileUploaFileForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            form.save()
        return redirect('myauth:user_details', pk=pk)


class AboutMeView(LoginRequiredMixin, TemplateView):
    template_name = "myauth/about-me.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if hasattr(user, 'profile'):
            profile = user.profile
        else:
            profile = Profile.objects.create(user=user)

        context['profile'] = profile
        context['form'] = ProfileUploaFileForm(instance=profile)
        return context

    def post(self, request, *args, **kwargs):
        form = ProfileUploaFileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('myauth:about-me')





class RegisterView(CreateView):
    form_class = UserCreationForm
    model = User
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")
    def form_valid(self, form):
        response = super().form_valid(form)
        avatar = form.cleaned_data.get("avatar")
        bio = form.cleaned_data.get("bio")
        if avatar:
            Profile.objects.create(user=self.object, avatar=avatar, bio=bio)
        else:
            Profile.objects.create(user=self.object, bio=bio)

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(self.request, user=user)
        return response


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/admin/')
        return render(request, 'myauth/login.html')
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect ('/admin/')
    return render(request, "myauth/login.html", {"error": "Invalid login credentials"})


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect(reverse("myauth:login"))


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")
    def form_valid(self, form):
        response = super().form_valid(form)
        avatar = form.cleaned_data.get("avatar")
        bio = form.cleaned_data.get("bio")
        if avatar:
            Profile.objects.create(user=self.object, avatar=avatar, bio=bio)
        else:
            Profile.objects.create(user=self.object, bio=bio)

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(self.request, user=user)
        return response

@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response

@cache_page(60 * 2)
def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default value")
    return HttpResponse(f"Cookie value: {value!r} + {random()}")


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set!")


@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default")
    return HttpResponse(f"Session value: {value!r}")


class Jsonresponse:
    pass


class FooBarView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return JsonResponse({"foo": "bar", "spam": "eggs"})


