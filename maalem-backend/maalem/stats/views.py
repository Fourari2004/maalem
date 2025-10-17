from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg, Count, Sum
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
from django.utils import timezone

class StatsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def artisan_stats(self, request):
        if request.user.user_type != 'artisan':
            return Response({"error": "Only artisans can access these stats"}, 
                          status=status.HTTP_403_FORBIDDEN)

        # Période
        period = request.query_params.get('period', '30')  # jours par défaut
        start_date = timezone.now() - timedelta(days=int(period))

        # Statistiques des projets
        projects_stats = Project.objects.filter(
            artisan=request.user,
            created_at__gte=start_date
        ).aggregate(
            total_projects=Count('id'),
            completed_projects=Count('id', filter=models.Q(status='completed')),
            in_progress_projects=Count('id', filter=models.Q(status='in_progress')),
            average_project_value=Avg('quotes__amount', filter=models.Q(quotes__status='accepted'))
        )

        # Statistiques des rendez-vous
        appointments_stats = Appointment.objects.filter(
            artisan=request.user,
            created_at__gte=start_date
        ).aggregate(
            total_appointments=Count('id'),
            completed_appointments=Count('id', filter=models.Q(status='completed')),
            cancelled_appointments=Count('id', filter=models.Q(status='cancelled'))
        )

        # Statistiques des avis
        reviews_stats = Review.objects.filter(
            artisan=request.user,
            created_at__gte=start_date
        ).aggregate(
            total_reviews=Count('id'),
            average_rating=Avg('rating'),
            average_work_quality=Avg('work_quality'),
            average_punctuality=Avg('punctuality'),
            average_professionalism=Avg('professionalism')
        )

        # Chiffre d'affaires mensuel
        revenue_by_month = Payment.objects.filter(
            invoice__project__artisan=request.user,
            status='completed',
            payment_date__gte=start_date
        ).annotate(
            month=TruncMonth('payment_date')
        ).values('month').annotate(
            total=Sum('amount')
        ).order_by('month')

        return Response({
            'projects': projects_stats,
            'appointments': appointments_stats,
            'reviews': reviews_stats,
            'revenue_by_month': revenue_by_month
        })

    @action(detail=False, methods=['get'])
    def client_stats(self, request):
        if request.user.user_type == 'artisan':
            return Response({"error": "This endpoint is for clients only"}, 
                          status=status.HTTP_403_FORBIDDEN)

        # Période
        period = request.query_params.get('period', '30')  # jours par défaut
        start_date = timezone.now() - timedelta(days=int(period))

        # Statistiques des projets
        projects_stats = Project.objects.filter(
            client=request.user,
            created_at__gte=start_date
        ).aggregate(
            total_projects=Count('id'),
            completed_projects=Count('id', filter=models.Q(status='completed')),
            in_progress_projects=Count('id', filter=models.Q(status='in_progress')),
            total_spent=Sum('quotes__amount', filter=models.Q(quotes__status='accepted'))
        )

        # Statistiques des rendez-vous
        appointments_stats = Appointment.objects.filter(
            client=request.user,
            created_at__gte=start_date
        ).aggregate(
            total_appointments=Count('id'),
            completed_appointments=Count('id', filter=models.Q(status='completed')),
            cancelled_appointments=Count('id', filter=models.Q(status='cancelled'))
        )

        # Artisans favoris
        favorite_artisans = Project.objects.filter(
            client=request.user,
            created_at__gte=start_date
        ).values(
            'artisan__id',
            'artisan__username'
        ).annotate(
            projects_count=Count('id')
        ).order_by('-projects_count')[:5]

        return Response({
            'projects': projects_stats,
            'appointments': appointments_stats,
            'favorite_artisans': favorite_artisans
        })