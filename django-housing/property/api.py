from django.http import JsonResponse

import logging
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated


from .forms import PropertyForm
from .models import Property, PropertyImage
from .serializers import PropertiesListSerializer


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_list(request):
    properties = Property.objects.all().order_by('-created_at')
    serializer = PropertiesListSerializer(properties, many=True)

    return JsonResponse({
        'data': serializer.data
    })

    
@api_view(['POST', 'FILES'])
def create_property(request):
    print("Request Headers:", request.headers)
    print("Authorization Header:", request.headers.get('Authorization'))
    print("Authenticated User:", request.user)
    print("Request POST Data:", request.POST)
    print("Request FILES Data:", request.FILES)

    user = request.user
    if not user.is_authenticated:
        return JsonResponse({"error": "User is not authenticated"}, status=403)

    # Recuperation du formulaire et des fichiers
    form = PropertyForm(request.POST, request.FILES)

    if form.is_valid():
        property = form.save(commit=False)
        property.landlord = request.user
        property.save()

        # Récupérer les fichiers additionnels envoyés avec indexation
        additionnal_images = request.FILES.getlist(f'additionnal_images[]')
        print(f'Additionnal images: {additionnal_images}')
        
        # Vérification et ajout des images
        for image in additionnal_images:
            print("Image reçue:", image)
            PropertyImage.objects.create(property=property, image=image)

        return JsonResponse({'success': True, 'property_id': str(property.id)})
    else:
        print('Form Errors:', form.errors)
        print('Non Field Errors:', form.non_field_errors())
        return JsonResponse({'errors': form.errors.as_json()}, status=400)
