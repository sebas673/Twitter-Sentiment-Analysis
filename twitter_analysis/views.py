from django.shortcuts import render, redirect
from .models import Campaign
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .sentiment import sentiment


def home(request):
    if request.user.is_authenticated:
        user = request.user
        context = {
            'campaigns': Campaign.objects.all().filter(owner=user)
        }
        return render(request, 'twitter_analysis/home.html', context)
    else:
        # return redirect('login')
        return render(request, 'twitter_analysis/homepage.html')


class CampaignListView(ListView):
    model = Campaign
    # template_name = 'twitter_analysis/campaign_see_more.html'
    template_name = 'twitter_analysis/campaign_see_more.html'
    # context_object_name = 'campaigns'

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        campaign = Campaign.objects.get(id=pk)

        context['posIDs'] = campaign.posIDs
        context['negIDs'] = campaign.negIDs
        context['keyword'] = campaign.keyword0

        return context


class CampaignDetailView(DetailView):
    model = Campaign
    context_object_name = 'campaign'


class CampaignCreateView(LoginRequiredMixin, CreateView):
    model = Campaign
    fields = ['name', 'keyword0', 'id_list', 'description']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CampaignUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Campaign
    fields = ['name', 'keyword0', 'id_list', 'description']

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
