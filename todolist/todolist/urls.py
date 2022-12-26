from django.contrib import admin
from django.urls import (
    path,
    include
)

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView
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
        'goals/',
        include(
            ('goals.urls', 'goals'),
            namespace='goals'
        )
    ),
    path(
        'bot/',
        include(
            ('bot.urls', 'bot'),
            namespace='bot'
        ),
    ),
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        'schema/',
        SpectacularAPIView.as_view(),
        name='schema'
    ),
    path(
        'schema/swagger-ui/',
        SpectacularSwaggerView.as_view(
            url_name='schema'
        ),
        name='swagger-ui'
    ),
]
