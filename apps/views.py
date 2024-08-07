from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from decimal import Decimal
from django.contrib.auth import get_user_model
from .models import Cosmetic, Category, Order, Cart, CartItem
from .forms import MyUpdateForm, CosmeticAddForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

User = get_user_model()


def index_views(request):
    cosmetics = Cosmetic.objects.filter(is_active=True)[::-1][:3]

    if request.method == 'POST':
        form = CosmeticAddForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Успешно создана')
    form = CosmeticAddForm()

    return render(
        request=request,
        template_name='cosmo/index.html',
        context={
            'cosmetics':cosmetics,
            'form': form
        }
    )


def detail_views(request,pk):
    cosmetic = get_object_or_404(Cosmetic,id=pk)

    recommendations = Cosmetic.objects.filter(category=cosmetic.category)

    if request.method == 'POST':
        if 'delete' in request.POST:
            cosmetic.delete()
            messages.success(request,'Успешно удалено')
            return redirect('index')

        form = MyUpdateForm(request.POST,request.FILES,instance=cosmetic)
        if form.is_valid():
            form.save()
            messages.success(request, 'Успешно изменено')

        if 'product' and 'title' and 'price' in request.POST:
            messages.success(request, 'Товар успешно добавлен в корзину')

    form = MyUpdateForm(instance=cosmetic)

    return render(
        request=request,
        template_name='cosmo/shop-detail.html',
        context={
            'cosmetic': cosmetic,
            'recommendations': recommendations,
            'form': form,
        }
    )


def shop_view(request):
    cosmetics = Cosmetic.objects.filter(is_active=True).order_by('-id')  # Сортировка по убыванию ID
    paginator = Paginator(cosmetics, 6)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(
        request=request,
        template_name='cosmo/shop.html',
        context={
            'cosmetics': page_obj,
            'page_obj': page_obj,
            'page_range': paginator.page_range
        }
    )


def add_to_cart(request, pk):
    if request.method == 'POST':
        cosmetic = get_object_or_404(Cosmetic, pk=pk)
        quantity = int(request.POST.get('quantity', 1))
        price_str = request.POST.get('price', str(cosmetic.price))

        # Replace comma with period for decimal conversion
        price_str = price_str.replace(',', '.')

        try:
            price = Decimal(price_str)
        except (ValueError, ArithmeticError):
            messages.error(request, 'Invalid price format')
            return redirect('shop')

        # Retrieve or create a cart for the user
        cart, created = Cart.objects.get_or_create(user=request.user, defaults={'total_price': Decimal('0.00')})

        # Retrieve or create a cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            cosmetic=cosmetic,
            defaults={'quantity': quantity, 'price': price}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        # Update cart total price
        cart.total_price += price * quantity
        cart.save()

        messages.success(request, 'Товар успешно добавлен в корзину')
        return redirect('shop')
    else:
        return redirect('shop')


def view_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.all()

    context = {
        'cart': cart,
        'cart_items': cart_items,
    }

    return render(request, 'cosmo/cart.html', context)


def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    cart.total_price -= cart_item.price * cart_item.quantity
    cart.save()

    cart_item.delete()

    messages.success(request, 'Товар удален из корзины')
    return redirect('view_cart')


def get_cart_data(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        return JsonResponse({'items': [], 'total_price': 0})

    items = []
    total_price = 0
    for item in cart.items.all():
        item_data = {
            'id': item.id,
            'title': item.cosmetic.title,
            'image_url': item.cosmetic.image.url if item.cosmetic.image else '',
            'quantity': item.quantity,
            'price': float(item.price),
            'total_price': float(item.price * item.quantity),
        }
        total_price += item_data['total_price']
        items.append(item_data)

    return JsonResponse({'items': items, 'total_price': total_price})


def create_order(request):
    if request.method == 'POST':
        user = get_object_or_404(User, id=request.user.id)
        cart = get_object_or_404(Cart, user=user)
        print(user.wallet, cart.total_price)
        print(f"Cart total price: {cart.total_price}")

        # Проверяем, есть ли товары в корзине
        if not cart.items.exists():
            messages.error(request, 'Ваша корзина пуста.')
            return redirect('index')

        # Проверяем, достаточно ли средств на счете
        if user.wallet >= cart.total_price:
            # Списываем средства и создаем заказ
            user.wallet -= cart.total_price
            user.save()

            order = Order(
                cart=cart,
                user=user,
                total_price=cart.total_price
            )
            order.save()

            # Очищаем корзину после создания заказа
            CartItem.objects.filter(cart=cart).delete()
            cart.total_price = 0
            cart.save()

            messages.success(request, f'Заказ успешно создан. С вашего баланса списано {cart.total_price} сом.')
        else:
            messages.error(request, 'На вашем балансе недостаточно средств.')

        return redirect('index')

    return redirect('index')

