from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateUserForm, LoginForm, UpdateUserForm, CustomPasswordResetForm, CustomSetPasswordForm
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress

from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer_generate

from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, logout, login

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from payment.models import Order
# Create your views here.
def register(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            # form.save()
            # return redirect('store')
            user = form.save()
            user.is_active =  False
            user.save()
            #Email verification setup
            current_site = get_current_site(request)
            subject = 'Account verification email'
            message = render_to_string('account/registration/email-verification.html',{

                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return redirect('email-verification-sent')
        
    context = {'form':form,'show_navbar': False}
    return render(request, 'account/registration/register.html', context=context)

def email_verification(request,uidb64, token):
    #unique id
    unique_id = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=unique_id)

    #success
    if user and user_tokenizer_generate.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('email-verification-success')
    
    #failed
    else:
        return redirect('email-verification-failed')


def email_verification_sent(request):
    
    context = {'show_navbar': False}
    return render(request, 'account/registration/email-verification-sent.html', context=context)

def email_verification_success(request):
    context = {'show_navbar': False}
    return render(request, 'account/registration/email-verification-success.html', context=context)

def email_verification_failed(request):
    context = {'show_navbar': False}
    return render(request, 'account/registration/email-verification-failed.html', context=context)

def my_login(request):
    
    form = LoginForm()
    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)
                cart = Cart(request)

                # Call the merge_cart_on_login function to merge the guest cart into the authenticated user's cart
                cart.merge_cart_on_login()
                messages.success(request, 'Login Successful')
                return redirect("dashboard")
    
    context = {'form': form,'show_navbar': False}
    return render(request, 'account/my-login.html', context=context)

def user_logout(request):

    try:
        for key in list(request.session.keys()):
            if key == 'session_key':
                continue
            else:
                del request.session[key]
            
    except KeyError:
        pass

    messages.success(request, "Logout Successful")
    # auth.logout(request)

    return redirect("store")

@login_required(login_url='my-login')
def dashboard(request):
    context = {'show_navbar': True}
    return render(request, 'account/dashboard.html', context=context)

@login_required(login_url='my-login')
def profile_management(request):

    #updating the user

    user_form= UpdateUserForm(instance=request.user)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('dashboard')

    # shifted this to above to add validation of username when updating - can't update the username to an already existing username  
    #user_form = UpdateUserForm(instance=request.user)

    context = {'user_form': user_form, 'show_navbar': True}
        
    return render(request, 'account/profile-management.html', context=context)

@login_required(login_url='my-login')
def delete_account(request):

    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        user.delete()
        messages.success(request, "Account Deletion Successful")
        return redirect('store')
    
    context = {'show_navbar': True}

    return render(request, 'account/delete-account.html', context=context)

# shipping view
@login_required(login_url='my-login')
def manage_shipping(request):
    
    try:
        # Account user with shipment information
        shipping = ShippingAddress.objects.get(user=request.user.id)

    except ShippingAddress.DoesNotExist:

        # Account user with no shipment information
        shipping = None
    form = ShippingForm(instance=shipping)

    if request.method == 'POST':
        form = ShippingForm(request.POST, instance=shipping)

        if form.is_valid():
            # Assign the user FK on the object
            shipping_user = form.save(commit=False)
            shipping_user.user = request.user
            shipping_user.save()

            return redirect('dashboard')
        
    context = {'form': form, 'show_navbar': True}
    return render(request, 'account/manage-shipping.html', context=context)


class CustomPasswordResetView(auth_views.PasswordResetView):

    template_name = 'account/password/password-reset.html'
    form_class = CustomPasswordResetForm
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['show_navbar'] = False
        return context
    
class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):

    template_name = 'account/password/password-reset-sent.html'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['show_navbar'] = False
        return context
    
class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):

    template_name='account/password/password-reset-form.html'
    form_class = CustomSetPasswordForm

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['show_navbar'] = False
        return context

class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):

    template_name='account/password/password-reset-complete.html'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['show_navbar'] = False
        return context
    
@login_required(login_url='my-login')
def track_orders(request):

    try:
        orders = Order.objects.filter(user=request.user)
        context = {"orders":orders}

        return render(request, 'account/track-orders.html', context=context)
    except:

        return render(request, 'account/track-orders.html')