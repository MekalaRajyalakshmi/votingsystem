from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Category, Nominee, UserVote

# Home Page - List all categories (login required)
@login_required
def home(request):
    categories = Category.objects.all()
    return render(request, 'home.html', {'categories': categories})

# View nominees in a category
@login_required
def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    nominees = category.nominee_set.all()
    has_voted = UserVote.objects.filter(user=request.user, category=category).exists()
    return render(request, 'category_detail.html', {
        'category': category,
        'nominees': nominees,
        'has_voted': has_voted,
    })

# Voting view
@login_required
def vote_nominee(request, nominee_id):
    nominee = get_object_or_404(Nominee, id=nominee_id)
    user = request.user
    category = nominee.category

    if UserVote.objects.filter(user=user, category=category).exists():
        messages.error(request, "Already voted in this category!")
        return redirect('category_detail', category.id)

    nominee.votes += 1
    nominee.save()
    UserVote.objects.create(user=user, category=category, nominee=nominee)
    messages.success(request, f"You voted for {nominee.name}!")
    return redirect('results', category.id)

# Results page for a category
@login_required
def results(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    nominees = Nominee.objects.filter(category=category)
    total_votes = sum(n.votes for n in nominees)

    results_data = []
    for nominee in nominees:
        vote_count = nominee.votes
        percentage = (vote_count / total_votes) * 100 if total_votes > 0 else 0
        results_data.append({
            "nominee": nominee,
            "votes": vote_count,
            "percentage": round(percentage, 2),
        })

    return render(request, "results.html", {
        "category": category,
        "results": results_data,
        "total_votes": total_votes,
    })

# Signup view (auto login after signup)
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')

        user = User.objects.create_user(username=username, password=password)
        login(request, user)  # auto login new user
        messages.success(request, "Account created successfully!")
        return redirect('home')

    return render(request, 'signup.html')

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')

    return render(request, 'login.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')
# Contact page
def contact_view(request):
    return render(request, 'contact.html')