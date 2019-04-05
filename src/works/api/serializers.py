from rest_framework import serializers

from works.models import Work, WorkImage, Review


class WorkImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkImage
        fields = [
            'image',
        ]


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'work',
            'first_score',
            'second_score',
            'third_score',
        ]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id',
            'created',
            'modified',
            'first_score',
            'second_score',
            'third_score',
        ]


class WorkListSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer()

    class Meta:
        model = Work
        fields = [
            'id',
            'created',
            'modified',
            'username',
            'email',
            'status',
            'reviews',
        ]


class WorkDetailSerializer(serializers.ModelSerializer):
    images = WorkImageSerializer(many=True)
    reviews = ReviewSerializer()

    class Meta:
        model = Work
        fields = [
            'id',
            'created',
            'modified',
            'username',
            'email',
            'status',
            'images',
            'reviews',
        ]


class WorkCreateSerializer(serializers.ModelSerializer):
    """
    Serialize when creating work
    """
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    images = WorkImageSerializer(many=True, read_only=True)

    class Meta:
        model = Work
        fields = [
            'username',
            'email',
            'images',
        ]

    def create(self, validated_data):
        image_data = self.context['request'].FILES
        if not len(image_data):
            raise serializers.ValidationError({'image': ['New work should contain at least one image file in post body']})
        work = Work.objects.create(**validated_data)
        for image in image_data.values():
            WorkImage.objects.create(work=work, image=image)
        return work
