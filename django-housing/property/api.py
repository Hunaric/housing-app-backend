from django.http import JsonResponse

import logging
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .forms import PropertyForm
from .models import Property, PropertyImage, Reservation
from .serializers import PropertiesListSerializer, PropertiesDetailSerializer, ReservationListSerializer
from useraccount.models import User


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_list(request):

    try:
        authorization_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not authorization_header:
            raise ValueError('Authorization header missing')
        
        token = authorization_header.split('Bearer ')[1]
        token = AccessToken(token)
        user_id = token.payload['user_id']
        user = User.objects.get(pk=user_id)
        # print('user:', user)
    except Exception as e:
        user = None
        # print(f'Error: {e}')


    print('user,', user)
    
    favorites = []
    properties = Property.objects.all().order_by('-created_at')

    # Filter for the url
    is_favorite = request.GET.get('is_favorite', '')
    landlord_id = request.GET.get('landlord_id', '')

    if landlord_id:
        properties = properties.filter(landlord_id=landlord_id)

    if is_favorite:
        properties = properties.filter(favorited__in=[user])
    
    # Not filtered
    if user:
        for property in properties:
            if user in property.favorited.all():
                favorites.append(property.id)
    serializer = PropertiesListSerializer(properties, many=True)

    return JsonResponse({
        'data': serializer.data,
        'favorites': favorites
    })


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def properties_detail(request, pk):
    property = Property.objects.get(pk=pk)

    serializer = PropertiesDetailSerializer(property, many=False)

    return JsonResponse(serializer.data)

    

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def property_reservations(request, pk):
    property = Property.objects.get(pk=pk)
    reservations = property.reservations.all()

    serializer = ReservationListSerializer(reservations, many=True)

    return Response(serializer.data)
    
    
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
def book_property(request, pk):
    try: 
        guests = request.POST.get('guests', '')
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        number_of_nights = request.POST.get('number_of_nights', '')
        total_price = request.POST.get('total_price', '')

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
        return JsonResponse({'success': True})
    except Exception as e:
        print('Error', e)

        return JsonResponse({'success': False})


@api_view(['POST'])
def toggle_favorite(request, pk):
    property = Property.objects.get(pk=pk)

    if request.user in property.favorited.all():
        property.favorited.remove(request.user)

        return JsonResponse({'is_favorite': False})
    else:
        property.favorited.add(request.user)

        return JsonResponse({'is_favorite': True})