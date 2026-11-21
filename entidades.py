from abc import ABC, abstractmethod  # Permite definir clases y métodos abstractos en POO
import re  # Permite validar el formato del correo electrónico con expresiones regulares
from excepciones import ErrorValidacionCliente  # Importa la excepción de validación de cliente


class EntidadSistema(ABC):
    """Clase abstracta base para entidades generales del sistema Software FJ."""

    def __init__(self, id_entidad: str) -> None:
        if not isinstance(id_entidad, str) or not id_entidad.strip():  # Verifica que el ID no esté vacío
            raise ErrorValidacionCliente("El identificador de la entidad no puede estar vacío.")  # Lanza error si falla
        self._id_entidad = id_entidad.strip()  # Guarda el ID con atributo protegido por convención

    @property
    def id_entidad(self) -> str:
        """Retorna el identificador de la entidad de forma controlada."""
        return self._id_entidad  # Devuelve el ID protegido

    @abstractmethod
    def resumen(self) -> str:
        """Método abstracto que cada entidad concreta debe implementar."""
        pass  # Obliga a las subclases a definir su propio resumen


class Cliente(EntidadSistema):
    """Representa un cliente de Software FJ con encapsulación y validaciones estrictas."""

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str) -> None:
        super().__init__(id_cliente)  # Inicializa y valida el ID desde EntidadSistema
        self.__nombre = ""  # Atributo privado para el nombre del cliente
        self.__correo = ""  # Atributo privado para el correo electrónico
        self.__telefono = ""  # Atributo privado para el teléfono de contacto
        self.nombre = nombre  # Usa el setter para validar el nombre al crear el objeto
        self.correo = correo  # Usa el setter para validar el correo al crear el objeto
        self.telefono = telefono  # Usa el setter para validar el teléfono al crear el objeto

    @property
    def nombre(self) -> str:
        """Obtiene el nombre completo del cliente."""
        return self.__nombre  # Retorna el atributo privado

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Valida y asigna el nombre del cliente."""
        if not isinstance(valor, str) or len(valor.strip()) < 3:  # Exige texto de al menos 3 caracteres
            raise ErrorValidacionCliente("El nombre del cliente debe tener al menos 3 caracteres.")  # Error si no cumple
        self.__nombre = valor.strip()  # Guarda el nombre limpio

    @property
    def correo(self) -> str:
        """Obtiene el correo electrónico del cliente."""
        return self.__correo  # Retorna el atributo privado

    @correo.setter
    def correo(self, valor: str) -> None:
        """Valida el formato del correo electrónico antes de asignarlo."""
        patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"  # Patrón básico y claro para correos válidos
        if not isinstance(valor, str) or not re.match(patron, valor.strip()):  # Valida tipo y formato
            raise ErrorValidacionCliente("El correo electrónico del cliente no tiene un formato válido.")  # Error si falla
        self.__correo = valor.strip().lower()  # Guarda el correo normalizado en minúsculas

    @property
    def telefono(self) -> str:
        """Obtiene el teléfono del cliente."""
        return self.__telefono  # Retorna el atributo privado

    @telefono.setter
    def telefono(self, valor: str) -> None:
        """Valida que el teléfono contenga solo dígitos (7 a 15 caracteres)."""
        limpio = str(valor).strip() if valor is not None else ""  # Convierte a cadena limpia si existe
        if not limpio.isdigit() or not (7 <= len(limpio) <= 15):  # Comprueba longitud y dígitos
            raise ErrorValidacionCliente("El teléfono debe contener entre 7 y 15 dígitos numéricos.")  # Error si falla
        self.__telefono = limpio  # Guarda el teléfono validado

    def resumen(self) -> str:
        """Implementación del método abstracto con información resumida del cliente."""
        return f"Cliente [{self.id_entidad}] - {self.nombre} | Correo: {self.correo} | Tel: {self.telefono}"  # Texto resumen
