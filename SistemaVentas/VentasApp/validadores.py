from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from datetime import date, timedelta

# Validadores personalizados

def validacion_numeros(value):
    if not value.isdigit():
        raise ValidationError("El valor debe contener solo números.")

def validacion_letras(value):
    if not value.isalpha():
        raise ValidationError("El valor debe contener solo letras.")

# Expresiones regulares
validacion_especial = RegexValidator(
    regex=r'^[a-zA-Z\s]+$',
    message="El campo solo debe contener letras y espacios."
)

validacion_especial2 = RegexValidator(
    regex=r'^[a-zA-Z0-9\s]+$',
    message="El campo solo debe contener letras, números y espacios."
)

validacion_especial3 = RegexValidator(
    regex=r'^[a-zA-Z0-9,.-ó\s]+$',
    message="El campo solo debe contener letras, números, comas, guiones y espacios."
)

# Validar fecha de nacimiento (mayor de edad)
def validar_fecha_nacimiento_cliente(fecha_nacimiento):
    hoy = date.today()
    if fecha_nacimiento > hoy:
        raise ValidationError("La fecha de nacimiento no puede ser posterior a hoy.")
    edad = hoy.year - fecha_nacimiento.year - (
        (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
    )
    if edad < 18:
        raise ValidationError("El cliente debe ser mayor de edad (al menos 18 años).")

# Validar edad máxima
def validacion_edad_maxima(fecha_nacimiento):
    edad = (date.today() - fecha_nacimiento).days // 365
    if edad > 60:
        raise ValidationError("La edad máxima permitida es de 60 años.")

# Validar fechas de creación y vencimiento
def validacion_fechas_creacion_vencimiento(fecha_creacion, fecha_vencimiento):
    if fecha_creacion == fecha_vencimiento:
        raise ValidationError("La fecha de creación no puede ser igual a la fecha de vencimiento.")

def validacion_fecha_vencimiento(fecha_creacion, fecha_vencimiento):
    if fecha_vencimiento > fecha_creacion + timedelta(days=5 * 365):
        raise ValidationError("La fecha de vencimiento no puede exceder 5 años desde la fecha de creación.")

# Validar fecha de elaboración
def validar_fecha_elaboracion(value):
    if value > date.today():
        raise ValidationError("La fecha de elaboración no puede ser futura.")

# Validar fecha de vencimiento
def validar_fecha_vencimiento(value, fecha_elaboracion):
    if value <= fecha_elaboracion:
        raise ValidationError("La fecha de vencimiento debe ser posterior a la fecha de elaboración.")
