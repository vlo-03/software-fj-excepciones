# Excepciones personalizadas para el sistema de Software FJ.
# Todas heredan de Exception para diferenciar errores de negocio y validación.


class ErrorSistemaSoftwareFJ(Exception):
    """Excepción base general del sistema Software FJ."""
    pass  # Permite capturar cualquier error propio del sistema si se requiere


class ErrorValidacionCliente(ErrorSistemaSoftwareFJ):
    """Se lanza cuando los datos de un cliente son inválidos o están incompletos."""
    pass  # Excepción específica para validaciones de la clase Cliente


class ErrorParametroServicio(ErrorSistemaSoftwareFJ):
    """Se lanza cuando un servicio recibe parámetros inválidos o faltantes."""
    pass  # Excepción específica para validación de parámetros en servicios


class ServicioNoDisponibleError(ErrorSistemaSoftwareFJ):
    """Se lanza cuando se intenta reservar o usar un servicio no disponible."""
    pass  # Excepción específica para indisponibilidad de servicios


class ErrorReserva(ErrorSistemaSoftwareFJ):
    """Se lanza cuando ocurre un error al crear, confirmar, cancelar o procesar una reserva."""
    pass  # Excepción específica para el ciclo de vida de una reserva


class ErrorCalculoCosto(ErrorSistemaSoftwareFJ):
    """Se lanza cuando hay inconsistencias o valores inválidos al calcular costos."""
    pass  # Excepción específica para fallos en cálculos financieros/costos
