from django.contrib.auth.models import User

def is_first_purchase(request):
    if request.user.is_authenticated:
        return {'is_first_purchase': not request.user.order_set.exists()}
    return {'is_first_purchase': False}
