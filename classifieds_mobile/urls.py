from django.urls import path, include
from rest_framework.routers import Route
from classifieds_mobile import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

app_name = 'classifieds_mobile'

urlpatterns = [

    # classifieds page url
    path('classifieds-list/', views.ClassifiedsListAPI.as_view(), name='classified_list'),
    path('classified-detail/<int:pk>/', views.ClassifiedsDetailAPI.as_view(), name='classified_detail'),

    # registration/login urls
    path('signin/', TokenObtainPairView.as_view(), name='sign_api'),
    path('sign-up/', views.signup_api, name='signup_api'),

    # posting classified ad url
    path('post-ad/', views.post_ad_api, name='post-ad'),

    # user classifieds url
    path('my-classifieds/', views.users_classifieds_api, name='my_classifieds'),
    path('my-classifed-delete/<int:pk>/',views.delete_ad_api,name='delete_my_classified'),
    path('edit-ad/<int:pk>/',views.edit_ad_api,name='edit_my_classified'),

    # others
    path('contact-us/', views.contact_us_api, name='contact_us'),
]
