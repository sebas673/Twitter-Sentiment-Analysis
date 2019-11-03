from django.urls import path
from . import views
from .views import (
    #     CampaignListView,
    CampaignDetailView,
    CampaignCreateView,
    CampaignUpdateView,
    CampaignDeleteView
)

urlpatterns = [
    #     path('', CampaignListView.as_view(), name='twitter_analysis-home'),
    path('', views.home, name='twitter_analysis-home'),
    path('campaign/<int:pk>/', CampaignDetailView.as_view(),
         name='campaign-detail'),
    path('campaign/new/', CampaignCreateView.as_view(),
         name='campaign-create'),
    path('campaign/<int:pk>/update/', CampaignUpdateView.as_view(),
         name='campaign-update'),
    path('campaign/<int:pk>/delete/', CampaignDeleteView.as_view(),
         name='campaign-delete'),
    path('about/', views.about, name='twitter_analysis-about'),
]
