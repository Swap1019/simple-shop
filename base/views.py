from typing import Any
from django.db import IntegrityError,DataError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404,redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import ListView,DetailView,View
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TheProduct,Cart,ProductHit,Colors
from django.db.models import Q,Count
from user.models import User
from user.forms import ReportProductForm
from .mixins import PageDataMixin
from .base_views import BaseShopView

class HomeView(PageDataMixin,BaseShopView):
    
    def get_queryset(self):
        #gets the most viewed products that were created by the user
        return TheProduct.objects.availables()
    
class HomeSearchView(PageDataMixin,BaseShopView):

    def get_queryset(self):
        query = self.request.GET.get('SearchQuery')
        return TheProduct.objects.filter(
            Q(product__icontains=query) |
            Q(tags__name__icontains=query),
            availability='A'
        ).order_by('-hits').distinct()
    
class ProductView(PageDataMixin,FormMixin,DetailView):
    template_name = 'base/view_product.html'
    context_object_name = 'product'
    model = TheProduct
    form_class = ReportProductForm
    #gets the specified product
    def get_object(self):
        global product
        product = get_object_or_404(TheProduct,id=self.kwargs.get('id'),availability='A')
        ip_address = self.request.user.ip_address
        if ip_address not in product.hits.all():
            product.hits.add(ip_address)
        return product

    #returns the related product
    def get_context_data(self, *args, **kwargs):
        context = super(ProductView, self).get_context_data(*args, **kwargs)
        categories = product.category.all()  # Assuming a product can belong to multiple categories
        context['related_products'] = TheProduct.objects.filter(category__in=categories,availability='A').exclude(id=product.id)
        context['colors'] = Colors.objects.filter(product=product)
        context['form'] = ReportProductForm(initial={'post': self.object})
        context['views'] = ProductHit.objects.filter(product=product).annotate(hit_count=Count('product')).order_by('-hit_count').count()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        product = TheProduct.objects.get(id = self.kwargs.get('id'))
        #insert user_id and product into form
        form.instance.user = User.objects.get(pk = self.request.user.pk)
        form.instance.reported_product = product
        form.instance.id = product.pk
        form.save()
        return super(ProductView, self).form_valid(form)
    
    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Product Reported Successfuly')
        return reverse('base:product', kwargs={'id': self.kwargs.get('id')})
    
"""Cart Views"""
class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        product_id = kwargs.get('id')
        selected_color = request.GET.get('color')
        
        if not selected_color:
            # Handle the case where no color was selected
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        # Validate product and selected color
        product = get_object_or_404(TheProduct, id=product_id, availability='A')
        cart_product_price = product.final_price

        # Ensure the selected color is valid for the product
        color = Colors.objects.filter(product=product, color=selected_color).first()
        if not color:
            # Handle invalid color selection
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        Cart.objects.get_or_create(
            user=request.user,
            product_id=product_id,
            cart_product_price=cart_product_price,
            color=selected_color,
            checkout=False
        )

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
class IncreaseUpdateCartView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        
        try:
            cart = Cart.objects.get(user = self.request.user, id = self.kwargs.get('id'),checkout = False)
            cart.quantity += 1
            cart.save(update_fields=['quantity'])

        except IntegrityError:
            messages.warning(request=request,message='Not allowed more than 5')
            
        except ObjectDoesNotExist:
            messages.error(request=request,message='Does not exist')

        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class DecreaseUpdateCartView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):

        try:
            cart = Cart.objects.get(user = self.request.user, id = self.kwargs.get('id'),checkout = False)
            cart.quantity -= 1
            cart.save(update_fields=['quantity'])
        
        except DataError:
            messages.warning(request=request,message='Out of range, pls delete the product from you cart or add one')
        
        except ObjectDoesNotExist:
            messages.error(request=request,message='Does not exist')


        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class UserCartDeleteView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):

        get_object_or_404(Cart,user = self.request.user,id = self.kwargs.get('id'),checkout = False).delete()
        return redirect('base:cart')
    
class UserCartCheckoutView(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        carts = Cart.objects.filter(user = self.request.user,checkout=False)
        product_ids = carts.values_list('product_id', flat=True)
        products = TheProduct.objects.filter(id__in = product_ids)

        for product,cart in zip(products,carts):
            cart.checkout = True
            product.quantity -= cart.quantity
            product.sold_quantity += cart.quantity
            product.quantity_check()
        
        Cart.objects.bulk_update(carts, ['checkout'])
        TheProduct.objects.bulk_update(products, ['sold_quantity','quantity','availability'])
        
        return HttpResponseRedirect(reverse('base:home'))
    
class UserCartView(LoginRequiredMixin,ListView):
    template_name = 'base/cart.html'
    context_object_name = 'carts'

    def get_queryset(self):
        global carts
        carts = Cart.objects.filter(user=self.request.user,checkout = False)
        return carts
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_ids = [product.product_id for product in carts]
        products = TheProduct.objects.filter(id__in=product_ids)
        totaL_carts_price = [cart.total_cart_price for cart in carts]
        context['product'] = products
        context['total'] = sum(totaL_carts_price)
        return context

"""End of Cart Views"""
    
class NewArrivalsView(PageDataMixin,BaseShopView):

    def get_queryset(self):
        return TheProduct.objects.new_arrivals()
    
class MostViewedProducts(PageDataMixin,BaseShopView):

    def get_queryset(self):
        #gets the most viewed products
        return TheProduct.objects.most_viewed_products()
    
class MostRatedProducts(PageDataMixin,BaseShopView):

    def get_queryset(self):
        return TheProduct.objects.most_rated_products()