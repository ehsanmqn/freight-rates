from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from ratestask_price.views import ListDailyAveragePriceV1


#
# Version 1 APIs
api_patterns_v1 = [
    path("rates/", ListDailyAveragePriceV1.as_view(), name="list-daily-average-price-v1")
]

#
# Version 1 APIs
api_patterns_v2 = [
    path("rates/", ListDailyAveragePriceV1.as_view(), name="list-daily-average-price-v2")
]

api_patterns = [
    path("v1/", include(api_patterns_v1), name="api-v1"),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    # API root path
    path("api/", include(api_patterns), name="api"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
