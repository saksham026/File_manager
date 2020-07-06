from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Filee
import operator
from django.urls import reverse_lazy
from django.contrib.staticfiles.views import serve

from django.db.models import Q


def home(request):
    return render(request, 'upload/home.html')

def search(request):
    template='upload/search.html'

    query=request.GET.get('q')

    result=Filee.objects.filter(Q(title__icontains=query) | Q(author__username__icontains=query) | Q(content__icontains=query))
    paginate_by=2
    context={ 'files':result }
    return render(request,template,context)
   


def getfile(request):
   return serve(request, 'File')


class FileListView(ListView):
    model = Filee
    template_name = 'upload/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'files'
    ordering = ['-date_posted']
    paginate_by = 2


class UserFileListView(ListView):
    model = Filee
    template_name = 'upload/user_files.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'files'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Filee.objects.filter(author=user).order_by('-date_posted')


class FileDetailView(DetailView):
    model = Filee
    template_name = 'upload/file_detail.html'


class FileCreateView(LoginRequiredMixin, CreateView):
    model = Filee
    template_name = 'upload/file_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class FileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Filee
    template_name = 'upload/file_form.html'
    fields = ['title', 'content', 'file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        file = self.get_object()
        if self.request.user == file.author:
            return True
        return False


class FileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Filee
    success_url = '/'
    template_name = 'upload/file_confirm_delete.html'

    def test_func(self):
        file = self.get_object()
        if self.request.user == file.author:
            return True
        return False


def about(request):
    return render(request, 'upload/about.html', {'title': 'About'})
