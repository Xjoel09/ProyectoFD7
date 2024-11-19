from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Category, Product, Review
from .forms import CategoryForm, ProductForm,CustomUserCreationForm, CommentForm, ReviewForm





# Vista para crear una nueva cuenta o registrarse
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('main:home')  
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

#@login_required
def index(request):
    return render(request, 'main/index.html')

# Create your views here.
# Vista para crear una nueva categoría
def create_category(request):
    if request.method == 'POST':
        if 'cancel' in request.POST:
            # Redirige a la lista de productos en caso de cancelación
            return redirect('main:category_list')
        elif 'save' in request.POST:
            # Lógica para guardar el producto
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('main:category_list')

    else:
        form = CategoryForm()
    
    return render(request, 'main/create_category.html', {'form': form})

# Vista para editar una categoría existente
def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    
    if request.method == 'POST':
        if 'delete' in request.POST:
            # Lógica para eliminar la categoría
            category.delete()
            return redirect('main:category_list')
        elif 'cancel' in request.POST:
            # Redirige a la lista de categorías en caso de cancelación
            return redirect('main:category_list')
        elif 'save' in request.POST:
            # Lógica para guardar la categoría
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                return redirect('main:category_list')
    else:
        form = CategoryForm(instance=category)
        
    return render(request, 'main/edit_category.html', {'form': form, 'category': category})

# Vista para eliminar una categoría
def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    
    if request.method == 'POST':
        category.delete()
        return redirect('main:category_list')  # Redirigir a la lista de categorías
    
    return render(request, 'main/delete_category.html', {'category': category})

# Vista para ver la lista de categorías
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'main/category_list.html', {'categories': categories})

# Vista para crear un nuevo producto
def create_product(request):
    if request.method == 'POST':
        if 'cancel' in request.POST:
            # Redirige a la lista de productos en caso de cancelación
            return redirect('main:product_list')
        elif 'save' in request.POST:
            # Lógica para guardar el producto
            form = ProductForm(request.POST, request.FILES )
            if form.is_valid():
                form.save()
                return redirect('main:product_list')
    else:
        form = ProductForm()
    categories = Category.objects.all()  # Obtén todas las categorías
    return render(request, 'main/create_product.html', {'form': form, 'categories': categories})

# Vista para editar un producto existente
def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        if 'delete' in request.POST:
            # Lógica para eliminar el producto
            product.delete()
            return redirect('main:product_list')
        elif 'cancel' in request.POST:
            # Redirige a la lista de productos en caso de cancelación
            return redirect('main:product_list')
        elif 'save' in request.POST:
            # Lógica para guardar el producto
            form = ProductForm(request.POST,request.FILES, instance=product)
            if form.is_valid():
                form.save()
                return redirect('main:product_list')
    else:
        form = ProductForm(instance=product)
        
    categories = Category.objects.all()  # Obtén todas las categorías
    return render(request, 'main/edit_product.html', {'form': form, 'product': product, 'categories': categories})

# Vista para eliminar un producto
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        product.delete()
        return redirect('main:product_list')  # Redirigir a la lista de productos
    
    return render(request, 'main/delete_product.html', {'product': product})

# Vista para ver la lista de productos
def product_list(request):
    # Obtén todas las categorías para construir el menú desplegable
    categories = Category.objects.all()

    # Inicializa una variable para almacenar la categoría seleccionada (por defecto, ninguna)
    selected_category_id = None
    selected_category_name = "Todos"  # Nombre por defecto para el botón

    if request.method == 'GET':
        # Obtiene el ID de la categoría seleccionada del formulario
        selected_category_id = request.GET.get('category')
        # Si se selecciona una categoría, obtén su nombre
        if selected_category_id:
            selected_category = Category.objects.get(id=selected_category_id)
            selected_category_name = selected_category.name

    # Filtra los productos según la categoría seleccionada (si hay alguna)
    if selected_category_id:
        products = Product.objects.filter(category_id=selected_category_id)
    else:
        # Si no se selecciona ninguna categoría, muestra todos los productos
        products = Product.objects.all()

    return render(request, 'main/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category_id': selected_category_id,
        'selected_category_name': selected_category_name  # Agregamos el nombre de la categoría seleccionada
    })
    
from .forms import CommentForm

# Vista para ver los detalles de los productos
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product=product)

    return render(request, 'main/product_detail.html', {
        'product': product,
        'reviews': reviews,
    })

# Vista para agregar una review
@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            rating = form.cleaned_data['rating']

            # Obtén el nombre de usuario del usuario actual
            user_name = request.user.username

            # Crea la revisión y asigna el nombre de usuario
            review = Review.objects.create(product=product, user=request.user, comment=comment, rating=rating)

            return redirect('main:product_detail', product_id=product_id)
    else:
        form = ReviewForm()

    return render(request, 'main/add_review.html', {'product': product, 'form': form})
