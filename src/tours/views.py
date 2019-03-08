from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.views.generic import edit
from django.contrib import messages
from django.urls import reverse_lazy

from .models import Tour
from profiles.models import Profile
from .scrap import get_flights

class ShowTours(generic.ListView):
    template_name = 'tours/tours.html'
    context_object_name = 'tour_list'

    def get_queryset(self):
        search_name = self.request.GET.get('search_name')
        search_value = self.request.GET.get('search_value')
        tours = Tour.objects.all()
        if search_name is not None:
            if search_name == "":
                return tours
            selected_tours = tours.filter(name=search_name)
            return selected_tours
        else:
            return tours

class TourCreate(edit.CreateView):
    model = Tour
    fields = ['name', 'description', 'value_adult', 'value_children', 'begin_date', 'end_date', 'places']
    success_url = reverse_lazy('home')


class TourDetail(generic.DetailView):
    model = Tour
    #a = get_flights()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['flights'] = ['1', '2', '3']
        return context


class TourDelete(edit.DeleteView):
    model = Tour
    success_url = reverse_lazy('home')


class TourEdit(edit.UpdateView):
    model = Tour
    fields = ['name', 'description', 'value_adult', 'value_children', 'begin_date', 'end_date', 'places']
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        tour = Tour.objects.get(pk=self.kwargs['pk'])
        return tour


def make_reserve(request, pk):
    # TODO: Do not reserve if already reserved
    user = request.user

    if user.is_authenticated:
        tour = Tour.objects.get(pk=pk)
        profile = Profile(user = user)
        reserves = profile.reserves
        if reserves.filter(id=tour.id).exists():
            messages.add_message(request, messages.INFO, 'Tour Already Reserved')
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            profile.reserves.add(tour)
            success_url = reverse_lazy('home')
            messages.add_message(request, messages.SUCCESS, 'Tour Reserved')
            return HttpResponseRedirect(reverse_lazy('home'))
    else:
        return HttpResponseRedirect(reverse_lazy('login'))

