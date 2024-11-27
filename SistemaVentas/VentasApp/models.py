from django.db import models
from .choices import CATEGORIA
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from .validadores import (
    validacion_numeros,
    validacion_especial,
    validacion_especial2,
    validacion_especial3,
    validacion_letras,
    validacion_edad_maxima,
    validacion_fecha_vencimiento,
    validacion_fechas_creacion_vencimiento,
    validar_fecha_nacimiento_cliente,
    validar_fecha_elaboracion,
    validar_fecha_vencimiento,
)
from decimal import Decimal

class Cliente(models.Model):
    cedula = models.CharField(primary_key=True, max_length=10, validators=[MinLengthValidator(10), validacion_numeros])
    nombre = models.CharField(max_length=100, validators=[validacion_especial])
    apellido = models.CharField(max_length=100, validators=[validacion_especial])
    telefono = models.CharField(max_length=10, validators=[validacion_numeros])
    email = models.EmailField(unique=True)
    direccion = models.CharField(max_length=200)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_nacimiento = models.DateField(validators=[validar_fecha_nacimiento_cliente])

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        db_table = "clientes"


class Producto(models.Model):
    codigo = models.CharField(primary_key=True, max_length=10, unique=True)
    nombre = models.CharField(max_length=50, validators=[validacion_especial3])
    marca = models.CharField(max_length=50, unique=True, validators=[validacion_especial3])
    caracteristicas_categoria = models.CharField(max_length=100, choices=CATEGORIA, validators=[validacion_especial3])
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_stock = models.IntegerField(validators=[MinValueValidator(0)])
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    fecha_elaboracion = models.DateField(validators=[validar_fecha_elaboracion])
    fecha_vencimiento = models.DateField(default='2024-01-01')

    def clean(self):
        validacion_fechas_creacion_vencimiento(self.fecha_elaboracion, self.fecha_vencimiento)
        validacion_fecha_vencimiento(self.fecha_elaboracion, self.fecha_vencimiento)

    def actualizar_stock(self, cantidad):
        self.cantidad_stock -= cantidad
        self.save()

    def __str__(self):
        return f"{self.nombre} ({self.marca})"

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        db_table = "productos"


class Empresa(models.Model):
    ruc = models.CharField(primary_key=True, max_length=13, validators=[MinLengthValidator(10), validacion_numeros])
    nombre = models.CharField(max_length=50, validators=[validacion_especial])
    direccion = models.TextField()
    telefono = models.CharField(max_length=10, validators=[validacion_numeros])
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        db_table = "empresas"


class Proveedor(models.Model):
    cedula = models.CharField(primary_key=True, max_length=10, validators=[MinLengthValidator(10), validacion_numeros])
    nombre = models.CharField(max_length=50, validators=[validacion_especial])
    apellido = models.CharField(max_length=50, validators=[validacion_especial])
    telefono = models.CharField(max_length=10, validators=[validacion_numeros])
    email = models.EmailField(unique=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        db_table = "proveedores"


class Empleado(models.Model):
    cedula = models.CharField(primary_key=True, max_length=10, validators=[MinLengthValidator(10), validacion_numeros])
    nombre = models.CharField(max_length=50, validators=[validacion_especial])
    apellido = models.CharField(max_length=50, validators=[validacion_especial])
    telefono = models.CharField(max_length=10, validators=[validacion_numeros])
    email = models.EmailField(unique=True)
    direccion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_nacimiento = models.DateField(validators=[validacion_edad_maxima])

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        db_table = "empleados"

class Factura(models.Model):
    codigo_factura = models.AutoField(primary_key=True)
    fecha_factura = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="facturas")
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name="facturas")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="facturas")
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="Cantidad")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)
    iva = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)

    def save(self, *args, **kwargs):
        # Calcular subtotal
        self.subtotal = self.cantidad * self.producto.precio
        # Calcular IVA (15% por defecto)
        self.iva = self.subtotal * Decimal('0.15')
        # Calcular total
        self.total = self.subtotal + self.iva

        # Actualizar el stock del producto
        if self.producto.cantidad_stock < self.cantidad:
            raise ValueError("Stock insuficiente para realizar esta factura.")
        self.producto.actualizar_stock(self.cantidad)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Factura {self.codigo_factura} - Cliente: {self.cliente.nombre} - Total: ${self.total:.2f}"

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        db_table = "facturas"
