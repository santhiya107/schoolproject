from dataclasses import fields
from rest_framework import serializers
from .models import Grade,Subject,Chapter,Answers,Question
import re


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'


    def validate(self, data):
        if Grade.objects.filter(grade=data['grade']).exists():
            raise serializers.ValidationError({'error':'invalid grade'})
        return data

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

    def validate(self,data):
        name = data['name']
        name = re.findall(r"[^\W\d_]+|\d+",name)
        data['name'] = (' '.join(name)).capitalize()
        code = (data['code']).upper()
        queryset = Subject.objects.all()
        if self.instance:
            id = self.instance.id
            queryset = queryset.exclude(id=id)
        if queryset.filter(name = data['name'],grade=data['grade']).exists():
            raise serializers.ValidationError({'error':'invalid subject name'})
        if queryset.filter(code=code).exists():
            raise serializers.ValidationError({'error':'invalid subject code'})

        return data

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'

    def validate(self, data):
        name = data['name']
        name = re.findall(r"[^\W\d_]+|\d+",name)
        data['name'] = (' '.join(name)).lower()
        queryset = Chapter.objects.all()
        if self.instance:
            id = self.instance.id
            queryset = queryset.exclude(id=id)

        if queryset.filter(name = data['name'],subject=data['subject']).exists():
            raise serializers.ValidationError({'error':'invalid chapter name'})
        if queryset.filter(subject=data['subject'],chapter_no=data['chapter_no']).exists():
            raise serializers.ValidationError({'error':'invalid cahpter no'})

        return data

        # if self.instance:
        #     id = self.instance.id
        #     if Chapter.objects.filter(subject=data['subject'],chapter_no=data['chapter_no']).exclude(id=id).exists():
        #         raise serializers.ValidationError({'error':'invalid chapter no'})
        #     if Chapter.objects.filter(name=name,subject=data['subject']).exclude(id=id).exists():
        #         raise serializers.ValidationError({'error':'invalid chapter name'})

        # else:
        #     if Chapter.objects.filter(subject=data['subject'],chapter_no=data['chapter_no']).exists():
        #         raise serializers.ValidationError({'error':'invalid chapter no'})
        #     if Chapter.objects.filter(name=name,subject=data['subject']).exists():
        #         raise serializers.ValidationError({'error':'invalid chapter name'})
        # return data    

class ChapterViewSerializer(serializers.Serializer):
    grade = serializers.IntegerField()
    subject = serializers.CharField()



class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ['option_a','option_b','option_c','option_d','answer']

class QuestionAnswerSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer()

    class Meta:
        model = Question
        fields = ['id','grade','subject','chapter','question',
                    'question_type','cognitive_level','difficulty_level','answers']


    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        question = Question.objects.create(**validated_data)
        Answers.objects.create(question=question, **answers_data)
        return question

    def update(self, instance, validated_data):
        answers_data = validated_data.pop('answers')
        answers = instance.answers
        instance.grade = validated_data.get('grade', instance.grade)
        instance.subject = validated_data.get('subject', instance.subject)
        instance.chapter = validated_data.get('chapter', instance.chapter)
        instance.question = validated_data.get('question', instance.question)
        instance.question_type = validated_data.get('question_type', instance.question_type)
        instance.cognitive_level = validated_data.get('cognitive_level', instance.cognitive_level)
        instance.difficulty_level = validated_data.get('difficulty_level', instance.difficulty_level)
        instance.save()

        answers.answer = answers_data.get(
            'answer',
            answers.answer
        )
        answers.option_a = answers_data.get(
            'option_a',
            answers.option_a
        )
        answers.option_b = answers_data.get(
            'option_b',
            answers.option_b
        )

        answers.option_c = answers_data.get(
            'option_c',
            answers.option_c
        )
        answers.option_d = answers_data.get(
            'option_d',
            answers.option_d
        )
        answers.save()
        return instance

class QuestionGetSerializer(serializers.Serializer):
    grade = serializers.IntegerField()
    subject = serializers.CharField()
    number_of_questions = serializers.IntegerField()

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


