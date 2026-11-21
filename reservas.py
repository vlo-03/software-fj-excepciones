from entidades import Cliente  # Importa la clase Cliente validada
from excepciones import ErrorCalculoCosto, ErrorReserva, ServicioNoDisponibleError  # Excepciones de reservas y costos
from gestor_logs import GestorLogs  # Importa el gestor de registros en archivo .log
from servicios import Servicio  # Importa la clase abstracta Servicio


class Reserva:
    """Representa una reserva que vincula un Cliente, un Servicio, duración y estado."""

    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA")  # Estados permitidos para una reserva

    def __init__(
        self,
        id_reserva: str,
        cliente: Cliente,
        servicio: Servicio,
        duracion: int,
        descuento_pct: float = 0.0,
        impuesto_pct: float = 0.0,
    ) -> None:
        if not isinstance(id_reserva, str) or not id_reserva.strip():  # Valida que exista un ID de reserva
            raise ErrorReserva("El identificador de la reserva es obligatorio.")  # Lanza error si falta
        if not isinstance(cliente, Cliente):  # Valida que el objeto sea instancia de Cliente
            raise ErrorReserva("La reserva requiere un objeto Cliente válido.")  # Lanza error si no lo es
        if not isinstance(servicio, Servicio):  # Valida que el objeto herede de Servicio
            raise ErrorReserva("La reserva requiere un objeto Servicio válido.")  # Lanza error si no lo es
        if not servicio.disponible:  # Verifica disponibilidad antes de crear la reserva
            raise ServicioNoDisponibleError(
                f"El servicio '{servicio.nombre}' ({servicio.codigo}) no está disponible actualmente."
            )  # Lanza excepción de indisponibilidad

        try:  # Intenta validar parámetros y calcular el costo inicial encadenando errores si ocurren
            servicio.validar_parametros(duracion)  # Valida la duración según el tipo de servicio
            costo_total = servicio.calcular_costo(duracion, descuento_pct=descuento_pct, impuesto_pct=impuesto_pct)  # Calcula costo
        except Exception as exc:  # Captura fallos de validación o cálculo
            raise ErrorReserva(f"No se pudo calcular o validar la reserva '{id_reserva}'.") from exc  # Encadena excepción

        self.id_reserva = id_reserva.strip().upper()  # Guarda ID normalizado
        self.cliente = cliente  # Asocia el cliente
        self.servicio = servicio  # Asocia el servicio
        self.duracion = duracion  # Guarda la duración solicitada
        self.descuento_pct = descuento_pct  # Guarda porcentaje de descuento
        self.impuesto_pct = impuesto_pct  # Guarda porcentaje de impuesto
        self.costo_total = costo_total  # Guarda el costo calculado
        self.estado = "PENDIENTE"  # Estado inicial por defecto

    def confirmar(self, logger: GestorLogs) -> None:
        """Confirma una reserva pendiente y registra el evento en el log."""
        try:  # Valida transición de estado
            if self.estado == "CANCELADA":  # No permite confirmar una reserva cancelada
                raise ErrorReserva(f"La reserva {self.id_reserva} está cancelada y no puede confirmarse.")  # Error de estado
            if self.estado == "CONFIRMADA":  # Evita confirmar dos veces sin control
                raise ErrorReserva(f"La reserva {self.id_reserva} ya se encuentra confirmada.")  # Error duplicado
            self.estado = "CONFIRMADA"  # Actualiza estado a confirmada
        except ErrorReserva as exc:  # Registra el error controlado
            logger.registrar("ERROR", f"Fallo al confirmar reserva {self.id_reserva}", str(exc))  # Escribe en log
            raise  # Relanza para que el llamador decida cómo continuar
        else:  # Se ejecuta solo si no hubo excepción
            logger.registrar(
                "INFO",
                f"Reserva {self.id_reserva} confirmada para {self.cliente.nombre} en {self.servicio.nombre} (${self.costo_total:.2f}).",
            )  # Registra éxito
        finally:  # Se ejecuta siempre al cerrar el bloque
            logger.registrar("INFO", f"Verificación de confirmación finalizada para reserva {self.id_reserva}.")  # Traza final

    def cancelar(self, motivo: str, logger: GestorLogs) -> None:
        """Cancela una reserva activa si el motivo es válido y registra el resultado."""
        try:  # Valida motivo y estado
            if not isinstance(motivo, str) or not motivo.strip():  # Exige un motivo no vacío
                raise ErrorReserva("Debe indicar un motivo válido para cancelar la reserva.")  # Error si falta motivo
            if self.estado == "CANCELADA":  # Evita cancelar dos veces
                raise ErrorReserva(f"La reserva {self.id_reserva} ya fue cancelada previamente.")  # Error de estado
            self.estado = "CANCELADA"  # Cambia estado a cancelada
        except ErrorReserva as exc:  # Registra error controlado
            logger.registrar("ERROR", f"Fallo al cancelar reserva {self.id_reserva}", str(exc))  # Escribe en log
            raise  # Relanza excepción
        else:  # Si no hubo error, registra cancelación
            logger.registrar("WARNING", f"Reserva {self.id_reserva} cancelada. Motivo: {motivo.strip()}.")  # Registra aviso
        finally:  # Limpieza/auditoría final del método
            logger.registrar("INFO", f"Proceso de cancelación evaluado para reserva {self.id_reserva}.")  # Traza final

    def procesar(self, logger: GestorLogs) -> str:
        """Procesa la reserva confirmada recalculando su costo y devolviendo un comprobante."""
        try:  # Intenta procesar la reserva
            if self.estado != "CONFIRMADA":  # Solo procesa reservas confirmadas
                raise ErrorReserva(
                    f"La reserva {self.id_reserva} debe estar CONFIRMADA para procesarse (estado actual: {self.estado})."
                )  # Error si no está confirmada
            costo_verificado = self.servicio.calcular_costo(
                self.duracion,
                descuento_pct=self.descuento_pct,
                impuesto_pct=self.impuesto_pct,
            )  # Recalcula costo para asegurar consistencia
            if costo_verificado != self.costo_total:  # Detecta discrepancias de cálculo
                raise ErrorCalculoCosto("Inconsistencia detectada al verificar el costo de la reserva.")  # Error de cálculo
        except (ErrorReserva, ErrorCalculoCosto) as exc:  # Captura errores de reserva o cálculo
            logger.registrar("ERROR", f"Error al procesar reserva {self.id_reserva}", str(exc))  # Registra en log
            raise  # Relanza excepción
        else:  # Ejecuta si todo fue válido
            comprobante = (
                f"Comprobante {self.id_reserva} | Cliente: {self.cliente.nombre} | "
                f"Servicio: {self.servicio.nombre} | Total: ${costo_verificado:.2f} | Estado: {self.estado}"
            )  # Arma comprobante
            logger.registrar("INFO", f"Procesada correctamente -> {comprobante}")  # Registra en log
            return comprobante  # Retorna comprobante
        finally:  # Registra cierre del procesamiento
            logger.registrar("INFO", f"Fin del intento de procesamiento para reserva {self.id_reserva}.")  # Traza final
