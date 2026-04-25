from django.urls import path, include

urlpatterns = [
    path('v1/', include('api.v1.urls')),
    # В будущем: path('v2/', include('api.v2.urls')),
]