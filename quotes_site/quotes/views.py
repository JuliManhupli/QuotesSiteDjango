from collections import Counter

from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.shortcuts import render, redirect
from itertools import chain
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import AuthorForm, QuoteForm
from .models import Quote, Author


def paginate_quotes(request, quotes):
    quotes_per_page = 10
    paginator = Paginator(quotes, quotes_per_page)
    page = request.GET.get('page')

    try:
        paginated_quotes = paginator.page(page)
    except PageNotAnInteger:
        paginated_quotes = paginator.page(1)
    except EmptyPage:
        paginated_quotes = paginator.page(paginator.num_pages)

    return paginated_quotes


def all_quotes(request):
    quotes = Quote.objects.all()
    paginated_quotes = paginate_quotes(request, quotes)
    return render(request, "quotes/index.html", context={'quotes': paginated_quotes})


def tag(request, tag):
    quotes = Quote.objects.filter(tags__contains=[tag])
    paginated_quotes = paginate_quotes(request, quotes)
    return render(request, "quotes/index.html", context={'quotes': paginated_quotes})


def author(request, author):
    author = Author.objects.get(fullname=author)
    return render(request, "quotes/author.html", context={'author': author})


def top_tags(request):
    all_tags = list(chain.from_iterable(Quote.objects.exclude(tags__isnull=True).values_list('tags', flat=True)))
    tag_counts = Counter(all_tags)
    top_tags = tag_counts.most_common(10)
    return render(request, "quotes/top_tags.html", context={'top_tags': top_tags})


@login_required
def add_author(request):
    form = AuthorForm(instance=Author())
    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES, instance=Author())
        if form.is_valid():
            author = form.save(commit=False)
            author.save()
            messages.success(request, f"Author added successfully!")
            return redirect(to="quotes:home")
    return render(request, 'quotes/author_form.html', context={"form": form})


@login_required
def add_quotes(request):
    form = QuoteForm(instance=Quote())
    if request.method == 'POST':
        form = QuoteForm(request.POST, request.FILES, instance=Quote())
        if form.is_valid():
            quote = form.save(commit=False)
            quote.save()
            messages.success(request, f"Quote added successfully!")
            return redirect(to="quotes:home")
    return render(request, 'quotes/quotes_form.html', context={"form": form})
