from django.contrib.auth.forms import AuthenticationFormfrom django.contrib.auth.models import Userfrom django.shortcuts import render, get_object_or_404, redirectfrom django.utils.translation import gettextfrom django.views import Viewfrom django.contrib.auth.decorators import login_requiredfrom django.contrib import messagesfrom django.contrib.auth import authenticate, login, logoutfrom task_manager.views import indexfrom .forms import SignUpForm, UpdateUserFormfrom task_manager.tasks.models import Taskclass UserListView(View):    def get(self, request, *args, **kwargs):        users = User.objects.all().order_by('id')        return render(request, 'users/users.html', context={            "users": users,        })@login_requireddef logout_view(request):    logout(request)    messages.info(request, gettext('You are logged out'))    return redirect(index)class SignUpView(View):    def get(self, request):        form = SignUpForm()        return render(request, 'users/create.html', {"form": form})    def post(self, request):        form = SignUpForm(request.POST)        if form.is_valid():            form.save()            messages.success(request, gettext('User successfully registered'))            return redirect('/login')        return render(request, 'users/create.html', {"form": form})class LoginView(View):    def get(self, request):        form = AuthenticationForm()        return render(request, 'login.html', {"form": form})    def post(self, request):        form = AuthenticationForm(request, data=request.POST)        if form.is_valid():            user_data = form.cleaned_data            user = authenticate(                username=user_data.get("username"),                password=user_data.get("password"                                       ))            if user is not None and user.is_active:                login(request, user)                messages.success(request, gettext('You are logged in'))                return redirect(index)            messages.error(request, gettext(                'Please enter the correct username and password. '                'Both fields can be case sensitive.'            ))        return render(request, 'login.html', {"form": form})class UserDeleteView(View):    def get(self, request, *args, **kwargs):        user = get_object_or_404(User, id=kwargs['id'])        if request.user.is_authenticated:            if user.id != request.user.id:                messages.error(request,                               gettext(                                   'You do not have rights '                                   'to change another user.'                               ))                return redirect('users')            else:                return render(request, 'users/delete.html', context={                    "user": user                })        messages.error(request,                       gettext(                           'You do not have rights to change another user.'                       ))        return redirect('users')    def post(self, request, *args, **kwargs):        context = {}        user = get_object_or_404(User, id=kwargs['id'])        if request.user.is_authenticated:            if user.id == request.user.id:                if user.id not in \                        Task.objects.values_list('author_id', flat=True) and \                        user.id not in \                        Task.objects.values_list('executor_id', flat=True):                    user.delete()                    context['user'] = user                    messages.success(request, gettext(                        'User deleted successfully'                    ))                    return redirect('/users')                else:                    messages.error(request,                                   gettext(                                       'Unable to delete user '                                       'because he used'                                   ))                    return render(request, 'users/users.html', context)            else:                messages.error(request,                               gettext(                                   'You do not have rights '                                   'to change another user.'                               ))                return render(request, 'users/users.html', context)        else:            messages.error(request,                           gettext(                               'You do not have rights to change another user.'                           ))            return render(request, 'users/users.html', context)class UserUpdateView(View):    def get(self, request, *args, **kwargs):        user = get_object_or_404(User, id=kwargs['id'])        if request.user.is_authenticated:            if user.id != request.user.id:                messages.error(request,                               gettext(                                   'You do not have rights '                                   'to change another user.'                               ))                return redirect('users')            else:                form = UpdateUserForm(user.id, {                    "first_name": user.first_name,                    "last_name": user.last_name,                    "username": user.username,                    "password1": "123",                    "password2": "123"                })                return render(request, 'users/update.html',                              context={"form": form, "user": user})        messages.error(request,                       gettext(                           'You do not have rights to change another user.'                       ))        return redirect('users')    def post(self, request, *args, **kwargs):        if request.user.is_authenticated:            form = UpdateUserForm(request.user.id, request.POST)            if form.is_valid():                form.save()                messages.success(request, gettext('User successfully updated'))                return redirect('users')            else:                return render(request, 'users/update.html',                              context={"form": form})