from rest_framework.generics import ListAPIView, RetrieveAPIView
from classifieds_mobile import serializers
from classifieds import models
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view
from classifieds.utils import create_classified_abstraction, deleting_classified_abstraction, \
    editing_classified_abstraction
from rest_framework import permissions


# Create your views here.

# Classifieds List REST API
class ClassifiedsListAPI(ListAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = serializers.ClassifiedsListAPISerializers
    queryset = models.Classified.objects.all()


# Classifieds Detail REST API
class ClassifiedsDetailAPI(RetrieveAPIView):
    permission_classes = []
    authentication_classes = []
    lookup_field = 'pk'
    serializer_class = serializers.ClassifiedsListAPISerializers

    def get_queryset(self):
        return models.Classified.objects.filter(pk=self.kwargs['pk'])


# signup api (dummy)
@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def signup_api(request):
    data = json.loads(request.body)
    new_user_instance = models.User.objects.create(email=data['email'])
    new_user_instance.set_password(data['password'])
    new_user_instance.save()
    return JsonResponse({'Response': 'User created Successfully'}, status=201, content_type='application/json')


# adding new classified function
@api_view(['POST'])
@csrf_exempt
def post_ad_api(request):
    data = json.loads(request.body)
    classified_instance = create_classified_abstraction(request, **data)
    return JsonResponse({'status': '201. Classified Created Successfully'})


# editing existing classified
@api_view(['POST'])
@csrf_exempt
def edit_ad_api(request, **kwargs):
    data = json.loads(request.body)
    classified_instance = models.Classified.objects.get(pk=kwargs.get('pk'))
    editing_classified_abstraction(request, classified_instance,**data)
    return JsonResponse({'data:Edited Successfully'}, status=200, content_type='application/json')


# deleting classifieds
@api_view(['DELETE'])
def delete_ad_api(request, **kwargs):
    deleting_classified_abstraction(request, **kwargs)
    return JsonResponse({'data': 'Classified deleted successfully'}, status=204, content_type='application/json')


# my classifieds function
@api_view(['GET'])
def users_classifieds_api(request):
    qs = models.Classified.objects.filter(user=request.user)
    serialized_qs = serializers.ClassifiedsListAPISerializers(qs, many=True).data
    return JsonResponse({'data': serialized_qs})


# contact-us api
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def contact_us_api(request):
    data = json.loads(request.body)
    # msg_plain = render_to_string('emails/contact_form.txt')
    #
    # email = EmailMessage('Contact Form: %s' % form.cleaned_data.get("subject"), msg_plain,
    #                      to=proj_settings.CONTACT_EMAILS)  # CONTACT EMAILS IS A LIST
    # email.send()
    #
    # messages.success(request, 'Your message has been sent successfully. We will get in touch shortly!')
    return JsonResponse({'status': 'Form submitted successfully!'})
