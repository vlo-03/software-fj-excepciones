from abc import ABC, abstractmethod  # Permite declarar clases y métodos abstractos
from excepciones import ErrorCalculoCosto, ErrorParametroServicio  # Excepciones de servicios y costos


class Servicio(ABC):
    """Clase abstracta base para los servicios ofrecidos por Software FJ."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, disponible: bool = True) -> None:
        if not isinstance(codigo, str) or not codigo.strip():  # Valida que haya código de servicio
            raise ErrorParametroServicio("El código del servicio es obligatorio.")  # Lanza error si falta
        if not isinstance(nombre, str) or not nombre.strip():  # Valida que haya nombre de servicio
            raise ErrorParametroServicio("El nombre del servicio es obligatorio.")  # Lanza error si falta
        if not isinstance(tarifa_base, (int, float)) or isinstance(tarifa_base, bool) or tarifa_base <= 0:  # Valida tarifa
            raise ErrorParametroServicio("La tarifa base debe ser un número mayor que cero.")  # Lanza error si falla
        self.codigo = codigo.strip().upper()  # Guarda código normalizado
        self.nombre = nombre.strip()  # Guarda nombre limpio
        self.tarifa_base = float(tarifa_base)  # Guarda tarifa base como flotante
        self.disponible = bool(disponible)  # Indica si el servicio está disponible para reservar

    @abstractmethod
    def validar_parametros(self, duracion: int) -> None:
        """Valida parámetros específicos de duración o uso para cada tipo de servicio."""
        pass  # Cada subclase define su propia regla de validación

    @abstractmethod
    def calcular_costo(self, duracion: int, descuento_pct: float = 0.0, impuesto_pct: float = 0.0) -> float:
        """Calcula el costo del servicio soportando descuento e impuesto opcionales (sobrecarga por parámetros)."""
        pass  # Cada subclase calcula el costo según su modelo

    @abstractmethod
    def describir(self) -> str:
        """Retorna una descripción detallada del servicio."""
        pass  # Cada subclase describe sus características

    def _aplicar_ajustes_financieros(self, subtotal: float, descuento_pct: float, impuesto_pct: float) -> float:
        """Aplica descuento e impuesto validados sobre un subtotal y retorna el total."""
        if subtotal < 0:  # Verifica que el subtotal no sea negativo
            raise ErrorCalculoCosto("El subtotal calculado no puede ser negativo.")  # Lanza error de cálculo
        if not (0 <= descuento_pct < 100):  # Valida rango porcentual de descuento
            raise ErrorCalculoCosto("El porcentaje de descuento debe estar entre 0 y menor que 100.")  # Lanza error
        if not (0 <= impuesto_pct <= 100):  # Valida rango porcentual de impuesto
            raise ErrorCalculoCosto("El porcentaje de impuesto debe estar entre 0 y 100.")  # Lanza error
        con_descuento = subtotal * (1 - (descuento_pct / 100.0))  # Aplica el descuento porcentual
        total = con_descuento * (1 + (impuesto_pct / 100.0))  # Aplica el impuesto sobre el valor con descuento
        return round(total, 2)  # Redondea a dos decimales


class ReservaSala(Servicio):
    """Servicio especializado para reserva de salas (duración en horas)."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, capacidad_personas: int, disponible: bool = True) -> None:
        super().__init__(codigo, nombre, tarifa_base, disponible)  # Inicializa atributos comunes de Servicio
        if not isinstance(capacidad_personas, int) or isinstance(capacidad_personas, bool) or capacidad_personas <= 0:  # Valida capacidad
            raise ErrorParametroServicio("La capacidad de la sala debe ser un entero mayor que cero.")  # Lanza error
        self.capacidad_personas = capacidad_personas  # Guarda capacidad máxima de personas

    def validar_parametros(self, duracion: int) -> None:
        """Valida que la reserva de sala sea de al menos 1 hora y máximo 12 horas."""
        if not isinstance(duracion, int) or isinstance(duracion, bool) or not (1 <= duracion <= 12):  # Valida horas
            raise ErrorParametroServicio("La duración de la reserva de sala debe ser un entero entre 1 y 12 horas.")  # Error si falla

    def calcular_costo(self, duracion: int, descuento_pct: float = 0.0, impuesto_pct: float = 0.0) -> float:
        """Calcula el costo de la sala por horas con descuento e impuesto opcionales."""
        self.validar_parametros(duracion)  # Valida duración antes de calcular
        subtotal = self.tarifa_base * duracion  # Calcula subtotal según horas reservadas
        return self._aplicar_ajustes_financieros(subtotal, descuento_pct, impuesto_pct)  # Retorna costo final

    def describir(self) -> str:
        """Describe la sala, su capacidad y su tarifa por hora."""
        estado = "Disponible" if self.disponible else "No disponible"  # Estado legible
        return f"Sala [{self.codigo}] {self.nombre} (Capacidad: {self.capacidad_personas} pers., Tarifa/h: ${self.tarifa_base:.2f}, {estado})"  # Descripción


