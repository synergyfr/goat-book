from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views.generic import FormView, CreateView, DetailView

from lists.models import Item, List
from lists.forms import ExistingListItemForm, ItemForm

User = get_user_model()


class HomePageView(FormView):
    template_name = 'home.html'
    form_class = ItemForm


def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=our_list, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(our_list)
    else:
        form = ExistingListItemForm(for_list=our_list)
    return render(
        request,
        'list.html',
        {
            'list': our_list,
            'form': form
        })


class NewListView(CreateView, HomePageView):

    def form_valid(self, form):
        list_ = List.objects.create()
        if self.request.user.is_authenticated:
            list_.owner = self.request.user
            list_.save()
        form.save(for_list=list_)
        return redirect(list_)


class ViewAndAddToList(DetailView, CreateView):

    model = List
    template_name = 'list.html'
    form_class = ExistingListItemForm

    def get_form(self):
        self.object = self.get_object()
        return self.form_class(for_list=self.object, data=self.request.POST)


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        nulist = List.objects.create()
        if request.user.is_authenticated:
            nulist.owner = request.user
            nulist.save()
        form.save(for_list=nulist)
        return redirect(nulist)
    else:
        return render(request, 'home.html', {'form': form})


def my_lists(request, email):
    owner = User.objects.get(email=email)
    return render(request, 'my_lists.html', {'owner': owner})


def share_list(request, list_id):
    mylist = List.objects.get(id=list_id)
    email = request.POST.get('sharee')
    user = User.objects.filter(email=email).first()
    if user:
        mylist.shared_with.add(user)
    return redirect(mylist)
