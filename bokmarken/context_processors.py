from django.conf import settings


def footer_message(request):
    return {'footer_message': settings.BOKMARKEN_FOOTER_MESSAGE}
