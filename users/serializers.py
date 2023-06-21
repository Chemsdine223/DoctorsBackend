from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models import Consultations, CustomUser, Patient, Schedule,Doctor, Specialite
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=17)
    password = serializers.CharField()

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')

        if phone and password:
            user = authenticate(phone=phone, password=password)
            if user:
                attrs['user'] = user
                return attrs
            raise serializers.ValidationError('Invalid login credentials.')
        raise serializers.ValidationError('Phone and password are required.')




class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['nom', 'prenom']

class SpecialiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialite
        fields = ['id','nom']

class DoctorSerializer(serializers.ModelSerializer):
    specialite = SpecialiteSerializer()
    class Meta:
        model = Doctor
        fields = ['id','nom', 'prenom','specialite']

class ConsultationSerializer(serializers.ModelSerializer):
    
    doctor_id = DoctorSerializer()
    patient_id = PatientSerializer()
    specialite = SpecialiteSerializer()
    
    class Meta:
        model = Consultations
        fields = '__all__'
        

class ConsultationPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultations
        fields = '__all__'


class CreationConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultations
        fields = '__all__'
        
        




# from rest_framework import serializers
# from .models import Schedule, Doctor

# class DoctorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Doctor
#         fields = ['nom', 'specialite','id']
        
class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('doctor', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche')


# class ConsultationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Consultations
#         fields = '__all__'

class PatientRegisterSerializer(serializers.ModelSerializer):
    
    nom = serializers.CharField(
        required = True
    )
    
    
    prenom = serializers.CharField(
        required = True
    )
        
    # nni = serializers.CharField(
    #     required = True,
    #     validators= [
    #         UniqueValidator(
    #             queryset= CustomUser.objects.all(),
                
    #         )
    #     ]
    # )
    phone = serializers.IntegerField(
        required = True,
        validators= [
            UniqueValidator(
                queryset= CustomUser.objects.all(),
                
            )
        ]
    )
    
    password = serializers.CharField(
        write_only = True,
        required = True,
        validators = [
            validate_password,
        ],
        style ={
            "input_type":"password",
        },
    )
    
    password2 = serializers.CharField(
        write_only = True,
        required = True,
        validators = [
            validate_password,
        ],
        style ={
            "input_type":"password",
        },
    )
    
    class Meta:
        model = Patient
        fields = (
            "nom",
            "prenom",
            "phone",
            # "nni",
            "password",
            "password2",
            
        )
    
    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {
                    "password":"passwords must match. "
                }
            )
        return attrs
    
    def create(self, validated_data):
        user = Patient.objects.create_user(
            phone= validated_data["phone"],
            # nni= validated_data["nni"],
            nom= validated_data["nom"],
            prenom= validated_data["prenom"],
        )
        user.set_password(
            validated_data["password"]
        )
        user.save()
        return user
