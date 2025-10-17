from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model
from django.db.models import Avg

User = get_user_model()

class ArtisanFilter(filters.FilterSet):
    specialty = filters.CharFilter(lookup_expr='icontains')
    location = filters.CharFilter(field_name='address', lookup_expr='icontains')
    min_rating = filters.NumberFilter(field_name='rating', lookup_expr='gte')
    max_rating = filters.NumberFilter(field_name='rating', lookup_expr='lte')
    min_experience = filters.NumberFilter(field_name='experience_years', lookup_expr='gte')
    search = filters.CharFilter(method='search_filter')
    near_me = filters.BooleanFilter(method='near_me_filter')

    class Meta:
        model = User
        fields = ['specialty', 'location', 'min_rating', 'max_rating', 'min_experience']

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            models.Q(username__icontains=value) |
            models.Q(specialty__icontains=value) |
            models.Q(bio__icontains=value)
        ).filter(user_type='artisan')

    def near_me_filter(self, queryset, name, value):
        user = self.request.user
        if not value or not user.latitude or not user.longitude:
            return queryset

        from django.db.models import F
        from django.db.models.functions import Power
        
        distance = Power(F('latitude') - user.latitude, 2) + \
                  Power(F('longitude') - user.longitude, 2)
        
        return queryset.filter(user_type='artisan').annotate(
            distance=distance
        ).filter(distance__lte=0.01)  # ~10km in coordinates