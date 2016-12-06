from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView, ModelFormMixin
from django.forms import Form, ModelForm

from store.models import Order

class OrderCreate(CreateView):
    model = Order
    http_method_names = ['get', 'post']
    success_url = '/thanks/'
    fields = ['from_first_name', 'from_last_name', 'from_email', 'to_first_name', 'to_last_name', 'delivery_company_name', 'to_first_name']

class CheckoutForm(ModelForm):
    class Meta:
        model = Order
        fields = ['from_first_name', 'from_last_name',
                  'to_first_name', 'to_last_name',
                  'delivery_company_name', 'delivery_first', 'delivery_second',
                  'delivery_third', 'delivery_postcode', 'delivery_note']

def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            print form
            print form.cleaned_data
            order = Order(from_first_name=form.cleaned_data['from_first_name'],
                          from_last_name=form.cleaned_data['from_last_name'],
                          from_email=request.POST.get('stripeEmail'),
                          stripe_tx=request.POST.get('stripeToken'),
                          to_first_name=form.cleaned_data['to_first_name'],
                          to_last_name=form.cleaned_data['to_last_name'],
                          delivery_company_name=form.cleaned_data['delivery_company_name'],
                          delivery_first=form.cleaned_data['delivery_first'],
                          delivery_second=form.cleaned_data['delivery_second'],
                          delivery_third=form.cleaned_data['delivery_third'],
                          delivery_postcode=form.cleaned_data['delivery_postcode'],
                          delivery_note=form.cleaned_data['delivery_note'],
                         )
            order.save()

            return HttpResponseRedirect('/thanks/')
    else:
        form = CheckoutForm()

    return render(request, 'store/order_form.html', {'form': form})

def index(request):
    return render(request, 'store/index.html')

def thanks(request):
    return render(request, 'store/thanks.html')

def tos(request):
    return render(request, 'store/tos.html')
