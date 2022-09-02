from rest_framework import serializers


class ItemSerializer(serializers.Serializer):
    seller_id= serializers.IntegerField()
    title= serializers.CharField()
    base_price= serializers.IntegerField() 
    original_price= serializers.IntegerField()
    initial_quantity= serializers.IntegerField() 
    sold_quantity= serializers.IntegerField()
    available_quantity= serializers.IntegerField() 
    thumbnail= serializers.URLField() 
    