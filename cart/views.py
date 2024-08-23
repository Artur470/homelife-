from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from product.models import Product
from .serializers import CartItemsSerializer, OrderSerializer
from drf_yasg.utils import swagger_auto_schema

class CartView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['cart'],
        operation_description="Получить список товаров в корзине пользователя."
    )
    def get(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user, ordered=False).first()
        if not cart:
            return Response({'error': 'Cart not found'}, status=404)
        queryset = CartItem.objects.filter(cart=cart)
        serializer = CartItemsSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=['cart'],
        operation_description="Добавить товар в корзину пользователя."
    )
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user, ordered=False)

        product = get_object_or_404(Product, id=data.get('product'))
        quantity = int(data.get('quantity', 1))

        if quantity <= 0:
            return Response({'error': 'Quantity must be greater than 0'}, status=400)

        if quantity > product.quantity:
            return Response({'error': 'Not enough stock available'}, status=400)

        # Calculate the price with promotion if applicable
        price = product.price
        promotion = product.promotion or 0
        if promotion > 0:
            price *= (1 - promotion / 100)

        # Get or create the CartItem
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'price': price, 'quantity': quantity, 'user': user}
        )

        if not created:
            # Update existing CartItem
            cart_item.quantity += quantity
            cart_item.price = price * cart_item.quantity
            cart_item.save()
        else:
            # Decrease product stock and save CartItem
            product.quantity -= quantity
            product.save()

        # Update cart total price
        cart.total_price = sum(item.price for item in CartItem.objects.filter(cart=cart))
        cart.save()

        return Response({'success': 'Item added to your cart'})

    @swagger_auto_schema(
        tags=['cart'],
        operation_description="Изменить/обновить товар в корзине пользователя."
    )
    def put(self, request):
        data = request.data
        cart_item = get_object_or_404(CartItem, id=data.get('id'))
        new_quantity = int(data.get('quantity'))

        if new_quantity <= 0:
            return Response({'error': 'Quantity must be greater than 0'}, status=400)

        product = cart_item.product
        price = product.price
        promotion = product.promotion or 0
        if promotion > 0:
            price *= (1 - promotion / 100)

        # Update the CartItem with the new quantity
        cart_item.quantity = new_quantity
        cart_item.price = price * new_quantity
        cart_item.save()

        # Adjust product stock
        old_quantity = CartItem.objects.get(id=cart_item.id).quantity
        product.quantity += old_quantity - new_quantity
        product.save()

        # Update cart total price
        cart = cart_item.cart
        cart.total_price = sum(item.price for item in CartItem.objects.filter(cart=cart))
        cart.save()

        return Response({'success': 'Product updated'})

    @swagger_auto_schema(
        tags=['cart'],
        operation_description="Удалить товар из корзины пользователя."
    )
    def delete(self, request):
        user = request.user
        data = request.data

        cart_item = get_object_or_404(CartItem, id=data.get('id'))
        cart = cart_item.cart

        # Increase the stock of the product
        product = cart_item.product
        product.quantity += cart_item.quantity
        product.save()

        cart_item.delete()

        # Update cart total price
        if CartItem.objects.filter(cart=cart).exists():
            queryset = CartItem.objects.filter(cart=cart)
            serializer = CartItemsSerializer(queryset, many=True)
            cart.total_price = sum(item.price for item in CartItem.objects.filter(cart=cart))
            cart.save()
            return Response(serializer.data)
        else:
            # If no items left in the cart, set the total_price to 0
            cart.total_price = 0
            cart.save()
            return Response({'success': 'Item removed from your cart'})
class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['order'],
        operation_description="Создать заказ из корзины пользователя."
    )
    def post(self, request):
        user = request.user
        cart = Cart.objects.filter(user=user, ordered=False).first()

        if not cart:
            return Response({'error': 'Cart not found or already ordered'}, status=400)

        order = Order.objects.create(
            user=user,
            cart=cart,
            total_price=cart.total_price
        )

        # Предполагается, что метод send_order_email() существует и корректно реализован
        order.send_order_email()

        cart.ordered = True
        cart.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=201)
