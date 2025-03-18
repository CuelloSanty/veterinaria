# Instituto Dr. Carlos María Carena: Presentación del Proyecto Final 2025
<hr>

>[!NOTE]
>Este proyecto Unicamente es escolar

## Configuración Inicial de un Proyecto Django

Esta guía te ayudará a configurar un proyecto Django desde un repositorio existente, realizar las migraciones necesarias y crear un superusuario.

---

### **1. Clonar el repositorio del proyecto**
Abre tu terminal y ejecuta el siguiente comando para clonar el repositorio:

```bash
git clone https://github.com/CuelloSanty/veterinaria.git
````
>[!TIP]
>Al clonar el repositorio asegurate de esta realizar los siguientes comandos, en la carpeta "veterinaria"
### **2. Crear migraciones de no tenerlas**
```bash
python manage.py makemigrations
````
>[!NOTE]
>En Django, las migraciones son una forma de gestionar los cambios en la estructura de la base de datos de tu proyecto. Básicamente, sirven para sincronizar el modelo de datos definido en el código Python (los models.py) con la base de datos real que utiliza tu aplicación
### **3. Migrarlo**
```bash
python manage.py migrate
````
### **4. Crear un super usuarior**
>[!NOTE]
>Ademas el super usuario de llama "staff" en los proyectos dajngo
```bash
python manage.py createsuperuser
````
>[!IMPORTANT]
>Es sumamente Importante que crees un usuario al contrario el sistema entrara en modo fallo
### Proyecto Veterina la cucha

### Links a docuemnto de diagramas

