from django.utils.deprecation import MiddlewareMixin

class LanguageMiddleware(MiddlewareMixin):
    def process_request(self, request):
        lang = (
            request.GET.get('lang')
            or request.headers.get('Accept-Language')
            or 'en'
        )
        request.lang = lang.split(',')[0].strip().lower()
