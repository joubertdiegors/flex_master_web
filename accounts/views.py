from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout, views as auth_views
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse

from .forms import UserBasicRegistrationForm, CustomerBasicRegistrationForm, CustomerCompleteRegistrationForm
from .mixins.mixins import CustomerAccessMixin
from customers.models import Customer, CustomerState, CustomerType
from products.models import Category
from .tokens import email_verification_token

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
            customer.save()

            #Verifica o e-mail informado
            send_verification_email(customer, request)

            # Logar o usuário automaticamente
            login(request, new_user)

            # Redireciona para a página de confirmação do e-mail com PRG
            return redirect('email_confirmation_sent', email=new_user.email)
        
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

class EmailConfirmationSentView(View):
    template_name = 'email_confirmation_sent.html'

    def get(self, request, *args, **kwargs):
        # Verifica se o cliente está autenticado
        if not request.user.is_authenticated:
            return redirect('/')  # Redireciona para a página principal se não estiver autenticado

        email = kwargs.get('email')

        # Verifica se o email pertence ao usuário autenticado
        if email != request.user.email:
            return redirect('/')  # Redireciona para a página principal se o email não pertencer ao usuário

        # Recupera categorias e mantém o contexto
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')
        context = {
            'email': email,
            'categories': categories,
            'is_not_list_page': True,
            'breadcrumb_off': True,
        }
        return render(request, self.template_name, context)

def send_verification_email(customer, request):
    try:
        # Gera o uidb64 (ID codificado)
        uid = urlsafe_base64_encode(force_bytes(customer.pk))
        # Gera o token de verificação
        token = email_verification_token.make_token(customer)
        
        # Monta a URL de ativação (/activate/<uidb64>/<token>/)
        activate_url = request.build_absolute_uri(
            reverse('activate', kwargs={'uidb64': uid, 'token': token})
        )
        
        # Exemplo de template HTML para o e-mail
        html_content = render_to_string('emails/verification_email.html', {
            'customer': customer,
            'activate_url': activate_url,
        })
        plain_message = strip_tags(html_content)
        
        subject = "Ative sua conta para continuar"
        from_email = None  # Usa o DEFAULT_FROM_EMAIL se configurado
        recipient_list = [customer.email]
        
        send_mail(
            subject,
            plain_message,
            from_email,
            recipient_list,
            html_message=html_content,
            fail_silently=False,
        )
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

def activate_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        customer = get_object_or_404(Customer, pk=uid)
    except (TypeError, ValueError, OverflowError):
        customer = None

    # Se o objeto Customer for inválido, ou se o token não for mais válido
    if not customer or not email_verification_token.check_token(customer, token):
        # Aqui token está inválido/expirado.
        # Exibir página customizada, calculando quantos dias faltam ou já expirou
        days_passed = (timezone.now() - customer.created_at).days if customer else 0
        # Se o token expira em 5 dias (432000s), calcule:
        days_left = 5 - days_passed

        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')

        context = {
            'customer': customer,
            'days_left': days_left,
            'categories': categories,
            'is_not_list_page': True,
            'breadcrumb_off': True,
        }
        return render(request, 'expired_token.html', context)

    # Se o token está válido, prossegue com a ativação
    customer.is_email_verified = True
    customer.save()
    messages.success(request, "Seu e-mail foi confirmado com sucesso!")
    return redirect('complete_registration', customer_id=customer.id)

def resend_verification(request, customer_id):
    if request.method == 'POST':
        customer = get_object_or_404(Customer, pk=customer_id)
        if not customer.is_email_verified:
            # Gera novo token, reenvia e-mail
            send_verification_email(customer, request)
            messages.success(request, "Um novo e-mail de verificação foi enviado.")
        else:
            messages.info(request, "O e-mail deste usuário já foi verificado.")
    return redirect('/')

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

