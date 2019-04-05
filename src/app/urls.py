from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from a12n.views import WhoAmIView
from works.api.views import WorkViewSet, ReviewViewSet, ReviewOnModerationViewSet

router = routers.SimpleRouter()

router.register(r'works', WorkViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'admin/onreview', ReviewOnModerationViewSet)

api_v1 = (
    url(r'^', include(router.urls)),
    url(r'^whoami/', WhoAmIView.as_view()),
    url(r'^auth/token/$', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    url(r'^auth/token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
)

urlpatterns = [
    url(r'^api/v1/', include((api_v1, 'api'), namespace='v1')),
    url(r'^djangoadmin/', admin.site.urls),
]

if settings.DEBUG:  # serve debug toolbar assets and pages
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls, namespace='debug')),
    ]

if settings.DEBUG:  # serve media files through django
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
