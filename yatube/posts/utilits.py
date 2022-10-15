from django.core.paginator import Paginator


def paginator_func(request, *args):
    paginator = Paginator(*args)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
