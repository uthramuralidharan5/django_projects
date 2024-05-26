from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Portfolio, Project
from .forms import UserProfileForm, PortfolioForm, ProjectForm

@login_required
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'profiles/user_profile.html', {'form': form})

@login_required
def portfolio_list(request):
    portfolios = Portfolio.objects.filter(user_profile__user=request.user)
    return render(request, 'profiles/portfolio_list.html', {'portfolios': portfolios})

@login_required
def portfolio_create(request):
    if request.method == 'POST':
        form = PortfolioForm(request.POST)
        if form.is_valid():
            portfolio = form.save(commit=False)
            profile = UserProfile.objects.get(user=request.user)
            portfolio.user_profile = profile
            portfolio.save()
            return redirect('portfolio_list')
    else:
        form = PortfolioForm()
    return render(request, 'profiles/portfolio_form.html', {'form': form})

@login_required
def portfolio_detail(request, pk):
    portfolio = get_object_or_404(Portfolio, pk=pk)
    projects = Project.objects.filter(portfolio=portfolio)
    return render(request, 'profiles/portfolio_detail.html', {'portfolio': portfolio, 'projects': projects})

@login_required
def project_create(request, portfolio_pk):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.portfolio = portfolio
            project.save()
            return redirect('portfolio_detail', pk=portfolio.pk)
    else:
        form = ProjectForm()
    return render(request, 'profiles/project_form.html', {'form': form, 'portfolio': portfolio})
