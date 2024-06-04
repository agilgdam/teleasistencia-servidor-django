from django.contrib.auth.models import User, Group
from rest_framework import serializers

from ...models import (
    Database_User,
    Direccion,
    Persona,
    Clasificacion_Recurso_Comunitario,
    Tipo_Recurso_Comunitario,
    Recurso_Comunitario,
    Tipo_Vivienda,
    Tipo_Situacion,
    Terminal,
    Paciente,
    Relacion_Paciente_Persona,
    Tipo_Modalidad_Paciente,
    Clasificacion_Alarma,
    Tipo_Alarma,
    Alarma
)
from ...rest_django.serializers import ImagenUserSerializer as V1ImagenUserSerializer


class GroupSerializer(serializers.ModelSerializer):
    """Serializador para los grupos de Django."""
    class Meta:
        model = Group
        fields = ("pk", "name", "permissions",)


class UserSerializer(serializers.ModelSerializer):
    """Serializador para los usuarios de Django."""
    groups = GroupSerializer(many=True)
    imagen = V1ImagenUserSerializer(source="imagen_user", read_only=True)
    database_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "url", "database_id", "is_active", "last_login", "username", "first_name", "last_name",
                  "email", "date_joined", "groups", "imagen",)

    def get_database_id(self, obj):
        try:
            db_user = obj.database_user
            return db_user.database.pk
        except Database_User.DoesNotExist:
            return None


class DireccionSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Direccion."""
    direccion_completa = serializers.CharField(source="direccion")

    class Meta:
        model = Direccion
        fields = ("id", "localidad", "provincia", "direccion_completa", "codigo_postal", )


class PersonaSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Persona."""
    direccion = DireccionSerializer(source="id_direccion")

    class Meta:
        model = Persona
        fields = ("id", "nombre", "apellidos", "dni", "fecha_nacimiento", "sexo", "telefono_fijo", "telefono_movil",
                  "direccion", )

    def create(self, validated_data):
        info_direccion = validated_data.get("id_direccion")
        direccion, _ = Direccion.objects.get_or_create(**info_direccion)

        persona = Persona.objects.create(
            nombre=validated_data.get("nombre"),
            apellidos=validated_data.get("apellidos"),
            dni=validated_data.get("dni"),
            fecha_nacimiento=validated_data.get("fecha_nacimiento"),
            sexo=validated_data.get("sexo"),
            telefono_fijo=validated_data.get("telefono_fijo"),
            telefono_movil=validated_data.get("telefono_movil"),
            id_direccion=direccion,
        )
        return persona


class PersonaReadSerializer(serializers.ModelSerializer):
    """Serializador de solo lectura para el modelo Persona."""
    direccion = DireccionSerializer(source="id_direccion", read_only=True)

    class Meta:
        model = Persona
        fields = ("id", "nombre", "apellidos", "dni", "fecha_nacimiento", "sexo", "telefono_fijo", "telefono_movil",
                  "direccion", )


class ClasificacionRecursoComunitarioSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Clasificacion_Recurso_Comunitario"""
    class Meta:
        model = Clasificacion_Recurso_Comunitario
        fields = ("id", "nombre",)


class TipoRecursoComunitarioSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Tipo_Recurso_Comunitario."""
    clasificacion_recurso_comunitario = \
        ClasificacionRecursoComunitarioSerializer(source="id_clasificacion_recurso_comunitario")

    class Meta:
        model = Tipo_Recurso_Comunitario
        fields = ("id", "nombre", "clasificacion_recurso_comunitario",)

    def create(self, validated_data):
        info_clasificacion_recurso = validated_data.get("id_clasificacion_recurso_comunitario")
        clasificacion_recurso, _ = Clasificacion_Recurso_Comunitario.objects.get_or_create(**info_clasificacion_recurso)

        tipo_recurso = Tipo_Recurso_Comunitario.objects.create(
            nombre=validated_data.get("nombre"),
            id_clasificacion_recurso_comunitario=clasificacion_recurso,
        )
        return tipo_recurso


