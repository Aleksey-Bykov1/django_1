from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.template.loader import render_to_string
from django.http import JsonResponse

from products.models import Product
from baskets.models import Basket


@login_required()
def basket_add(request, id):
    product = Product.objects.get(id=id)
    baskets = Basket.objects.filter(user=request.user, product=product)
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required()
def basket_remove(request, id):
    Basket.objects.get(id=id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required()
def baskets_edit(request, id, quantity):
    if request.is_ajax():
        basket = Basket.objects.get(id=id)
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()

        baskets = Basket.objects.filter(user=request.user)
        # context = {'baskets': baskets}
        result = render_to_string('baskets/basket.html', request=request)
        return JsonResponse({'result': result})
