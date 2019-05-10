from Web.models import Page

def page(request):
    return {'pages':Page.objects.filter(is_active=True)}