class TipoRecursoComunitarioReadSerializer(serializers.ModelSerializer):
    """Serializador de solo lectura para el modelo Tipo_Recurso_Comunitario."""
    clasificacion_recurso_comunitario = \
        ClasificacionRecursoComunitarioSerializer(source="id_clasificacion_recurso_comunitario", read_only=True)

    class Meta:
        model = Tipo_Recurso_Comunitario
        fields = ("id", "nombre", "clasificacion_recurso_comunitario",)


class RecursoComunitarioSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Recurso_Comunitario"""
    tipo_recurso_comunitario = TipoRecursoComunitarioSerializer(source="id_tipos_recurso_comunitario")
    direccion = DireccionSerializer(source="id_direccion")

    class Meta:
        model = Recurso_Comunitario
        fields = ("id", "nombre", "telefono", "tipo_recurso_comunitario", "direccion",)

    def create(self, validated_data):
        info_tipo_recurso = validated_data.get("id_tipos_recurso_comunitario")
        info_clasificacion_recurso = info_tipo_recurso.get("id_clasificacion_recurso_comunitario")
        clasificacion_recurso, _ = Clasificacion_Recurso_Comunitario.objects.get_or_create(**info_clasificacion_recurso)
        info_tipo_recurso["id_clasificacion_recurso_comunitario"] = clasificacion_recurso
        tipo_recurso, _ = Tipo_Recurso_Comunitario.objects.get_or_create(**info_tipo_recurso)

        recurso = Recurso_Comunitario.objects.create(
            nombre=validated_data.get("nombre"),
            telefono=validated_data.get("telefono"),
            id_tipos_recurso_comunitario=tipo_recurso,
        )
        return recurso


class RecursoComunitarioReadSerializer(serializers.ModelSerializer):
    """Serializador de solo lectura para el modelo Recurso_Comunitario."""
    tipo_recurso_comunitario = TipoRecursoComunitarioSerializer(source="id_tipos_recurso_comunitario", read_only=True)
    direccion = DireccionSerializer(source="id_direccion", read_only=True)

    class Meta:
        model = Recurso_Comunitario
        fields = ("id", "nombre", "telefono", "tipo_recurso_comunitario", "direccion",)


class TipoViviendaSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Tipo_Vivienda."""
    class Meta:
        model = Tipo_Vivienda
        fields = ("id", "nombre",)


class TipoSituacionSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Tipo_Situacion."""
    class Meta:
        model = Tipo_Situacion
        fields = ("id", "nombre",)


class TerminalSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Terminal."""
    titular = serializers.ModelSerializer(source="id_titular")
    tipo_vivienda = TipoViviendaSerializer(source="id_tipo_vivienda")
    tipo_situacion = TipoSituacionSerializer(source="id_tipo_situacion")

    class Meta:
        model = Terminal
        fields = ("id", "numero_terminal", "modo_acceso_vivienda", "barreras_arquitectonicas", "modelo_terminal",
                  "fecha_tipo_situacion", "titular", "tipo_vivienda", "tipo_situacion",)
        depth = 1

    def create(self, validated_data):
        info_titular = validated_data.get("id_titular")
        titular, _ = Paciente.objects.get_or_create(**info_titular)

        info_tipo_vivienda = validated_data.get("id_tipo_vivienda")
        tipo_vivienda, _ = Tipo_Vivienda.objects.get_or_create(**info_tipo_vivienda)

        info_tipo_situacion = validated_data.get("id_tipo_situacion")
        tipo_situacion, _ = Tipo_Situacion.objects.get_or_create(**info_tipo_situacion)

        terminal = Terminal.objects.create(
            numero_terminal=validated_data.get("numero_terminal"),
            modo_acceso_vivienda=validated_data.get("tipo_acceso_vivienda"),
            barreras_arquitectonicas=validated_data.get("barreras_arquitectonicas"),
            modelo_terminal=validated_data.get("modelo_terminal"),
            fecha_tipo_situacion=validated_data.get("fecha_tipo_situacion"),
            id_titular=titular,
            id_tipo_vivienda=tipo_vivienda,
            id_tipo_situacion=tipo_situacion,
        )
        return terminal


