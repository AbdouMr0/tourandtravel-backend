from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .models import Contact
from .serializers import ContactSerializer

@api_view(['POST'])
def contact_create(request):
    if request.method == 'POST':
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            # Save the contact data
            contact = serializer.save()

            # Send email
            send_mail(
                subject=f"New Contact Form Submission: {contact.subject}",
                message=f"Message from {contact.name} ({contact.email}):\n\n{contact.message}",
                from_email='your_email@example.com',  # Your email address
                recipient_list=['recipient@example.com'],  # Recipient's email address
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
