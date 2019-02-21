from django.core.paginator import Paginator
from django.shortcuts import render


class TemplateListView:
    def __init__(self, items_list, template, page=1, items_on_page=10):
        self.template = template
        self.items_list = items_list
        self.page = page
        self.items_on_page = items_on_page
        self.context = {}

    def add_extra(self, key, value):
        self.context[key] = value

    def render(self, request):
        paginator = Paginator(self.items_list, self.items_on_page)
        if not self.page in paginator.page_range:
            self.page = 1

        self.context['items_list'] = paginator.page(self.page).object_list
        self.context['paginator'] = paginator
        self.context['current_page'] = self.page

        return render(request, self.template, self.context)
