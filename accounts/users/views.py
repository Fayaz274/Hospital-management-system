from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.views.generic import ListView,TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import CustomUser
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.edit import UpdateView
from django.contrib import messages


# Create your views here.
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm,CustomAuthenticationForm, UserEditForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

##################################Super Admin Views############################## 
class SuperadminHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'superadmin/superadmin_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
    
class SuperadminUserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = CustomUser
    template_name='superadmin/user_list.html'
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.role=="superadmin"
    def get_queryset(self):
        # Get the queryset of CustomUser objects, excluding superadmin users
        return CustomUser.objects.exclude(role="superadmin")

class UserEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CustomUser
    form_class = UserEditForm
    template_name = 'superadmin/superadmin_user_edit.html'  # Create this template

    # Redirect to a success URL after editing
    success_url = reverse_lazy('superadmin-user-list')  # Adjust this URL as needed
    def test_func(self):
        return self.request.user.role=="superadmin"

    # Optional: You can override the get_queryset method to further filter users if needed
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     # You can add filtering logic here
    #     return queryset
    
class DeleteUserView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.role == 'superadmin'

    def get(self, request, user_id):
        # Get the user based on the user_id
        user = get_object_or_404(CustomUser, id=user_id)
        return render(request, 'superadmin/super_delete_user.html', {'user': user})

    def post(self, request, user_id):
        # Get the user based on the user_id
        user = get_object_or_404(CustomUser, id=user_id)

        # Delete the user
        user.delete()
        return redirect('superadmin-user-list')
    
class ViewUserDetailsView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.role == 'superadmin'

    def get(self, request, user_id):
        # Get the user based on the user_id
        user = get_object_or_404(CustomUser, id=user_id)
        return render(request, 'superadmin/user_details.html', {'user': user})
    
class AddUserView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.role == 'superadmin'
    def get(self, request):
        # Display the user creation form
        form = CustomUserCreationForm()
        return render(request, 'superadmin/add_user.html', {'form': form})

    def post(self, request):
        # Handle the user creation form submission
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Create a new user
            user = form.save()
            # Customize user role as needed (e.g., set it to 'admin' or 'patient')
            # user.role = 'admin'  # Change to the desired role
            user.save()
            return redirect('superadmin-user-list')  # Redirect to the user list page after successful creation
        return render(request, 'superadmin/add_user.html', {'form': form})
    
####################################Profile Views##############################################
class ViewProfileView(LoginRequiredMixin, View):
    template_name = 'view_profile.html'

    def get(self, request):
        return render(request, self.template_name)

class EditProfileView(LoginRequiredMixin, View):
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('view-profile')

    def get(self, request):
        form = UserEditForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})
####################################Admin Views################################################
class AdminHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'admin/admin_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
    def test_func(self):
        return self.request.user.role=="admin"
    
# class AdminUserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
#     model=CustomUser
#     template_name='admin/admin_user_list.html'
#     context_object_name='users'

#     def test_func(self):
#         return self.request.user.role=="superadmin"
    
#     def get_queryset(self):
#         # Get the queryset of CustomUser objects, excluding superadmin users
#         return CustomUser.objects.exclude(role="superadmin")

def custom_login(request):
    if request.method == 'POST':
        # Handle the login form submission
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            # Authentication logic
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                
                # Log the user in
                login(request, user)
                # Redirect based on user role
                if user.role == 'superadmin':
                    return redirect('superadmin-home')                
                elif user.role == 'admin':
                    return redirect('admin-home') 
                elif user.role == 'doctor':
                    return redirect('doctor-home')
                elif user.role == 'employee':
                    return redirect('employee-home')
                elif user.role == 'patient':
                    return redirect('patient-home')

    else:
            form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})






