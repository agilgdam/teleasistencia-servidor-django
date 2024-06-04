from django.contrib.auth.models import User, Group
from rest_framework import viewsets

from ... import models
from . import serializers


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class DireccionViewSet(viewsets.ModelViewSet):
    queryset = models.Direccion.objects.all()
    serializer_class = serializers.DireccionSerializer


class PersonaViewSet(viewsets.ModelViewSet):
    queryset = models.Persona.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve",):
            return serializers.PersonaReadSerializer
        else:
            return serializers.PersonaSerializer


class ClasificacionRecursoComunitarioViewSet(viewsets.ModelViewSet):
    queryset = models.Clasificacion_Recurso_Comunitario.objects.all()
    serializer_class = serializers.ClasificacionRecursoComunitarioSerializer


class TipoRecursoComunitarioViewSet(viewsets.ModelViewSet):
    queryset = models.Tipo_Recurso_Comunitario.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve",):
            return serializers.TipoRecursoComunitarioReadSerializer
        else:
            return serializers.TipoRecursoComunitarioSerializer


class RecursoComunitarioViewSet(viewsets.ModelViewSet):
    queryset = models.Recurso_Comunitario.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve",):
            return serializers.RecursoComunitarioReadSerializer
        else:
            return serializers.RecursoComunitarioSerializer


class TipoViviendaViewSet(viewsets.ModelViewSet):
    queryset = models.Tipo_Vivienda.objects.all()
    serializer_class = serializers.TipoViviendaSerializer


class TipoSituacionViewSet(viewsets.ModelViewSet):
    queryset = models.Tipo_Situacion.objects.all()
    serializer_class = serializers.TipoSituacionSerializer


class TerminalViewSet(viewsets.ModelViewSet):
    queryset = models.Terminal.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve",):
            return serializers.TerminalReadSerializer
        else:
            return serializers.TerminalSerializer


class TipoModalidadPacienteViewSet(viewsets.ModelViewSet):
    queryset = models.Tipo_Modalidad_Paciente.objects.all()
    serializer_class = serializers.TipoModalidadPacienteSerializer


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = models.Paciente.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve",):
            return serializers.PacienteReadSerializer
        else:
            return serializers.PacienteSerializer


class RelacionPacientePersonaViewSet(viewsets.ModelViewSet):
    queryset = models.Relacion_Paciente_Persona.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve",):
            return serializers.RelacionPacientePersonaReadSerializer
        else:
            return serializers.RelacionPacientePersonaSerializer


class ClasificacionAlarmaViewSet(viewsets.ModelViewSet):
    queryset = models.Clasificacion_Alarma.objects.all()
    serializer_class = serializers.ClasificacionAlarmaSerializer


class TipoAlarmaViewSet(viewsets.ModelViewSet):
    queryset = models.Tipo_Alarma.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve",):
            return serializers.TipoAlarmaReadSerializer
        else:
            return serializers.TipoAlarmaSerializer


class AlarmaViewSet(viewsets.ModelViewSet):
    queryset = models.Alarma.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve",):
            return serializers.AlarmaReadSerializer
        else:
            return serializers.AlarmaSerializer
