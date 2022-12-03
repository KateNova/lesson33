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
        'api/core/',
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
