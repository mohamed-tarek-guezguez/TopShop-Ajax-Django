from django.shortcuts import render
from .models import Product, Review
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def products(request):
    context = {

    }
    return render(request, 'storeApp/products.html', context)

def fetchProducts(request):
    q = request.GET.get('q', None)
    if q == '':
        products = list(Product.objects.values().order_by('-id'))
    else:
        words = q.split(" ")
        q_filters = Q()
        for word in words:
            q_filters |= Q(Title__icontains=word)
        products = list(Product.objects.values().filter(q_filters).order_by('-id'))

    paginator = Paginator(products, 8)
    page = request.GET.get('page', 1)

    try:
        prods = paginator.page(page)
    except(EmptyPage, InvalidPage):
        prods = paginator.page(1)

    products = list(prods)

    number = prods.number

    page_rangeStart = prods.paginator.page_range.start
    if (int(page_rangeStart) < int(number) - 3):
        page_rangeStart = number - 3

    page_rangeEnd = prods.paginator.page_range.stop
    if (int(page_rangeEnd) > int(number) + 3):
        page_rangeEnd = number + 4

    return JsonResponse({
        "products": products,
        "num_pages": paginator.num_pages,
        "has_previous": prods.has_previous(),
        "has_next": prods.has_next(),
        "page_rangeStart": page_rangeStart,
        "page_rangeEnd": page_rangeEnd,
        'page': number
    })

def details(request, slug):
    product = Product.objects.get(Slug=slug)
    reviews = Review.objects.filter(post_connected=product).order_by('-id')

    context = {
        "product": product,
        "reviews": reviews
    }

    if request.user.is_authenticated:
        author = User.objects.get(username=request.user.username)

        exists = False
        if Review.objects.filter(post_connected=product, user=author).exists():
            exists = True

        context['exists'] = exists

    return render(request, 'storeApp/productDetails.html', context)

@login_required
def addReview(request):
    slug = request.POST.get('slug', None)
    rating = request.POST.get('rating', None)
    comment = request.POST.get('comment', None)

    product = Product.objects.get(Slug=slug)
    author = User.objects.get(username=request.user.username)

    exists = False
    if Review.objects.filter(post_connected=product, user=author).exists():
        review = Review.objects.get(post_connected=product, user=author)
        review.rating = rating
        review.comment = comment
        review.save()
        exists = True
    else:
        Review(
            user = author,
            rating = rating,
            comment = comment,
            post_connected = product
        ).save()
    product.save()

    reviews = list(Review.objects.values().filter(post_connected=product).order_by('-id'))

    return JsonResponse({
        "number_of_reviews": product.number_of_reviews,
        "totalRating": product.totalRating,
        "reviews": reviews,
        "exists": exists
    })