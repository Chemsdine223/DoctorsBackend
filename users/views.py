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
from datetime import datetime, time
import re


from users.serializers import ConsultationSerializer, CreationConsultationSerializer, DoctorSerializer, PatientRegisterSerializer, ScheduleGetSerializer, ScheduleSerializer


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

    def post(self, request, *args, **kwargs):
        consultation_id = request.data.get('consultation_id')
        try:
            consultation = Consultations.objects.get(id=consultation_id)
        except Consultations.DoesNotExist:
            return Response({"error": "Consultation not found."}, status=status.HTTP_404_NOT_FOUND)

        consultation.status = 'accepted'
        consultation.save()
        serializer = self.get_serializer(consultation)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        consultation_id = request.data.get('consultation_id')
        try:
            consultation = Consultations.objects.get(id=consultation_id)
        except Consultations.DoesNotExist:
            return Response({"error": "Consultation not found."}, status=status.HTTP_404_NOT_FOUND)

        consultation.status = 'refused'
        consultation.save()
        serializer = self.get_serializer(consultation)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
            serializer = ScheduleGetSerializer(existing_schedule)
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



# class CreateConsultationView(APIView):
#     def post(self, request, format=None):
#         serializer = CreationConsultationSerializer(data=request.data)
#         if serializer.is_valid():
#             patient_id = serializer.validated_data.get('patient_id')
#             doctor_id = serializer.validated_data.get('doctor_id')
#             consultation_date_str = serializer.validated_data.get('date_de_consultation')
#             consultation_time_str = serializer.validated_data.get('heure_de_consultation')

#             # Parse date from string
#             consultation_date = datetime.strptime(consultation_date_str, "%Y-%m-%d").date()

#             # Parse time interval from string (e.g., "11h-12h")
#             time_match = re.match(r"(\d{1,2})h-(\d{1,2})h", consultation_time_str)
#             if time_match:
#                 start_hour = int(time_match.group(1))
#                 end_hour = int(time_match.group(2))
#                 consultation_time = time(start_hour)
#             else:
#                 return Response({'error': 'Invalid time format. Expected "hh-hh".'}, status=400)

#             # Combine date and time into a datetime object
#             consultation_datetime = datetime.combine(consultation_date, consultation_time)

#             # Check if there is an existing consultation with the same doctor and patient
#             existing_consultation = Consultations.objects.filter(
#                 patient_id=patient_id,
#                 doctor_id=doctor_id,
#                 date_de_consultation=consultation_date_str,
#                 heure_de_consultation=consultation_time_str
#             ).exists()

#             if existing_consultation:
#                 return Response({'error': 'Une consultation existe aux heures et date spécifiées.'}, status=400)

#             # Get the doctor's schedule for the consultation date
#             doctor_schedule = Schedule.objects.filter(doctor_id=doctor_id).first()

#             if not doctor_schedule:
#                 return Response({'error': 'Le médecin n\'a pas de planning défini.'}, status=400)

#             # Get the weekday of the consultation date (0 for Monday, 1 for Tuesday, etc.)
#             consultation_weekday = consultation_date.weekday()

#             # Get the corresponding weekday attribute in the doctor's schedule
#             weekday_attribute = Schedule._meta.get_field(f"{Schedule.weekday_names[consultation_weekday]}")

#             # Get the time slot for the consultation weekday
#             consultation_time_slot = getattr(doctor_schedule, weekday_attribute)

#             # Parse the start and end times of the time slot
#             slot_start_time_str, slot_end_time_str = consultation_time_slot.split('-')
#             slot_start_time = datetime.strptime(slot_start_time_str.strip(), "%Hh").time()
#             slot_end_time = datetime.strptime(slot_end_time_str.strip(), "%Hh").time()

#             # Compare the consultation time with the time slot
#             if not (slot_start_time <= consultation_time <= slot_end_time):
#                 return Response({'error': 'Le médecin n\'est pas disponible à la date et heure spécifiées.'}, status=400)

#             serializer.save()
#             return Response(serializer.data, status=201)

#         return Response(serializer.errors, status=400)






