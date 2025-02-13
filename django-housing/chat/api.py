from django.http import JsonResponse

from rest_framework.decorators import api_view

from .models import Conversation, ConversationMessage
from .serializers import ConversationListSerializer, ConversationDetailSerializer, ConversationMessageSerializer


@api_view(['GET'])
def conversation_list(request):
    serializer = ConversationListSerializer(request.user.conversations.all(), many=True)

    return JsonResponse({
        'data': serializer.data
    }, safe=False)


@api_view(['GET'])
def conversation_detail(request, pk):
    conversation = request.user.conversations.get(pk=pk)

    limit = int(request.GET.get('limit', 10))
    messages = conversation.messages.order_by('-created_at')[:limit]

    conversation_serializer = ConversationDetailSerializer(conversation, many=False)

    # Inversion de l'ordre des messages pour passer du plus ancien au plus récent
    messages = messages[::-1]  # Inverse l'ordre de la liste

    messages_serializer = ConversationMessageSerializer(messages, many=True)
    # messages_serializer = ConversationMessageSerializer(conversation.messages.all(), many=True)

    return JsonResponse({
        'conversation': conversation_serializer.data, 
        'messages': messages_serializer.data
    }, safe=False)
