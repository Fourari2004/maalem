from django_filters import rest_framework as filters
from .models import Post
from django.contrib.auth import get_user_model

User = get_user_model()

class PostFilter(filters.FilterSet):
    category = filters.CharFilter(lookup_expr='iexact')
    location = filters.CharFilter(lookup_expr='icontains')
    author_type = filters.CharFilter(field_name='author__user_type')
    search = filters.CharFilter(method='search_filter')
    near_me = filters.BooleanFilter(method='near_me_filter')
    date_range = filters.DateFromToRangeFilter(field_name='created_at')

    class Meta:
        model = Post
        fields = ['category', 'location', 'author_type']

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            models.Q(title__icontains=value) |
            models.Q(description__icontains=value) |
            models.Q(author__username__icontains=value)
        )

    def near_me_filter(self, queryset, name, value):
        user = self.request.user
        if not value or not user.latitude or not user.longitude:
            return queryset

        # Calcul de la distance (approximatif, dans un rayon de 10km)
        from django.db.models import F
        from django.db.models.functions import Power
        
        distance = Power(F('latitude') - user.latitude, 2) + \
                  Power(F('longitude') - user.longitude, 2)
        
        return queryset.annotate(
            distance=distance
        ).filter(distance__lte=0.01)  # ~10km in coordinates