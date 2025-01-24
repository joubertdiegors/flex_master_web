from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from products.models import Product
from promotions.models import Promotion
from categories.models import Category
from .mixins import CartMixin

from django.http import JsonResponse


class CartDetailView(CartMixin, View):
    template_name = 'cart_detail.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(parent__isnull=True).prefetch_related('subcategories')

        # cart = self.get_or_create_cart(request)
        cart = self.get_cart(request)

        # Se o carrinho não existir, retornar uma página vazia ou uma mensagem de "carrinho vazio"
        if not cart or not cart.items.exists():
            return render(request, self.template_name, {
                'categories': categories,
                'cart': None,
                'total_items': 0,
                'total_cost': 0.0,
                'is_not_list_page': True,
                'breadcrumb_off': True,
                'is_cart_detail_page': True,
                'message': 'Seu carrinho está vazio.'
            })

        # Calcular os totais
        total_items = sum(item.quantity for item in cart.items.all())
        total_cost = cart.get_total_cost()
        
        return render(request, self.template_name, {
            'categories': categories,
            'cart': cart,
            'total_items': total_items,
            'total_cost': total_cost,
            'is_not_list_page': True,
            'breadcrumb_off': True,
            'is_cart_detail_page': True,
        })

class AddToCartView(CartMixin, View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        cart = self.get_cart(request) or self.create_cart(request)
        # cart = self.get_or_create_cart(request)
        product = get_object_or_404(Product, id=product_id)

        # Verificar se o produto está em promoção
        promotion = Promotion.objects.filter(product=product).first()
        price = promotion.promotion_price if promotion else product.selling_price

        # Verificar se o item já existe no carrinho
        cart_items = CartItem.objects.filter(cart=cart, product=product)
        
        if cart_items.exists():
            cart_item = cart_items.first()  # Pegue o primeiro item
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(cart=cart, product=product, quantity=quantity, price=price)
        
        # Atualize o preço
        if promotion:
            cart_item.promotion = promotion
        else:
            cart_item.promotion = None
        cart_item.save()

        # Retornar dados atualizados para AJAX
        total_items = sum(item.quantity for item in cart.items.all())
        total_cost = cart.get_total_cost()
        

        return JsonResponse({
            'message': 'Produto adicionado ao carrinho',
            'cart_data': {
                'total_items': total_items,
                'total_cost': float(total_cost)
            }
        })

class UpdateCartItemQuantityView(CartMixin, View):  # Herda de CartMixin
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))

        # Obter o carrinho existente
        cart = self.get_cart(request)
        if not cart:
            return JsonResponse({'error': 'Carrinho não encontrado'}, status=400)

        # cart = self.get_or_create_cart(request)  # Isso agora funcionará
        
        # Verificar se o produto existe no carrinho
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if not cart_item:
            return JsonResponse({'error': 'Produto não encontrado no carrinho'}, status=400)
        
        # Atualizar a quantidade do item no carrinho
        # cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity = quantity
        cart_item.save()

        # Calcular o total do item atualizado
        # item_total = cart_item.quantity * cart_item.price

        # Calcular o total do item atualizado
        item_total = cart_item.get_cost()

        # Preparar dados do carrinho para resposta AJAX
        total_items = sum(item.quantity for item in cart.items.all())
        total_cost = cart.get_total_cost()

        return JsonResponse({
            'cart_data': {
                'item_total': float(item_total),
                'total_items': total_items,
                'total_cost': float(total_cost)
            }
        })

class RemoveFromCartView(CartMixin, View):
    def post(self, request, product_id, *args, **kwargs):
        # cart = self.get_or_create_cart(request)
         # Obter o carrinho existente
        cart = self.get_cart(request)
        if not cart:
            return JsonResponse({'error': 'Carrinho não encontrado'}, status=400)
        
        # Obter o item no carrinho
        product = get_object_or_404(Product, id=product_id)
        # cart_item = get_object_or_404(CartItem, cart=cart, product=product)
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if not cart_item:
            return JsonResponse({'error': 'Produto não encontrado no carrinho'}, status=400)
        
        # Remover completamente o item selecionado
        cart_item.delete()

        # Atualizar o total de itens e o custo total
        total_items = sum(item.quantity for item in cart.items.all())
        total_cost = cart.get_total_cost()

        # Retornar uma resposta JSON com os dados atualizados
        return JsonResponse({
            'cart_data': {
                'total_items': total_items,
                'total_cost': float(total_cost)
            }
        })
