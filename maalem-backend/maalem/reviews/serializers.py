from rest_framework import serializers
from .models import Review, ReviewPhoto
from django.contrib.auth import get_user_model

User = get_user_model()

class ReviewPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewPhoto
        fields = ['id', 'image', 'uploaded_at']
        read_only_fields = ['uploaded_at']


class ReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.SerializerMethodField()
    reviewer_image = serializers.SerializerMethodField()
    photos = ReviewPhotoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'artisan', 'reviewer', 'reviewer_name', 'reviewer_image',
            'rating', 'comment', 'work_quality', 'punctuality', 
            'professionalism', 'created_at', 'updated_at', 'photos'
        ]
        read_only_fields = ['reviewer', 'created_at', 'updated_at']
    
    def get_reviewer_name(self, obj):
        if obj.reviewer.first_name and obj.reviewer.last_name:
            return f"{obj.reviewer.first_name} {obj.reviewer.last_name}"
        return obj.reviewer.username
    
    def get_reviewer_image(self, obj):
        if obj.reviewer.profile_picture:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.reviewer.profile_picture.url)
        return None
    
    def validate(self, attrs):
        request = self.context.get('request')
        if request and request.user:
            # Ensure reviewer is a client
            if request.user.user_type != 'client':
                raise serializers.ValidationError({
                    "error": "Seuls les clients peuvent laisser des avis."
                })
            
            # Ensure artisan is actually an artisan
            artisan = attrs.get('artisan')
            if artisan and artisan.user_type != 'artisan':
                raise serializers.ValidationError({
                    "error": "Vous ne pouvez laisser un avis que pour un artisan."
                })
            
            # Check if user has already reviewed this artisan
            if Review.objects.filter(
                artisan=artisan, 
                reviewer=request.user
            ).exists():
                raise serializers.ValidationError({
                    "error": "Vous avez déjà laissé un avis pour cet artisan."
                })
        
        return attrs
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user:
            validated_data['reviewer'] = request.user
        return super().create(validated_data)
