from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),

    # Category + Voting
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('vote/<int:nominee_id>/', views.vote_nominee, name='vote'),
    path('results/<int:category_id>/', views.results, name='results'),

    # Auth
    path('signup/', views.signup_view, name='signup'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('contact/', views.contact_view, name='contact'),
]