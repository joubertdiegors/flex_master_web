from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .forms import UserBasicRegistrationForm, CustomerBasicRegistrationForm, CustomerCompleteRegistrationForm
from .mixins.mixins import CustomerAccessMixin
from customers.models import Customer, CustomerState, CustomerType
from products.models import Category

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Usa a sessão antiga para a transferência do carrinho de compras do anônimo para o usuário que for logado
            old_session_key = request.session.session_key
            login(request, user)
            request.session['old_session_key'] = old_session_key
            
            if not user.is_superuser and not user.is_staff:
                return redirect('/')
            return redirect('dashboard')
        else:
            login_form = AuthenticationForm()
    else:
        login_form = AuthenticationForm()
    return render(request, 'login.html', {'login_form': login_form})

def logout_view(request):
    logout(request)
    return redirect('/')

class RegisterBasicView(View):
    template_name = 'register_basic.html'

    def get(self, request, *args, **kwargs):
        user_form = UserBasicRegistrationForm()
        customer_form = CustomerBasicRegistrationForm()
        
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')

        context = {
            'user_form': user_form,
            'customer_form': customer_form,
            'categories': categories,
            'is_not_list_page': True,
            'breadcrumb_off': True,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_form = UserBasicRegistrationForm(request.POST)
        customer_form = CustomerBasicRegistrationForm(request.POST)

        if user_form.is_valid() and customer_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.username = user_form.cleaned_data['email']
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            customer = customer_form.save(commit=False)
            customer.user = new_user
            customer.first_name = new_user.first_name
            customer.last_name = new_user.last_name
            customer.email = new_user.email
            customer.created_by = new_user

            customer.save()

            # Logar o usuário automaticamente
            login(request, new_user)

            return redirect('complete_registration', customer_id=customer.id)

        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')

        context = {
            'user_form': user_form,
            'customer_form': customer_form,
            'categories': categories,
            'is_not_list_page': True,
            'breadcrumb_off': True,
        }
        return render(request, self.template_name, context)

class CompleteRegistrationView(CustomerAccessMixin, View):
    template_name = 'complete_registration.html'

    def get(self, request, customer_id, *args, **kwargs):
        customer = get_object_or_404(Customer, id=customer_id)
        form = CustomerCompleteRegistrationForm(instance=customer)
        
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')

        context = {
            'form': form,
            'categories': categories,
            'is_not_list_page': True,
            'breadcrumb_off': True,
        }
        return render(request, self.template_name, context)

    def post(self, request, customer_id, *args, **kwargs):
        customer = get_object_or_404(Customer, id=customer_id)
        form = CustomerCompleteRegistrationForm(request.POST, request.FILES, instance=customer)

        if form.is_valid():
            form.save()
            return redirect('/')  # Redirecionar para a página de perfil ou login

        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')

        context = {
            'form': form,
            'categories': categories,
            'is_not_list_page': True,
            'breadcrumb_off': True,
        }
        return render(request, self.template_name, context)
