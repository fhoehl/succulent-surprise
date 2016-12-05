from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView

from store.models import Order

class OrderCreate(CreateView):
    model = Order
    http_method_names = ['get', 'post']
    success_url = '/thanks/'
    fields = ['from_first_name', 'from_last_name', 'from_email', 'from_phone', 'to_first_name', 'to_last_name', 'delivery_company_name', 'to_first_name']
    #template_name = 'store/checkout.html'

def index(request):
    return render(request, 'store/index.html')

def checkout(request):
    return render(request, 'store/checkout.html')
