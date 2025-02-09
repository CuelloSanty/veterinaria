from django.db import models

class Proveedore(models.Model):
    cuit = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=30)
    direccion = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(unique=True,  blank=True, null=True)
    
    def __str__(self):
        return self.nombre
class Articulo(models.Model):
    MEDICAMENTO = 'Med'
    ALIMENTO = 'Alim'
    ACCESORIO = 'Acc'
    OTRO = 'Otro'
    tipo = [
        ('Med', 'Medicamento'),
        ('Alim', 'Alimento'),
        ('Acc', 'Accesorio'),
    ]
    BOLSA = 'Bol'
    CAJA = 'Caj'
    SOBRE = 'Sob'
    COMPRIMIDO = 'Com'
    UNIDAD = 'Uni'
    KILOS = 'Alim'
    GRAMOS = 'Gra'
    LITROS = 'Acc'
    MILILITROS = 'Mil'
    OTRO = 'Otro'
    medidas = [
        ('Bol', 'Bolsa'),
        ('Caj', 'Caja'),
        ('Sob', 'Sobre'),
        ('Com', 'Comprimido'),
        ('Uni', 'Unidad'),
        ('Kil', 'Kilos'),
        ('Gra', 'Gramos'),
        ('Mil', 'Mililitros'),
        ('Lit', 'Litros'),
        ('Otro', 'Otro')
    ]


    # Campo [Open]
    codigo = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=150,blank=True, null=True)
    img = models.URLField(max_length=655, blank=True, null=True)
    marca = models.CharField(max_length=30)
    
    # No Obligatorio
    peso = models.DecimalField(max_digits=5, decimal_places=3,blank=True, default=None,null=True)
    talle = models.DecimalField(max_digits=2,decimal_places=1,default=None,blank=True,null=True)
    vencimiento = models.DateField(default=None, blank=True,null=True)
    
    unidad = models.CharField(max_length=5, choices=medidas, default=KILOS)

    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    proveedor = models.ForeignKey(Proveedore, related_name='Articulos', on_delete=models.CASCADE)
    stock_minimo = models.IntegerField(blank=True, null=True)
    
    # Campo
    tipo = models.CharField(max_length=5, choices=tipo, default=MEDICAMENTO)
    tipo_mascota = models.CharField(max_length=5, choices=[('perro',"Perro"), ('gato','Gato')])
    # campo [end]

    def __str__(self):
        return self.nombre




class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    FechaContratacion = models.DateField()
    MAN = "Mañana"
    TAR = "Tarde"
    FUT = "Completa"
    Turno = [(MAN,"Mañana"),(TAR,"Tarde"),(FUT,"Completa")]
    TurnoChoice = models.CharField(max_length=8, choices=Turno, default="")
    sueldo = models.IntegerField(default=None)

    def __str__(self):
        return self.nombre

class Adelanto(models.Model):
    empleado = models.ForeignKey(Empleado, related_name='adelantos', on_delete=models.CASCADE)
    Monto = models.IntegerField(default=None)
    FechaAdelanto = models.DateField()

    def __str__(self):
        return f"{self.Monto} - {self.FechaAdelanto}"

class Cliente(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    direccion = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.CharField(max_length=10,  blank=True, null=True)
    email = models.EmailField(unique=True,  blank=True, null=True)
    
    def __str__(self):
        return self.nombre

class Mascota(models.Model):
    nombre = models.CharField(max_length=30)
    raza = models.CharField(max_length=30,  blank=True, null=True)
    edad = models.IntegerField( blank=True, null=True)
    cliente = models.ForeignKey(Cliente, related_name='Clientes', on_delete=models.PROTECT)
    
    def __str__(self):
        return self.nombre

# -----------------------------  Atencion --------------------------------------
class Atencione(models.Model):
    dia = models.DateField()
    hora = models.TimeField(auto_now=False, auto_now_add=False)
    MEDICO = 'Med'
    PELUQUERIA = 'Pel'
    AMBOS = 'Amb'
    tipo = [
        ('Med', 'Medica'),
        ('Pel', 'Peluqueria'),
        ('Amb', 'Ambos'),
    ]
    tipo = models.CharField(max_length=5, choices=tipo, default=MEDICO)
    descripcion = models.CharField(max_length=150)
    Precio_Atencion = models.DecimalField(max_digits=10, decimal_places=2)
    precio_final = models.DecimalField(max_digits=10, decimal_places=2, default=None)
    
    # Foranea
    mascota = models.ForeignKey(Mascota, related_name='mascotas', on_delete=models.CASCADE)
    def __str__(self):
        return str(self.dia)


class ArticuloAtencion(models.Model):
    articulo = models.ForeignKey(Articulo, related_name='articulos', on_delete=models.CASCADE)
    pedido = models.ForeignKey(Atencione, related_name='atencion', on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return str(self.id)
# ------------------------------ Atencion --------------------------------


# ---------------------------- Pedidos -------------------------------------------
class Pedido(models.Model):
    fecha = models.DateField()
    MEDICAMENTO = 'Med'
    ALIMENTO = 'Alim'
    ACCESORIO = 'Acc'
    OTRO = 'Otro'
    tipo = [
        ('Med', 'Medicamento'),
        ('Alim', 'Alimento'),
        ('Acc', 'Accesorio'),
    ]
    tipo = models.CharField(max_length=5, choices=tipo, default=MEDICAMENTO)
    proveedor = models.ForeignKey(Proveedore,related_name='Proveedores', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)    

class DetallePedido(models.Model):
    articulo = models.ForeignKey(Articulo,related_name='Art', on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido,related_name='Ped', on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return str(self.id)
# ---------------------------- Pedidos -------------------------------------------[End]


class Venta(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateField()
    cliente =  models.ForeignKey(Cliente,related_name='CLientes', on_delete=models.PROTECT)
    empleado = models.ForeignKey(Empleado,related_name='EMpleados',on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id)

class DetalleVenta(models.Model):
    id = models.AutoField(primary_key=True)
    venta = models.ForeignKey(Venta,related_name='VEntas', on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulo,related_name='ARticulos', on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=14,decimal_places=3)

    def __str__(self):
        return str(self.id)

# Subs 
class Subscription(models.Model):
    Gmail = models.CharField(max_length=125)
    asunto = models.CharField(max_length=200,default='')
    Nombre = models.CharField(max_length=1000, default='', blank=True)