class CreateConsultationView(APIView):
    def post(self, request, format=None):
        serializer = CreationConsultationSerializer(data=request.data)
        if serializer.is_valid():
            patient_id = serializer.validated_data.get('patient_id')
            doctor_id = serializer.validated_data.get('doctor_id')
            consultation_date_str = serializer.validated_data.get('date_de_consultation')
            consultation_time_str = serializer.validated_data.get('heure_de_consultation')

            # Parse date from string
            consultation_date = datetime.strptime(consultation_date_str, "%Y-%m-%d").date()

            # Parse time interval from string (e.g., "11h-12h")
            time_match = re.match(r"(\d{1,2})h-(\d{1,2})h", consultation_time_str)
            if time_match:
                start_hour = int(time_match.group(1))
                end_hour = int(time_match.group(2))
                consultation_start_time = time(start_hour)
                consultation_end_time = time(end_hour)
            else:
                return Response({'error': 'Invalid time format. Expected "hh-hh".'}, status=400)

            # Check if there is an existing consultation with the same doctor and patient
            existing_consultation = Consultations.objects.filter(
                patient_id=patient_id,
                doctor_id=doctor_id,
                date_de_consultation=consultation_date_str,
                heure_de_consultation=consultation_time_str
            ).exists()

            if existing_consultation:
                return Response({'error': 'Une consultation existe aux heures et date spécifiées.'}, status=400)

            # Check if there is an existing consultation at the specified date and time
            existing_consultation = Consultations.objects.filter(
                date_de_consultation=consultation_date,
                heure_de_consultation=consultation_time_str
            ).exists()

            if existing_consultation:
                return Response({'error': 'Une consultation existe aux date et temps spécifiés.'}, status=400)

            # Check if the doctor is available at the specified date and time
            doctor_schedule = Schedule.objects.get(doctor_id=doctor_id)
            day_of_week = consultation_date.weekday()
            day_of_week_mapping = {
                0: 'lundi',
                1: 'mardi',
                2: 'mercredi',
                3: 'jeudi',
                4: 'vendredi',
                5: 'samedi',
                6: 'dimanche'
            }
            day_of_week_field = day_of_week_mapping.get(day_of_week)
            if day_of_week_field:
                doctor_available_time = getattr(doctor_schedule, day_of_week_field)
                available_start_hour, available_end_hour = doctor_available_time.split(' - ')
                available_start_time = datetime.strptime(available_start_hour, "%Hh").time()
                available_end_time = datetime.strptime(available_end_hour, "%Hh").time()

                if (
                    consultation_start_time < available_start_time or
                    consultation_end_time > available_end_time
                ):
                    return Response({'error': 'Le medecin n\'est pas disponible a la date et heure specifiees.'}, status=400)

            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)



# class CreateConsultationView(APIView):
#     def post(self, request, format=None):
#         serializer = CreationConsultationSerializer(data=request.data)
#         if serializer.is_valid():
#             patient_id = serializer.validated_data.get('patient_id')
#             doctor_id = serializer.validated_data.get('doctor_id')
#             consultation_date_str = serializer.validated_data.get(
#                 'date_de_consultation')
#             consultation_time_str = serializer.validated_data.get(
#                 'heure_de_consultation')

#             # Parse date from string
#             consultation_date = datetime.strptime(
#                 consultation_date_str, "%Y-%m-%d").date()

#             # Parse time interval from string (e.g., "11h-12h")
#             time_match = re.match(
#                 r"(\d{1,2})h-(\d{1,2})h", consultation_time_str)
#             if time_match:
#                 start_hour = int(time_match.group(1))
#                 end_hour = int(time_match.group(2))
#                 consultation_time = time(start_hour)
#             else:
#                 return Response({'error': 'Invalid time format. Expected "hh-hh".'}, status=400)

#             # Combine date and time into a datetime object
#             consultation_datetime = datetime.combine(
#                 consultation_date, consultation_time)

#             # Check if there is an existing consultation with the same doctor and patient
#             existing_consultation = Consultations.objects.filter(
#                 patient_id=patient_id,
#                 doctor_id=doctor_id,
#                 date_de_consultation=consultation_date_str,
#                 heure_de_consultation=consultation_time_str
#             ).exists()

#             if existing_consultation:
#                 return Response({'error': 'Une consultation existe aux heures et date specifies.'}, status=400)

#             # Check if there is an existing consultation at the specified date and time
#             existing_consultation = Consultations.objects.filter(
#                 date_de_consultation=consultation_date,
#                 heure_de_consultation=consultation_time
#             ).exists()

#             if existing_consultation:
#                 return Response({'error': 'Une consultation exists aux date et temps specifies.'}, status=400)

#             serializer.save()
#             return Response(serializer.data, status=201)

#         return Response(serializer.errors, status=400)


# class CreateConsultationView(APIView):
#     def post(self, request, format=None):
#         serializer = CreationConsultationSerializer(data=request.data)
#         if serializer.is_valid():
#             patient_id = serializer.validated_data.get('patient_id')
#             doctor_id = serializer.validated_data.get('doctor_id')

#             # Check if there is an existing consultation with the same doctor and patient
#             existing_consultation = Consultations.objects.filter(
#                 patient_id=patient_id,
#                 doctor_id=doctor_id
#             ).exists()

#             if existing_consultation:
#                 return Response({'error': 'A consultation with this doctor already exists for the patient.'}, status=400)

#             serializer.save()
#             return Response(serializer.data, status=201)

#         return Response(serializer.errors, status=400)


class AddDescription(generics.GenericAPIView):
    # Replace with your actual serializer class
    serializer_class = ConsultationSerializer

    def post(self, request, *args, **kwargs):
        consultation_id = request.data.get('consultation_id')
        consultation_desc = request.data.get('description')

        try:
            consultation = Consultations.objects.get(id=consultation_id)
        except Consultations.DoesNotExist:
            return Response({"error": "Consultation not found."}, status=status.HTTP_404_NOT_FOUND)

        consultation.description = consultation_desc
        consultation.save()

        serializer = self.get_serializer(consultation)
        return Response(serializer.data, status=status.HTTP_200_OK)
