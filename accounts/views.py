from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, views as auth_views
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.utils.html import strip_tags
from django.urls import reverse

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
                messages.success(request, "Seu login foi realizado com sucesso!")
                return redirect(request.META.get('HTTP_REFERER', '/'))
            messages.success(request, "Bem vindo ao painel administrativo!")
            return redirect('dashboard')
        else:
            # Adiciona uma mensagem de erro para o modal
            messages.error(request, "Usuário ou senha incorretos.")
            return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect(request.META.get('HTTP_REFERER', '/'))

def logout_view(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))

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
            customer.generate_verification_code()  # Gera o código de verificação
            customer.save()

            #Verifica o e-mail informado
            send_verification_code(customer)

            # Logar o usuário automaticamente
            login(request, new_user)

            # Redireciona para a página de confirmação do e-mail com PRG
            return redirect('verify_email')
        
        else:
            # Formulários inválidos: retorna para a mesma página mostrando os erros
            categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')

            context = {
                'user_form': user_form,       # Contém os erros do formulário de usuário
                'customer_form': customer_form,  # Contém os erros do formulário de cliente
                'categories': categories,
                'is_not_list_page': True,
                'breadcrumb_off': True,
            }
            return render(request, self.template_name, context)

def send_verification_code(customer):
    html_message = render_to_string('emails/verification_code_email.html', {
        'customer': customer,
        'code': customer.email_verification_code,
    })
    plain_message = strip_tags(html_message)
    send_mail(
        subject="Seu Código de Verificação - Sacolão",
        message=plain_message,
        from_email="noreply@sacolao.be",
        recipient_list=[customer.email],
        html_message=html_message,
    )

class EmailVerificationView(View):
    template_name = "verify_email.html"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:  # Garante que o usuário está logado
            messages.error(request, "Você precisa estar logado para verificar seu e-mail.")
            return redirect("login")

        customer = request.user.customer_profile

        # Verifica se o e-mail já foi verificado
        if customer.is_email_verified:
            messages.info(request, "Seu e-mail já foi verificado.")
            return redirect("/")  # Redireciona para o dashboard

        # Contexto para renderizar a página
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
        context = {
            'categories': categories,
            'is_not_list_page': True,
            'breadcrumb_off': True,
        }

        # Renderiza a página de verificação
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:  # Garante que o usuário está logado
            messages.error(request, "Você precisa estar logado para verificar seu e-mail.")
            return redirect("login")

        customer = request.user.customer_profile
        code = request.POST.get("verification_code")

        # Verifica se o código está correto e não expirou
        if code == customer.email_verification_code and customer.email_verification_code_expiry > now():
            customer.is_email_verified = True
            customer.email_verification_code = None
            customer.email_verification_code_expiry = None
            customer.save()
            messages.success(request, "E-mail verificado com sucesso! Por favor, complete o seu cadastro.")
            return redirect('complete_registration', customer_id=customer.id)
        else:
            messages.error(request, "Código inválido ou expirado. Tente novamente.")
        
        # Contexto para recarregar a página com erro
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
        context = {
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
            # Agora que o cadastro está completo, enviamos o email de boas-vindas
            confirmation_link = request.build_absolute_uri('/')  # Se quiser um link qualquer (p.ex. homepage)
            send_welcome_email(customer, confirmation_link)

            messages.success(request, "Cadastro concluído com sucesso!")
            return redirect('/')  # Redirecionar onde você quiser: página inicial ou perfil

        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')

        context = {
            'form': form,
            'categories': categories,
            'is_not_list_page': True,
            'breadcrumb_off': True,
        }
        return render(request, self.template_name, context)

def send_welcome_email(customer, confirmation_link):
    # Renderizando o template
    html_message = render_to_string('emails/welcome_email.html', {'customer': customer, 'confirmation_link': confirmation_link})
    plain_message = strip_tags(html_message)  # Para versões que não suportam HTML
    
    # Enviando o e-mail
    send_mail(
        'Bem-vindo(a) ao Sacolão.be!',
        plain_message,  # Mensagem de texto (opcional)
        None,  # No default FROM_EMAIL, já será utilizado o DEFAULT_FROM_EMAIL configurado
        [customer.email],  # Para quem o e-mail será enviado
        html_message=html_message,  # Para versões que suportam HTML
        fail_silently=False,
    )


# Redefinição de senhas (Esqueci minha senha)

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    html_email_template_name = 'emails/password_reset_email.html'  # Define o template HTML personalizado

    def get_context_data(self, **kwargs):
        # Adiciona categorias e outros dados ao contexto
        context = super().get_context_data(**kwargs)
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
        context.update({
            'categories': categories,
            'is_not_list_page': True,
            'breadcrumb_off': True,
        })
        return context

    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        """
        Sobrescreve o método de envio de e-mail para garantir o uso do template personalizado.
        """
        reset_url = self.request.build_absolute_uri(reverse('password_reset_confirm', kwargs={
            'uidb64': context['uid'],
            'token': context['token']
        }))

        # Renderiza o template HTML
        html_message = render_to_string(self.html_email_template_name, {
            'user': context.get('user'),
            'reset_url': reset_url,
        })
        plain_message = strip_tags(html_message)

        # Envia o e-mail com suporte a texto puro e HTML
        email = EmailMultiAlternatives(
            subject="Redefinição de Senha - Sacolão",
            body=plain_message,
            from_email=from_email or settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
        )
        email.attach_alternative(html_message, "text/html")
        email.send()

class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
        context.update({
            'categories': categories,
            'is_not_list_page': True,
            'breadcrumb_off': True,
        })
        return context

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
        context.update({
            'categories': categories,
            'is_not_list_page': True,
            'breadcrumb_off': True,
        })
        return context

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
        context.update({
            'categories': categories,
            'is_not_list_page': True,
            'breadcrumb_off': True,
        })
        return context

