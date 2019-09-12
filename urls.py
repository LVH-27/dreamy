from django.urls import include, path


urlpatterns = [
    path('', include('dreamy.urls')),
    path('api/', include('api.urls')),
]
