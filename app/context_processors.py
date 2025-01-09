# app/context_processors.py

import os
from django.conf import settings

def get_logo_urls(request):
    logo_dir = os.path.join(settings.MEDIA_ROOT, 'store', 'logo')
    header_logo_url = None
    navbar_logo_url = None
    product_default_url = None
    favicon_url = None

    if os.path.exists(os.path.join(logo_dir, 'header_logo.png')):
        header_logo_url = settings.MEDIA_URL + 'store/logo/header_logo.png'

    if os.path.exists(os.path.join(logo_dir, 'navbar_logo.png')):
        navbar_logo_url = settings.MEDIA_URL + 'store/logo/navbar_logo.png'

    if os.path.exists(os.path.join(logo_dir, 'product_default.png')):
        product_default_url = settings.MEDIA_URL + 'store/logo/product_default.png'

    if os.path.exists(os.path.join(logo_dir, 'favicon.ico')):
        favicon_url = settings.MEDIA_URL + 'store/logo/favicon.ico'

    return {
        'header_logo_url': header_logo_url,
        'navbar_logo_url': navbar_logo_url,
        'product_default_url': product_default_url,
        'favicon_url': favicon_url,
    }
