from django.http import JsonResponse

import logging
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated


from .forms import PropertyForm
from .models import Property, PropertyImage, Reservation
from .serializers import PropertiesListSerializer, PropertiesDetailSerializer


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_list(request):
    properties = Property.objects.all().order_by('-created_at')
    serializer = PropertiesListSerializer(properties, many=True)

    return JsonResponse({
        'data': serializer.data
    })


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_detail(request, pk):
    property = Property.objects.get(pk=pk)

    serializer = PropertiesDetailSerializer(property, many=False)

    return JsonResponse (serializer.data)

    
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


@api_view(['POST'])
def bok_property(request, pk):
    try: 
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        number_of_nights = request.POST.get('number_of_nights', '')
        total_price = request.POST.get('total_price', '')
        guests = request.POST.get('guests', '')

        property = Property.objects.get(pk=pk)

        Reservation.objects.create(
            property=property,
            start_date=start_date,
            end_date=end_date,
            number_of_nights=number_of_nights,
            total_price=total_price,
            guests=guests,
            created_by=request.user
        )
    except Exception as e:
        print('Error', e)

        return JsonResponse({'success': False})