[Documento de diagramas](https://docs.google.com/document/d/1LQO2MToAFLjsmfHMEtaHMNgcC2pTqcuNrIlhqEyJZqk/edit?usp=sharing)
### Links de docuemnto tesis

[Documento_Tesis](https://docs.google.com/document/d/1nzVrZ4r2uNMaKcOJUtP5nHdKVUvF9E-6hl5mMrEZeQI/edit?usp=sharing)

<hr>

# **Introducción a Django**

Django es un framework de desarrollo web de alto nivel para Python que permite a los desarrolladores crear aplicaciones web rápidas, escalables y seguras. Fue diseñado con el objetivo de simplificar tareas comunes de desarrollo y facilitar la creación de aplicaciones complejas.

---

## **¿Qué hace especial a Django?**

### 1. **Rápido desarrollo**
Django sigue el principio **DRY (Don’t Repeat Yourself)**, lo que significa que minimiza la redundancia en el código y acelera el desarrollo.

<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRz4XEvFCZozRglB2E_XEpXNRXwVk6pE1I7mQ&s" style="border-radius:50%;">

### 2. **Incluye todo lo esencial**
Es un framework "baterías incluidas", lo que significa que viene con muchas funcionalidades listas para usar, como autenticación, administración, manejo de formularios, generación de URLs y mucho más.

### 3. **Altamente escalable**
Desde proyectos pequeños hasta sistemas masivos, Django se adapta fácilmente y es utilizado por empresas como Instagram y Spotify.

### 4. **Seguridad robusta**
Django tiene medidas integradas para prevenir problemas comunes de seguridad, como inyecciones SQL, cross-site scripting (XSS) y cross-site request forgery (CSRF).

<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR2O2Bms3bx40dmE2O9WY-jLbFOodFHVjJ_fg&s" style="border-radius:50%;">

### 5. **Código abierto y comunidad activa**
Django es un proyecto de código abierto con una comunidad global de desarrolladores, lo que garantiza actualizaciones frecuentes y una amplia base de recursos de aprendizaje.

---

## **Ventajas de Usar Django**

| Característica        | Beneficio                                                    |
|-----------------------|-------------------------------------------------------------|
| **Sistema ORM**       | Interactúa con bases de datos sin escribir consultas SQL.   |
| **Panel de Admin**    | Un panel listo para gestionar tu aplicación de manera visual. |
| **Modularidad**       | Reutiliza componentes como aplicaciones dentro de tu proyecto. |
| **Soporte de Templating** | Genera vistas HTML dinámicas de forma sencilla.             |
| **Multiplataforma**   | Funciona en diferentes sistemas operativos con facilidad.    |

---

## **Casos de Uso**
- **Plataformas de comercio electrónico**: Administración eficiente de usuarios, productos y transacciones.
- **Redes sociales y foros**: Creación de funcionalidades como perfiles, seguidores y publicación de contenido.
- **Sistemas empresariales**: Gestión de inventarios, reportes o sistemas de facturación.

---

## **¿Por qué elegir Django?**
Django es perfecto si:
- Quieres desarrollar rápido y con una estructura sólida.
- Necesitas un framework confiable con medidas de seguridad integradas.
- Deseas una solución escalable que pueda crecer con tu proyecto.
- Prefieres una herramienta con documentación detallada y una comunidad activa.

---

## **Conclusión**
Django te permite enfocarte en la lógica de tu aplicación en lugar de reinventar la rueda con cada proyecto. Es ideal para desarrolladores que buscan combinar rapidez, flexibilidad y robustez.

¡Con Django puedes convertir tus ideas en aplicaciones web de calidad profesional sin complicaciones!

# Bonus
>[!TIP]
>Con Django es usar las vistas genéricas basadas en clases (Class-Based Views, CBVs) cuando sea posible. Estas vistas son muy poderosas y te permiten ahorrar tiempo y reducir código redundante. Por ejemplo, si solo necesitas mostrar una lista de objetos o un detalle, puedes usar ListView o DetailView, respectivamente.

````python 
from django.views.generic import ListView
from .models import TuModelo

class TuModeloListView(ListView):
    model = TuModelo
    template_name = 'tu_modelo_list.html'
````

#### Control De stock Nativo

>[!NOTE]
>Este código define una función para gestionar cambios en datos relacionados con formularios y una base de datos.
````python
def function(db_formset_after, db_formset_before,DbToChanged):
    def GetData(cleaned_form):
        return {"id":cleaned_form.get('id'),"cantidad": cleaned_form.get('cantidad'),"art":cleaned_form.get('articulo')}
    def PushToDb(id, cantidad, operation, db_to_change):
        db = db_to_change.objects.get(pk=id)
        if operation == 1:  
            db.cantidad += cantidad
            db.save()
        if operation == 2:
            if not cantidad > db.cantidad:
                db.cantidad -= cantidad
                db.save()
        else: pass
    def GetPreviousToCompare(db_formset_after,id_before, before):
        op = None
        cantidad = None
        if  id_before == None: 
            return PushToDb(before["art"].codigo, before["cantidad"], 2, DbToChanged)
        if not id_before == None:
            db_prev = db_formset_after.get(id=int(str(id_before)))
            after = {"id":db_prev.id,"cantidad":db_prev.cantidad,"art":db_prev.articulo}
        # Operations
            if after["cantidad"] < before["cantidad"]:
                cantidad = after["cantidad"] - before["cantidad"]
                op = 1
            if after["cantidad"] > before["cantidad"]:
                cantidad = before["cantidad"] - after["cantidad"]
                op = 2
            if before["cantidad"] == 0: 
                PushToDb(before["art"].codigo,after["cantidad"],1 , DbToChanged)
            PushToDb(before["art"].codigo, cantidad ,op,DbToChanged)

    deleted_forms = db_formset_before.deleted_forms
    if deleted_forms:
        for form in deleted_forms:
            data = GetData(form.cleaned_data)
            PushToDb(data['art'].codigo, data["cantidad"], 2, DbToChanged)
    if db_formset_before:
        for form in db_formset_before:
            if form.has_changed():   
                data = GetData(form.cleaned_data)
                GetPreviousToCompare(db_formset_after, data["id"], data)

````
>[!TIP]
>Si buscas este codigo en internet, No lo encontaras ya que es propio y licenciado.

### *Aquí tienes un resumen:*

Función GetData: Extrae información clave (id, cantidad, art) de un formulario limpio y la devuelve como un diccionario.
Función PushToDb: Actualiza los datos de la base de datos en función de una operación:
Suma (operation == 1) una cantidad al campo cantidad.
Resta (operation == 2) una cantidad si el resultado no es negativo.

Función GetPreviousToCompare: Compara los datos actuales (after) con los datos previos (before). Según los cambios en cantidad, decide si realizar una operación de suma o resta en la base de datos.

Gestión de formularios eliminados: Si hay formularios eliminados (deleted_forms), reduce la cantidad correspondiente en la base de datos.

Gestión de cambios en formularios existentes: Para cada formulario que ha cambiado, extrae los datos y compara los valores actuales con los anteriores, aplicando las operaciones necesarias.

En resumen, este código centraliza la lógica para mantener sincronizados los cambios entre formularios y la base de datos, gestionando operaciones de aumento o disminución en las cantidades almacenadas




