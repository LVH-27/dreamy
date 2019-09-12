from django.urls import include, path


urlpatterns = [
    path('', include('dreamy.urls')),
    path('api/', include('api.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
]
