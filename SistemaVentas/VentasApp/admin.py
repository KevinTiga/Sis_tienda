from django.contrib import admin
from .models import Cliente, Producto, Empresa, Proveedor, Empleado, Factura
# Register your models here.



from django.contrib import admin
from .models import Cliente, Producto, Empresa, Proveedor, Empleado, Factura

# Configuración para el modelo Cliente
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombre', 'apellido', 'telefono', 'email', 'fecha_nacimiento', 'fecha_creacion')
    search_fields = ('cedula', 'nombre', 'apellido', 'email')
    list_filter = ('fecha_creacion',)
    ordering = ('nombre', 'apellido')

# Configuración para el modelo Producto
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'marca', 'precio', 'cantidad_stock', 'fecha_ingreso', 'fecha_vencimiento')
    search_fields = ('codigo', 'nombre', 'marca')
    list_filter = ('fecha_ingreso', 'fecha_vencimiento', 'caracteristicas_categoria')
    ordering = ('nombre',)
    list_editable = ('precio', 'cantidad_stock')

# Configuración para el modelo Empresa
@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('ruc', 'nombre', 'direccion', 'telefono', 'email')
    search_fields = ('ruc', 'nombre', 'email')
    ordering = ('nombre',)

# Configuración para el modelo Proveedor
@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombre', 'apellido', 'telefono', 'email', 'empresa')
    search_fields = ('cedula', 'nombre', 'apellido', 'email', 'empresa__nombre')
    list_filter = ('empresa',)
    ordering = ('nombre', 'apellido')

# Configuración para el modelo Empleado
@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombre', 'apellido', 'telefono', 'email', 'fecha_nacimiento', 'fecha_creacion')
    search_fields = ('cedula', 'nombre', 'apellido', 'email')
    list_filter = ('fecha_creacion',)
    ordering = ('nombre', 'apellido')

# Configuración para el modelo Factura
@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('codigo_factura', 'fecha_factura', 'cliente', 'empleado', 'producto', 'cantidad', 'subtotal', 'iva', 'total')
    search_fields = ('codigo_factura', 'cliente__nombre', 'empleado__nombre', 'producto__nombre')
    list_filter = ('fecha_factura',)
    ordering = ('-fecha_factura',)




