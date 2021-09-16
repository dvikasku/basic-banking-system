from django.shortcuts import render,redirect
from customers.models import Customer
from transaction.models import Payment
from django.contrib import messages

# Create your views here.
def search(request):
    query = request.GET['query']

    if len(query) > 78:
        cust = Customer.objects.none()
    else:
        print(query)
        custname = Customer.objects.filter(cust_name__icontains = query)
    params = {'users': custname, 'query': query}
    return render(request, 'search.html', params)

def usersList(request):
    return render(request ,'index.html')

def home(request):
    cust = Customer.objects.all()
    return render(request , 'transfer_money.html' , { 'users' : cust })

def sendMoney(request, id):
    cust_data = Customer.objects.get(id=id)
    allCust = Customer.objects.all().exclude(id=id)
    return render(request , 'transfer.html', { 'customs' : cust_data , 'allCust' : allCust})

def handleTransfer(request):
    name = request.POST.get('name')
    idP = request.POST.get('idP')
    sendTo = request.POST.get('sendTo')
    if sendTo == '-1':
        messages.error(request, 'Please select a user to send money')
        return redirect('sendmoney' , id=int(idP))
    amount = request.POST.get('amount')
    if int(amount) < 0:
        messages.error(request, "Amount can't be negative")
        return redirect('sendmoney', id=int(idP))
    person = Customer.objects.get(id=idP)
    person2 = Customer.objects.get(cust_name= sendTo)

    if int(person.balance) > int(amount):
        person.balance = int(person.balance) - int(amount)
        person.save()
        payment = Payment(frm = name, to=sendTo , amount=amount)
        person2.balance = int(person2.balance) + int(amount)
        payment.save()
        person2.save()
        messages.success(request, 'Payment done successfully')
    else:
        messages.error(request, 'Insufficient Balance')
    return redirect('transactions')


def transactions(request):
    trans = Payment.objects.all().order_by('-id')
    return render(request, 'display.html' , { 'trans' : trans  })
