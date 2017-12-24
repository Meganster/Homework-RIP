from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


def helloworld(request):
    now = "Helloworld"
    html = "<html><body> %s </body></html>" %now
    return HttpResponse(html)


