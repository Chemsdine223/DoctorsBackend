from rest_framework import generics, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth import get_user_model


from users.serializers import ConsultationSerializer, CreationConsultationSerializer, DoctorSerializer, PatientRegisterSerializer, ScheduleSerializer


from .models import Consultations, CustomUser, Doctor, Patient, Schedule


def create():
    pass

class LoginView(APIView):
    def post(self, request):
        phone = request.data['phone']
        password = request.data['password']

        try:
            user = CustomUser.objects.get(phone=phone)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('User not found')

        if user.role == 'Patient':
            try:
                patient = Patient.objects.get(phone=phone)
            except Patient.DoesNotExist:
                raise AuthenticationFailed('Patient not found')

            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'id': patient.id,
                    'role': user.role,
                    'nom': patient.nom,
                    'prenom': patient.prenom,
                    # 'nni': patient.nni,
                    'phone': patient.phone,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                })
            else:
                raise AuthenticationFailed('Incorrect password')

        elif user.role == 'Doctor':
            try:
                doctor = Doctor.objects.get(phone=phone)
            except Doctor.DoesNotExist:
                raise AuthenticationFailed('Doctor not found')

            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'id': doctor.id,
                    'role': user.role,
                    'nom': doctor.nom,
                    'prenom': doctor.prenom,
                    # 'nni': doctor.nni,
                    'specialite': doctor.specialite.nom,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                })
            else:
                raise AuthenticationFailed('Incorrect password')

        else:
            raise AuthenticationFailed('Invalid role')


class ConsultationListView(generics.ListAPIView):
    serializer_class = ConsultationSerializer
    def get_queryset(self):
        doctor_id = self.kwargs['id']
        queryset = Consultations.objects.filter(doctor_id=doctor_id)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No consultations found."}, status=status.HTTP_404_NOT_FOUND)


class ConsultationPatient(generics.ListAPIView):
    serializer_class = ConsultationSerializer

    def get_queryset(self):
        patient_id = self.kwargs['id']
        queryset = Consultations.objects.filter(patient_id=patient_id)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No consultations found."}, status=status.HTTP_404_NOT_FOUND)


# class ScheduleView(APIView):
#     def post(self, request):
#         serializer = ScheduleSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ScheduleView(APIView):
    def post(self, request):
        doctor_id = request.data.get('doctor')
        existing_schedule = Schedule.objects.filter(
            doctor_id=doctor_id).first()

        if existing_schedule:
            serializer = ScheduleSerializer(
                existing_schedule, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response("Schedule not found", status=status.HTTP_404_NOT_FOUND)


class GetSchedules(APIView):                                      
    def get(self, request, doctor_id):
        existing_schedule = Schedule.objects.filter(
            doctor_id=doctor_id).first()

        if existing_schedule:
            serializer = ScheduleSerializer(existing_schedule)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response("Schedule not found", status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_patient_data(request, id):
    patient = Patient.objects.get(id=id)
    # Retrieve additional patient data or perform any required operations
    # ...

    return Response({
                    # 'patient_data': 'Data related to the patient',
                    'id': patient.id,
                    # "role": "Patient",
                    'nom': patient.nom,
                    'prenom': patient.prenom,
                    # 'nni': patient.nni,
                    'phone': patient.phone,
                    })


class PatientRegisterView(generics.CreateAPIView):

    model = get_user_model()
    serializer_class = PatientRegisterSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(status=Response.status_code)


class DoctorsListView(APIView):
    def get(self, request):
        users = Doctor.objects.all()
        serializer = DoctorSerializer(users, many=True)
        return Response(serializer.data)


class CreateConsultationView(APIView):
    def post(self, request, format=None):
        serializer = CreationConsultationSerializer(data=request.data)
        if serializer.is_valid():
            patient_id = serializer.validated_data.get('patient_id')
            doctor_id = serializer.validated_data.get('doctor_id')

            # Check if there is an existing consultation with the same doctor and patient
            existing_consultation = Consultations.objects.filter(
                patient_id=patient_id,
                doctor_id=doctor_id
            ).exists()

            if existing_consultation:
                return Response({'error': 'A consultation with this doctor already exists for the patient.'}, status=400)

            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)

