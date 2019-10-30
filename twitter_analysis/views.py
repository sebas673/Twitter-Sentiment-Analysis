from django.shortcuts import render
from .models import Campaign
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .sentiment import sentiment_by_keyword


def home(request):
    context = {
        'campaigns': Campaign.objects.filter(user=request.user)
    }
    return render(request, 'twitter_analysis/home.html', context)


class CampaignListView(ListView):
    model = Campaign
    template_name = 'twitter_analysis/home.html'
    context_object_name = 'campaigns'


class CampaignDetailView(DetailView):
    model = Campaign
    context_object_name = 'campaign'


class CampaignCreateView(LoginRequiredMixin, CreateView):
    model = Campaign
    fields = ['name', 'description', 'keyword0']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CampaignUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Campaign
    fields = ['name', 'description', 'keyword0']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        campaign = self.get_object()
        if self.request.user == campaign.owner:
            return True
        return False


class CampaignDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Campaign
    context_object_name = 'campaign'
    success_url = '/'

    def test_func(self):
        campaign = self.get_object()
        if self.request.user == campaign.owner:
            return True
        return False


def about(request):
    return render(request, 'twitter_analysis/about.html')
