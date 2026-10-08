from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import FlowerForm
from .models import Flower


def create_account(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()

    return render(request, 'Inventory/create_account.html', {'form': form})


@login_required
def index(request):
    query = request.GET.get('q', '').strip()
    flower_type = request.GET.get('type', '').strip()
    products = Flower.objects.all().order_by('-date_added')

    if query:
        products = products.filter(
            Q(flower_name__icontains=query)
            | Q(flower_type__icontains=query)
            | Q(color__icontains=query)
            | Q(description__icontains=query)
        )
    if flower_type:
        products = products.filter(flower_type=flower_type)

    return render(request, 'Inventory/home.html', {
        'products': products,
        'query': query,
        'selected_type': flower_type,
        'flower_types': Flower.FLOWER_TYPE,
        'total_flowers': Flower.objects.count(),
        'total_quantity': sum(
            Flower.objects.values_list('quantity', flat=True)
        ),
    })


@login_required
def profile(request):
    return render(request, 'Inventory/profile.html')


@login_required
def save_flower(request, product_id=None):
    flower = get_object_or_404(Flower, product_id=product_id) if product_id else None

    if request.method == 'POST':
        form = FlowerForm(request.POST, instance=flower)
        if form.is_valid():
            saved_flower = form.save()
            action = 'updated' if flower else 'saved'
            messages.success(
                request,
                f'{saved_flower.flower_name} was {action} successfully.',
            )
            return redirect('index')
    else:
        form = FlowerForm(instance=flower)

    return render(request, 'Inventory/flower_form.html', {
        'form': form,
        'flower': flower,
    })


@login_required
def delete_flower(request, product_id):
    flower = get_object_or_404(Flower, product_id=product_id)
    if request.method != 'POST':
        return render(request, 'Inventory/flower_delete.html', {'flower': flower})

    name = flower.flower_name
    flower.delete()
    messages.success(request, f'{name} was removed from your inventory.')
    return redirect('index')
