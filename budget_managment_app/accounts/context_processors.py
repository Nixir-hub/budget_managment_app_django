from .models import AccountBalance

def account_balance(request):
    if request.user.is_authenticated:
        account = AccountBalance.objects.filter(user=request.user).first()
        return {'nav_balance': account.balance if account else 0}
    return {}
