from django.shortcuts import render,redirect

# Create your views here.
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction
from django.db import transaction
from decimal import Decimal
from django.contrib.auth.models import User



@login_required
def dashboard(request):

    account, created = Account.objects.get_or_create(user=request.user)

    context = {
        'account': account
    }

    return render(request, 'dashboard.html', context)


from decimal import Decimal


@login_required
def deposit(request):
    account = Account.objects.get(user=request.user)

    if request.method == "POST":
        amount = request.POST.get('amount')

        if amount:   # check if not empty
            amount = Decimal(amount)
            account.balance += amount
            account.save()

            return redirect('dashboard')

    return render(request, 'deposit.html')



@login_required
def withdraw(request):
    account = Account.objects.get(user=request.user)

    if request.method == "POST":
        amount = request.POST.get('amount')

        if amount:
            amount = Decimal(amount)

            if account.balance >= amount:
                account.balance -= amount
                account.save()

                return redirect('dashboard')

    return render(request, 'withdraw.html')

@login_required
def transfer(request):
    sender = Account.objects.get(user=request.user)

    if request.method == "POST":
        receiver_username = request.POST.get('account')
        amount = request.POST.get('amount')

        # check empty fields
        if receiver_username and amount:

            amount = Decimal(amount)

            try:
                receiver_user = User.objects.get(username=receiver_username)
                receiver = Account.objects.get(user=receiver_user)

                if sender.balance >= amount:
                    sender.balance -= amount
                    receiver.balance += amount

                    sender.save()
                    receiver.save()

                    return redirect('dashboard')

            except User.DoesNotExist:
                print("User not found")

    return render(request, "transfer.html")

@login_required
def transactions(request):

    account = Account.objects.get(user=request.user)

    transactions = Transaction.objects.filter(account=account) | Transaction.objects.filter(receiver_account=account)
    context = {
        "transactions": transactions
    }

    return render(request, "transactions.html", context)