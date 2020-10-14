from django.views.generic import DetailView, ListView

from iarp_django_utils.pagination import paginator_helper

from .models import Item


class ItemListView(ListView):
    model = Item
    paginate_by = 5


class ItemCustomListView(ListView):
    model = Item

    def get_context_data(self, *args, **kwargs):
        kwargs = super().get_context_data(*args, **kwargs)
        kwargs.update(paginator_helper(
            context_key='object_list',
            queryset=Item.objects.order_by('-pk'),
            params=self.request.GET,
        ))
        return kwargs


class ItemDetailView(DetailView):
    model = Item

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update(paginator_helper(
            context_key='subitems_list',
            queryset=self.object.subitems.all(),
            params=self.request.GET,
        ))
        return kwargs
