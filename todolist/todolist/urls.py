from django.contrib import admin
from django.urls import (
    path,
    include
)


urlpatterns = [
    path(
        'oauth/',
        include(
            'social_django.urls',
            namespace='social'
        )
    ),
    path(
        'core/',
        include(
            ('core.urls', 'core'),
            namespace='core'
        )
    ),
    path(
        'admin/',
        admin.site.urls
    ),
]

