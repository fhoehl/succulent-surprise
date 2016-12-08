import os

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView, ModelFormMixin
from django.forms import Form, ModelForm

import stripe

from store.models import Order

stripe.api_key = os.environ['STRIPE_API_KEY']

class CheckoutForm(ModelForm):
    class Meta:
        model = Order
        fields = ['from_first_name', 'from_last_name',
                  'to_first_name', 'to_last_name',
                  'delivery_company_name', 'delivery_first', 'delivery_second',
                  'delivery_third', 'delivery_postcode', 'delivery_note']

def process_payment(stripe_email, stripe_token, form):
    order = Order(state='S',
                  from_first_name=form.cleaned_data['from_first_name'],
                  from_last_name=form.cleaned_data['from_last_name'],
                  from_email=stripe_email,
                  stripe_tx=stripe_token,
                  to_first_name=form.cleaned_data['to_first_name'],
                  to_last_name=form.cleaned_data['to_last_name'],
                  delivery_company_name=form.cleaned_data['delivery_company_name'],
                  delivery_first=form.cleaned_data['delivery_first'],
                  delivery_second=form.cleaned_data['delivery_second'],
                  delivery_third=form.cleaned_data['delivery_third'],
                  delivery_postcode=form.cleaned_data['delivery_postcode'],
                  delivery_note=form.cleaned_data['delivery_note'],)

    try:
        # Create a charge: this will charge the user's card
        charge = stripe.Charge.create(amount=1700,
                                      currency='gbp',
                                      source=stripe_token,
                                      description='One succulent surprise')

        order.state = 'P'
    except stripe.error.CardError as e:
        # The card has been declined
        order.state = 'E'
    finally:
        order.save()

    return order

def checkout(request):
    if request.method != 'POST':
        form = CheckoutForm()

    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            stripe_email = request.POST['stripeEmail'],
            stripe_token = request.POST['stripeToken'],
            order = process_payment(stripe_email[0], stripe_token[0], form)

            if order.state == 'P':
                return HttpResponseRedirect('/thanks/')

    return render(request, 'store/order_form.html', {'form': form})

def index(request):
    return render(request, 'store/index.html')

def thanks(request):
    return render(request, 'store/thanks.html')

def tos(request):
    return render(request, 'store/tos.html')
