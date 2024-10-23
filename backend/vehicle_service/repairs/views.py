from datetime import datetime
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from .models import Component, Vehicle, Issue, Payment
from .serializers import ComponentSerializer, PaymentSerializer, VehicleSerializer, IssueSerializer

class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

@api_view(['GET'])
def revenue_view(request):
    today = timezone.now().date()

    daily_revenue = Payment.objects.filter(paid_at__date=today).aggregate(total_revenue=Sum('amount'))['total_revenue']
    daily_revenue = daily_revenue if daily_revenue is not None else 0

    # daily_revenue = Payment.objects.filter(paid_at__date=today).aggregate(total_revenue=Sum('amount'))['total_revenue'] or 0

    first_day_of_month = today.replace(day=1)
    monthly_revenue = Payment.objects.filter(paid_at__date__gte=first_day_of_month).aggregate(total_revenue=Sum('amount'))['total_revenue'] or 0

    first_day_of_year = today.replace(month=1, day=1)
    yearly_revenue = Payment.objects.filter(paid_at__date__gte=first_day_of_year).aggregate(total_revenue=Sum('amount'))['total_revenue'] or 0

    revenue_data = {
        "daily": daily_revenue,
        "monthly": monthly_revenue,
        "yearly": yearly_revenue,
    }

    return Response(revenue_data)


from django.shortcuts import get_object_or_404

@api_view(['POST'])
def complete_issue(request, component_id):
    # Retrieve the component and ensure it exists
    component = get_object_or_404(Component, id=component_id)

    # Create the issue. You need to get the vehicle from the request.
    vehicle_id = request.data.get('vehicle_id')  # Assuming you pass the vehicle ID in the request
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    # Specify the repair type. Here, it's assumed to be 'repair', but you can change it as needed.
    repair_type = 'repair'  # or 'purchase' based on your logic

    # Create the Issue instance
    issue = Issue.objects.create(
        vehicle=vehicle,
        component=component,
        repair_type=repair_type
    )

    # Calculate the payment amount (optional based on your logic)
    total_price = issue.price

    # Create the payment
    payment = Payment.objects.create(
        issue=issue,
        amount=total_price
    )

    return Response({'message': 'Issue completed and payment recorded.'}, status=200)

from rest_framework import status

@api_view(['POST'])
def PaymentView(request):
    serializer = PaymentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)