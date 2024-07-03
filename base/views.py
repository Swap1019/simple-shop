from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404,redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import ListView,DetailView,View,DeleteView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TheProduct,PagePic,Cart
from django.db.models import Q
from user.models import User
from user.forms import ReportProductForm

class Home(ListView):
    template_name = 'base/list_page.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        #gets the most viewed products that were created by the user
        return TheProduct.objects.availables()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the background_pic to the context
        context['background_pic'] = PagePic.objects.get().website_pic
        if self.request.user.is_authenticated:
            context['user_profile'] = User.objects.get(pk=self.request.user.pk).profile
            context['username'] = User.objects.get(pk=self.request.user.pk).username
            context['cart'] = Cart.objects.filter(user=self.request.user,deleted=False)
            context['quantity'] = context['cart'].count()
        return context
    
class HomeSearch(ListView):
    model = TheProduct
    template_name = 'base/list_page.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('SearchQuery')
        return TheProduct.objects.filter(
            Q(product__icontains=query) |
            Q(tags__name__icontains=query),
            availability='A'
        ).order_by('-hits').distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the background_pic to the context
        context['background_pic'] = PagePic.objects.get().website_pic
        if self.request.user.is_authenticated:
            context['user_profile'] = User.objects.get(pk=self.request.user.pk).profile
            context['username'] = User.objects.get(pk=self.request.user.pk).username
            context['cart'] = Cart.objects.filter(user=self.request.user,deleted=False)
            context['quantity'] = context['cart'].count()
        return context
    
class Product(FormMixin,DetailView):
    template_name = 'base/view_product.html'
    context_object_name = 'product'
    model = TheProduct
    form_class = ReportProductForm
    #gets the specified product
    def get_object(self):
        product = get_object_or_404(TheProduct,id=self.kwargs.get('id'))
        ip_address = self.request.user.ip_address
        if ip_address not in product.hits.all():
            product.hits.add(ip_address)
        return product

    #returns the related product
    def get_context_data(self, *args, **kwargs):
        context = super(Product, self).get_context_data(*args, **kwargs)
        product = context['product']
        categories = product.category.all()  # Assuming a product can belong to multiple categories
        related_products = TheProduct.objects.filter(category__in=categories).exclude(id=product.id)
        context['related_products'] = related_products
        context['form'] = ReportProductForm(initial={'post': self.object})

        if self.request.user.is_authenticated:
            context['user_profile'] = User.objects.get(pk=self.request.user.pk).profile
            context['username'] = User.objects.get(pk=self.request.user.pk).username
            context['cart'] = Cart.objects.filter(user=self.request.user,deleted=False)
            context['quantity'] = context['cart'].count()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        user_id = User.objects.get(pk = self.request.user.pk)
        product = TheProduct.objects.get(id = self.kwargs.get('id'))
        #insert user_id and product into form
        form.instance.user = user_id
        form.instance.reported_product = product
        form.instance.id = product.pk
        form.save()
        return super(Product, self).form_valid(form)
    
    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Product Reported Successfuly')
        return reverse('base:product', kwargs={'id': self.kwargs.get('id')})
    
"""Cart Views"""
class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        product_id = kwargs.get('id')
        
        cart_product_price = TheProduct.objects.get(id=product_id).final_price
        Cart.objects.get_or_create(user = user, product_id = product_id,cart_product_price=cart_product_price)

        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
class IncreaseUpdateCartView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        user = self.request.user

        cart = Cart.objects.get(user = user, id = id)
        cart.quantity += 1
        cart.save(update_fields=['quantity'])

        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class DecreaseUpdateCartView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('id')
        user = self.request.user

        cart = Cart.objects.get(user = user, id = id)
        cart.quantity -= 1
        cart.save(update_fields=['quantity'])
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

class UserCartDeleteView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        id=self.kwargs.get('id')
        user=self.request.user

        get_object_or_404(Cart,user = user,id = id).delete()
        return redirect('base:cart')
    
class UserCartView(LoginRequiredMixin,ListView):
    template_name = 'base/cart.html'
    context_object_name = 'carts'

    def get_queryset(self):
        global carts
        carts = Cart.objects.filter(user=self.request.user,deleted=False)
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
    
class NewArrivalsView(ListView):
    template_name = 'base/list_page.html'
    context_object_name = 'products'
    queryset = TheProduct.objects.new_arrivals()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the background_pic to the context
        context['background_pic'] = PagePic.objects.get().website_pic

        if self.request.user.is_authenticated:
            context['user_profile'] = User.objects.get(pk=self.request.user.pk).profile
            context['username'] = User.objects.get(pk=self.request.user.pk).username
            context['cart'] = Cart.objects.filter(user=self.request.user,deleted=False)
            context['quantity'] = context['cart'].count()
        return context
    
class MostViewedProducts(ListView):
    template_name = 'base/list_page.html'
    context_object_name = 'products'

    def get_queryset(self):
        #gets the most viewed products
        return TheProduct.objects.most_viewed_products()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the background_pic to the context
        context['background_pic'] = PagePic.objects.get().website_pic

        if self.request.user.is_authenticated:
            context['user_profile'] = User.objects.get(pk=self.request.user.pk).profile
            context['username'] = User.objects.get(pk=self.request.user.pk).username
            context['cart'] = Cart.objects.filter(user=self.request.user,deleted=False)
            context['quantity'] = context['cart'].count()
        return context
    
class MostRatedProducts(ListView):
    template_name = 'base/list_page.html'
    context_object_name = 'products'

    def get_queryset(self):
        return TheProduct.objects.most_rated_products()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the background_pic to the context
        context['background_pic'] = PagePic.objects.get().website_pic
        if self.request.user.is_authenticated:
            context['user_profile'] = User.objects.get(pk=self.request.user.pk).profile
            context['username'] = User.objects.get(pk=self.request.user.pk).username
            context['cart'] = Cart.objects.filter(user=self.request.user,deleted=False)
            context['quantity'] = context['cart'].count()
        return context