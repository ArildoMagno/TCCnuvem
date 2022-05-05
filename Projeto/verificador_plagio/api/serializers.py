from rest_framework import serializers


class YourSerializer(serializers.Serializer):
    """Your data serializer, define your fields here."""
    comments = serializers.IntegerField()
    likes = serializers.IntegerField()


class AnalyseSerializer(serializers.Serializer):
    name_file1 = serializers.CharField()
    name_file2 = serializers.CharField()
    similar_sets_log1 = serializers.ListField()
    similar_sets_log2 = serializers.ListField()
    percent_plagiarism = serializers.FloatField()
