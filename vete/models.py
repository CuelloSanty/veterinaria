from django.db import models


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
