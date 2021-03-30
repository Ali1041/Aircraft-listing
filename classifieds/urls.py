from django.urls import path
from classifieds import views as classifieds_views

urlpatterns = [

    # Home page url
    path('', classifieds_views.index, name='index'),

    # Contact us page url
    path('contacts/', classifieds_views.contacts, name='contacts'),

    # Classifieds page url
    path('classifieds/', classifieds_views.ClassifiedListView.as_view(), name='classifieds'),

    # Classified page url
    path('classifieds/<int:pk>/', classifieds_views.ClassifiedDetailView.as_view(), name='classified'),
    path('classifieds/<int:pk>/pay/', classifieds_views.classified_pay, name='classified_pay'),
    path('classifieds/<int:pk>/confirm-payment/', classifieds_views.classified_confirm_payment,
         name='classified_confirm_payment'),
    path('classifieds/<int:pk>/activate/', classifieds_views.classified_activate,
         name='classified_activate'),
    path('classifieds/<int:pk>/deactivate/', classifieds_views.classified_deactivate,
         name='classified_deactivate'),

    # users classifieds url
    path('my-classifieds/', classifieds_views.my_classifieds, name='my_classifieds'),
    path('delete-ad/<int:pk>/', classifieds_views.delete_classified, name='delete-ad'),
    path('post-ad-edit/<int:pk>/', classifieds_views.post_ad, name='post_ad_edit'),

    # Ad posting url
    path('post-ad/', classifieds_views.post_ad, name='post_ad'),


    # others
    path('search/', classifieds_views.search, name='search'),
    path('newsletter-subscribe/', classifieds_views.newsletter, name='newsletter'),
]