class AlquilerEquipo(Servicio):
    """Servicio especializado para alquiler de equipos tecnológicos (duración en días)."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, tipo_equipo: str, disponible: bool = True) -> None:
        super().__init__(codigo, nombre, tarifa_base, disponible)  # Inicializa atributos comunes de Servicio
        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():  # Valida tipo de equipo
            raise ErrorParametroServicio("El tipo de equipo es obligatorio para el alquiler.")  # Lanza error
        self.tipo_equipo = tipo_equipo.strip()  # Guarda tipo de equipo

    def validar_parametros(self, duracion: int) -> None:
        """Valida que el alquiler sea entre 1 y 30 días."""
        if not isinstance(duracion, int) or isinstance(duracion, bool) or not (1 <= duracion <= 30):  # Valida días
            raise ErrorParametroServicio("El alquiler de equipo debe ser de entre 1 y 30 días.")  # Error si falla

    def calcular_costo(self, duracion: int, descuento_pct: float = 0.0, impuesto_pct: float = 0.0) -> float:
        """Calcula el costo del alquiler por días con descuento e impuesto opcionales."""
        self.validar_parametros(duracion)  # Valida días antes de calcular
        subtotal = self.tarifa_base * duracion  # Calcula subtotal por días
        return self._aplicar_ajustes_financieros(subtotal, descuento_pct, impuesto_pct)  # Retorna costo final

    def describir(self) -> str:
        """Describe el equipo, categoría y tarifa diaria."""
        estado = "Disponible" if self.disponible else "No disponible"  # Estado legible
        return f"Equipo [{self.codigo}] {self.nombre} (Tipo: {self.tipo_equipo}, Tarifa/día: ${self.tarifa_base:.2f}, {estado})"  # Descripción


class AsesoriaEspecializada(Servicio):
    """Servicio especializado para asesorías técnicas de Software FJ (duración en sesiones)."""

    def __init__(self, codigo: str, nombre: str, tarifa_base: float, especialidad: str, disponible: bool = True) -> None:
        super().__init__(codigo, nombre, tarifa_base, disponible)  # Inicializa atributos comunes de Servicio
        if not isinstance(especialidad, str) or not especialidad.strip():  # Valida especialidad
            raise ErrorParametroServicio("La especialidad de la asesoría es obligatoria.")  # Lanza error
        self.especialidad = especialidad.strip()  # Guarda especialidad

    def validar_parametros(self, duracion: int) -> None:
        """Valida que la asesoría contemple entre 1 y 20 sesiones."""
        if not isinstance(duracion, int) or isinstance(duracion, bool) or not (1 <= duracion <= 20):  # Valida sesiones
            raise ErrorParametroServicio("La asesoría especializada debe tener entre 1 y 20 sesiones.")  # Error si falla

    def calcular_costo(self, duracion: int, descuento_pct: float = 0.0, impuesto_pct: float = 0.0) -> float:
        """Calcula el costo de la asesoría por sesiones con descuento e impuesto opcionales."""
        self.validar_parametros(duracion)  # Valida sesiones antes de calcular
        subtotal = self.tarifa_base * duracion  # Calcula subtotal por sesiones
        return self._aplicar_ajustes_financieros(subtotal, descuento_pct, impuesto_pct)  # Retorna costo final

    def describir(self) -> str:
        """Describe la asesoría, especialidad y tarifa por sesión."""
        estado = "Disponible" if self.disponible else "No disponible"  # Estado legible
        return f"Asesoría [{self.codigo}] {self.nombre} (Área: {self.especialidad}, Tarifa/sesión: ${self.tarifa_base:.2f}, {estado})"  # Descripción
