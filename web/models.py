from django.db import models
from django.contrib.auth.models import User

class Dueno(models.Model):
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class Vacuna(models.Model):
    nombre = models.CharField(max_length=50)
    laboratorio = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Mascota(models.Model):
    nombre = models.CharField(max_length=50)
    especie = models.CharField(max_length=20)
    dueno = models.ForeignKey( # La relación entre Mascota y Dueno se establece mediante una clave foránea (ForeignKey) que apunta al modelo Dueno. Esto significa que cada mascota está asociada a un dueño específico, y se pueden tener múltiples mascotas asociadas al mismo dueño. La opción 'on_delete=models.SET_NULL' indica que, si un dueño es eliminado de la base de datos, el campo 'dueno' en las mascotas asociadas se establecerá en NULL en lugar de eliminar las mascotas. Las opciones 'null=True' y 'blank=True' permiten que el campo 'dueno' sea opcional, lo que significa que una mascota puede existir sin estar asociada a un dueño. La opción 'related_name="mascotas"' permite acceder a las mascotas asociadas a un dueño utilizando el atributo 'mascotas' en la instancia de Dueno, lo que facilita la consulta de las mascotas de un dueño específico. Por ejemplo, si se tiene una instancia de Dueno llamada 'dueno1', se puede acceder a sus mascotas utilizando 'dueno1.mascotas.all()'.
        Dueno,
        on_delete = models.SET_NULL,
        null = True,
        blank = True, # blank se utiliza para permitir que el campo 'dueno' pueda estar vacío en los formularios de Django, lo que es útil cuando se quiere crear una mascota sin asignarle un dueño en ese momento. Esto es especialmente útil en situaciones donde se desea registrar una mascota antes de tener la información del dueño, o cuando se quiere permitir que las mascotas existan sin un dueño específico.
        related_name='mascotas' # La opción 'related_name' se utiliza para establecer un nombre de relación inversa, lo que permite acceder a las mascotas asociadas a un dueño utilizando el atributo 'mascotas' en la instancia de Dueno. Esto facilita la consulta de las mascotas de un dueño específico. Por ejemplo, si se tiene una instancia de Dueno llamada 'dueno1', se puede acceder a sus mascotas utilizando 'dueno1.mascotas.all()'.
    )
    vacunas = models.ManyToManyField( #vacunas es una relación muchos a muchos con la clase Vacuna. Esto significa que una mascota puede tener varias vacunas asociadas, y una vacuna puede estar asociada a varias mascotas.
        Vacuna,
        related_name="mascotas_vacunas" #mascotas_vacunas es el nombre de la relación inversa que se puede utilizar para acceder a las mascotas asociadas a una vacuna específica. Por ejemplo, si se tiene una instancia de Vacuna llamada 'vacuna1', se puede acceder a las mascotas asociadas a esa vacuna utilizando 'vacuna1.mascotas_vacunas.all()'.
    )

    def __str__(self):
        return f"{self.nombre} ({self.especie})"

class ExpedienteMedico(models.Model):
    mascota = models.OneToOneField(
        Mascota,
        on_delete= models.CASCADE,
        primary_key= True,
        related_name="expediente"
    )
    fecha_ultima_visita = models.DateField()
    diagnostico = models.TextField()
    
    def __str__(self):
        return f"Expediente de {self.mascota.nombre} ({self.mascota.especie})" # El método __str__ se ha personalizado para mostrar el nombre de la mascota y su especie, lo que facilita la identificación del expediente médico asociado a cada mascota cuando se visualizan en el panel de administración de Django o en otras partes del proyecto donde se necesite mostrar información sobre los expedientes médicos.
 

class UserProfile(models.Model):
    # A continuación, ejemplos de algunos campos que se quieren asociar al usuario
    # Se pueden agregar más campos según las necesidades del proyecto
    # Por ejemplo, se podría agregar un campo para la dirección del usuario, o para su número de teléfono, o para su fecha de nacimiento, etc.
    tipos = (
        ('cliente', 'Cliente'), # Asumiendo que los tipos de usuario son 'cliente' y 'operario'
        ('operario', 'Operario'),
    )
    tipo = models.CharField(max_length=50, default='cliente', choices=tipos) # El campo 'tipo' se utiliza para diferenciar entre los diferentes tipos de usuarios, y se establece un valor por defecto de 'cliente' para que, si no se especifica un tipo al crear un usuario, se asigne automáticamente el tipo 'cliente'.
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE) # El campo 'user' es una relación uno a uno con el modelo User de Django, lo que significa que cada instancia de UserProfile está asociada a una única instancia de User, y viceversa. La opción 'related_name' se utiliza para establecer un nombre de relación inversa, lo que permite acceder al perfil del usuario desde la instancia de User utilizando 'user.userprofile'.

    def __str__(self): # Este método se utiliza para representar la instancia de UserProfile como una cadena de texto, y se ha personalizado para mostrar el id del usuario, su nombre completo (nombre y apellido), su nombre de usuario, y su tipo de usuario. Esto facilita la identificación de cada perfil de usuario cuando se visualizan en el panel de administración de Django o en otras partes del proyecto donde se necesite mostrar información sobre los usuarios.
        id = self.user.id
        nombre = self.user.first_name
        apellido = self.user.last_name
        usuario = self.user.username
        tipo = self.tipo
        return f'{id} | {nombre} {apellido} | {usuario} | {tipo}' 