class TerminalReadSerializer(serializers.ModelSerializer):
    """Serializador de solo lectura para el modelo Terminal."""
    titular = serializers.ModelSerializer(source="id_titular", read_only=True)
    tipo_vivienda = TipoViviendaSerializer(source="id_tipo_vivienda", read_only=True)
    tipo_situacion = TipoSituacionSerializer(source="id_tipo_situacion", read_only=True)

    class Meta:
        model = Terminal
        fields = ("id", "numero_terminal", "modo_acceso_vivienda", "barreras_arquitectonicas", "modelo_terminal",
                  "fecha_tipo_situacion", "titular", "tipo_vivienda", "tipo_situacion",)
        depth = 1


class TipoModalidadPacienteSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Tipo_Modalidad_Paciente."""
    class Meta:
        model = Tipo_Modalidad_Paciente
        fields = ("id", "nombre", )


class PacienteSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Paciente."""
    terminal = TerminalSerializer(source="id_terminal")
    persona = PersonaSerializer(source="id_persona")
    modalidad_paciente = TipoModalidadPacienteSerializer(source="id_tipo_modalidad_paciente")

    class Meta:
        model = Paciente
        fields = ("id", "tiene_ucr", "numero_expediente", "numero_seguridad_social",
                  "prestacion_otros_servicios_sociales", "observaciones_medicas", "intereses_y_actividades",
                  "terminal", "persona", "modalidad_paciente")

    def create(self, validated_data):
        info_terminal = validated_data.get("id_terminal")
        terminal, _ = Terminal.objects.get_or_create(**info_terminal)

        info_persona = validated_data.get("id_persona")
        persona, _ = Persona.objects.get_or_create(**info_persona)

        info_modalidad_paciente = validated_data.get("id_tipo_modalidad_paciente")
        modalidad_paciente, _ = Tipo_Modalidad_Paciente.objects.get_or_create(**info_modalidad_paciente)

        paciente = Paciente.objects.create(
            tiene_ucr=validated_data.get("tiene_ucr"),
            numero_expediente=validated_data.get("numero_expediente"),
            numero_seguridad_social=validated_data.get("numero_seguridad_social"),
            prestacion_otros_servicios_sociales=validated_data.get("prestacion_otros_servicios_sociales"),
            observaciones_medicas=validated_data.get("observaciones_medicas"),
            intereses_y_actividades=validated_data.get("intereses_y_actividades"),
            id_terminal=terminal,
            id_persona=persona,
            id_tipo_modalidad_paciente=modalidad_paciente,
        )
        return paciente


class PacienteReadSerializer(serializers.ModelSerializer):
    """Serializador de solo lectura para el modelo Paciente."""
    terminal = TerminalSerializer(source="id_terminal", read_only=True)
    persona = PersonaSerializer(source="id_persona", read_only=True)
    modalidad_paciente = TipoModalidadPacienteSerializer(source="id_tipo_modalidad_paciente", read_only=True)

    class Meta:
        model = Paciente
        fields = ("id", "tiene_ucr", "numero_expediente", "numero_seguridad_social",
                  "prestacion_otros_servicios_sociales", "observaciones_medicas", "intereses_y_actividades",
                  "terminal", "persona", "modalidad_paciente")


class RelacionPacientePersonaSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Relacion_Paciente_Persona."""
    paciente = PacienteSerializer(source="id_paciente")

    class Meta:
        model = Relacion_Paciente_Persona
        fields = ("id", "nombre", "apellidos", "telefono", "tipo_relacion", "tiene_llaves_vivienda", "disponibilidad",
                  "observaciones", "prioridad", "es_conviviente", "tiempo_domicilio", "paciente", )

    def create(self, validated_data):
        info_paciente = validated_data.get("id_paciente")
        paciente, _ = Paciente.objects.get_or_create(**info_paciente)

        relacion = Relacion_Paciente_Persona.objects.create(
            nombre=validated_data.get("nombre"),
            apellidos=validated_data.get("apellidos"),
            telefono=validated_data.get("telefono"),
            tipo_relacion=validated_data.get("tipo_relacion"),
            tiene_llaves_vivienda=validated_data.get("tiene_llaves_vivienda"),
            disponibilidad=validated_data.get("disponibilidad"),
            observaciones=validated_data.get("observaciones"),
            prioridad=validated_data.get("prioridad"),
            es_conviviente=validated_data.get("es_conviviente"),
            tiempo_domicilio=validated_data.get("tiempo_domicilio"),
            id_paciente=paciente,
        )
        return relacion


class RelacionPacientePersonaReadSerializer(serializers.ModelSerializer):
    """Serializador de solo lectura para el modelo Relacion_Paciente_Persona."""
    paciente = PacienteSerializer(source="id_paciente", read_only=True)

    class Meta:
        model = Relacion_Paciente_Persona
        fields = ("id", "nombre", "apellidos", "telefono", "tipo_relacion", "tiene_llaves_vivienda", "disponibilidad",
                  "observaciones", "prioridad", "es_conviviente", "tiempo_domicilio", "paciente", )


class ClasificacionAlarmaSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Clasificacion_Alarma."""
    class Meta:
        model = Clasificacion_Alarma
        fields = ("id", "nombre", "codigo", )


class TipoAlarmaSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Tipo_Alarma."""
    clasificacion = ClasificacionAlarmaSerializer(source="id_clasificacion_alarma")

    class Meta:
        model = Tipo_Alarma
        fields = ("id", "nombre", "codigo", "es_dispositivo", "clasificacion", )

    def create(self, validated_data):
        info_clasificacion = validated_data.get("id_clasificacion_alarma")
        clasificacion, _ = Clasificacion_Alarma.objects.get_or_create(**info_clasificacion)

        tipo_alarma = Tipo_Alarma.objects.create(
            nombre=validated_data.get("nombre"),
            codigo=validated_data.get("codigo"),
            es_dispositivo=validated_data.get("es_dispositivo"),
            id_clasificacion_alarma=clasificacion,
        )
        return tipo_alarma


class TipoAlarmaReadSerializer(serializers.ModelSerializer):
    """Serializador de solo lectura para el modelo Tipo_Alarma."""
    clasificacion = ClasificacionAlarmaSerializer(source="id_clasificacion_alarma", read_only=True)

    class Meta:
        model = Tipo_Alarma
        fields = ("id", "nombre", "codigo", "es_dispositivo", "clasificacion", )


class AlarmaSerializer(serializers.ModelSerializer):
    """Serializador para el modelo Alarma."""
    tipo_alarma = TipoAlarmaSerializer(source="id_tipo_alarma")
    teleoperador = UserSerializer(source="id_teleoperador")

    class Meta:
        model = Alarma
        fields = ("id", "estado_alarma", "fecha_registro", "observaciones", "resumen", "tipo_alarma", "teleoperador", )

    def create(self, validated_data):
        info_tipo_alarma = validated_data.get("id_tipo_alarma")
        tipo_alarma, _ = Tipo_Alarma.objects.get_or_create(**info_tipo_alarma)

        info_teleoperador = validated_data.get("id_teleoperador")
        teleoperador, _ = User.objects.get_or_create(**info_teleoperador)

        alarma = Alarma.objects.create(
            estado_alarma=validated_data.get("estado_alarma"),
            fecha_registro=validated_data.get("fecha_registro"),
            observaciones=validated_data.get("observaciones"),
            resumen=validated_data.get("resumen"),
            id_tipo_alarma=tipo_alarma,
            id_teleoperador=teleoperador,
        )
        return alarma


class AlarmaReadSerializer(serializers.ModelSerializer):
    """Serializador de solo lectura para el modelo Alarma."""
    tipo_alarma = TipoAlarmaSerializer(source="id_tipo_alarma", read_only=True)
    teleoperador = UserSerializer(source="id_teleoperador", read_only=True)

    class Meta:
        model = Alarma
        fields = ("id", "estado_alarma", "fecha_registro", "observaciones", "resumen", "tipo_alarma", "teleoperador", )
