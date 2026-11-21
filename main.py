from entidades import Cliente  # Clase Cliente con encapsulación y validaciones
from excepciones import (  # Excepciones personalizadas del sistema
    ErrorCalculoCosto,
    ErrorParametroServicio,
    ErrorReserva,
    ErrorSistemaSoftwareFJ,
    ErrorValidacionCliente,
    ServicioNoDisponibleError,
)
from gestor_logs import GestorLogs  # Gestor de registro en archivo .log
from reservas import Reserva  # Clase Reserva
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala  # Tres servicios especializados


def ejecutar_simulacion() -> None:
    """Ejecuta 10 operaciones secuenciales sobre listas en memoria y registra eventos/errores en log."""
    logger = GestorLogs("logs_software_fj.log")  # Inicializa archivo de logs en texto plano
    clientes: list[Cliente] = []  # Lista interna en memoria para clientes válidos
    servicios = []  # Lista interna en memoria para servicios válidos
    reservas: list[Reserva] = []  # Lista interna en memoria para reservas válidas

    logger.registrar("INFO", "Inicio de simulación Software FJ (10 operaciones secuenciales).")  # Marca inicio

    # Operación 1 (Válida): Registro correcto de un cliente
    try:  # Intenta crear cliente válido
        c1 = Cliente("CLI-01", "Valeria Rojas", "valeria.rojas@correo.com", "3104567890")  # Crea instancia Cliente
    except ErrorValidacionCliente as exc:  # Captura error de validación
        logger.registrar("ERROR", "Operación 1 fallida al registrar cliente CLI-01", str(exc))  # Registra error
    else:  # Ejecuta si el registro fue exitoso
        clientes.append(c1)  # Agrega cliente a la lista interna
        logger.registrar("INFO", f"Operación 1 exitosa: {c1.resumen()}")  # Registra éxito

    # Operación 2 (Inválida): Registro de cliente con correo y teléfono inválidos
    try:  # Intenta crear cliente con datos erróneos
        c_invalido = Cliente("CLI-02", "Lu", "correo-sin-arroba", "123")  # Dispara ErrorValidacionCliente
    except ErrorValidacionCliente as exc:  # Captura excepción esperada
        logger.registrar("ERROR", "Operación 2 controlada: registro de cliente inválido rechazado", str(exc))  # Registra error
    else:  # No debería ejecutarse en este caso
        clientes.append(c_invalido)  # Si pasara, lo añadiría

    # Operación 3 (Válida): Creación de los 3 servicios especializados (sala, equipo y asesoría)
    try:  # Crea servicios válidos
        s_sala = ReservaSala("SALA-1", "Sala Ejecutiva Norte", 50.0, capacidad_personas=12, disponible=True)  # Reserva de sala
        s_equipo = AlquilerEquipo("EQ-1", "Laptop Desarrollador i7", 25.0, tipo_equipo="Portátil", disponible=True)  # Alquiler de equipo
        s_asesoria = AsesoriaEspecializada(
            "ASE-1", "Arquitectura de Software", 80.0, especialidad="Backend y POO", disponible=True
        )  # Asesoría especializada
    except ErrorParametroServicio as exc:  # Captura error en parámetros de servicio
        logger.registrar("ERROR", "Operación 3 fallida al crear servicios base", str(exc))  # Registra error
    else:  # Guarda servicios creados
        servicios.extend([s_sala, s_equipo, s_asesoria])  # Añade los tres servicios a la lista
        for srv in servicios:  # Recorre cada servicio para describirlo
            logger.registrar("INFO", f"Operación 3 exitosa - Servicio registrado: {srv.describir()}")  # Registra servicio

    # Operación 4 (Inválida): Creación de servicio con tarifa negativa y duración fuera de rango
    try:  # Intenta crear servicio con tarifa inválida
        s_error = ReservaSala("SALA-BAD", "Sala Auditorio", -20.0, capacidad_personas=30)  # Lanza ErrorParametroServicio
    except ErrorParametroServicio as exc:  # Captura excepción de parámetro
        logger.registrar("ERROR", "Operación 4 controlada: creación de servicio inválida", str(exc))  # Registra error
    else:  # Si no falló, agrega a la lista
        servicios.append(s_error)  # Añade servicio

    # Operación 5 (Válida): Reserva exitosa de sala con descuento e impuesto opcionales (sobrecarga de costo)
    try:  # Crea y confirma reserva de sala
        r1 = Reserva(
            "RES-01",
            clientes[0],
            servicios[0],
            duracion=4,
            descuento_pct=10.0,
            impuesto_pct=19.0,
        )  # Calcula costo con descuento e impuesto
        r1.confirmar(logger)  # Confirma la reserva
    except ErrorSistemaSoftwareFJ as exc:  # Captura errores del sistema
        logger.registrar("ERROR", "Operación 5 fallida en reserva de sala", str(exc))  # Registra error
    else:  # Guarda reserva confirmada
        reservas.append(r1)  # Agrega a lista de reservas
        logger.registrar("INFO", f"Operación 5 exitosa: Reserva {r1.id_reserva} por ${r1.costo_total:.2f}")  # Registra éxito

    # Operación 6 (Inválida): Intento de reserva sobre un servicio NO disponible
    try:  # Crea servicio no disponible y trata de reservarlo
        s_no_disp = AlquilerEquipo("EQ-99", "Proyector 4K", 40.0, tipo_equipo="Video", disponible=False)  # No disponible
        r_fallida_disp = Reserva("RES-02", clientes[0], s_no_disp, duracion=2)  # Dispara ServicioNoDisponibleError
    except ServicioNoDisponibleError as exc:  # Captura excepción de indisponibilidad
        logger.registrar("ERROR", "Operación 6 controlada: reserva de servicio no disponible", str(exc))  # Registra error
    else:  # Si se creara, la guardaría
        reservas.append(r_fallida_disp)  # Añade reserva

    # Operación 7 (Inválida): Reserva con duración inválida encadenando excepción original (from)
    try:  # Intenta reservar sala por 25 horas (máximo permitido: 12)
        r_duracion_mala = Reserva("RES-03", clientes[0], servicios[0], duracion=25)  # Lanza ErrorReserva encadenado
    except ErrorReserva as exc:  # Captura ErrorReserva
        causa = str(exc.__cause__) if exc.__cause__ else "Sin causa encadenada"  # Obtiene causa raíz encadenada
        logger.registrar(
            "ERROR",
            "Operación 7 controlada: duración inválida en reserva",
            f"{exc} | Causa raíz: {causa}",
        )  # Registra error y causa encadenada

    # Operación 8 (Válida): Reserva de asesoría especializada y procesamiento de comprobante
    try:  # Crea, confirma y procesa reserva de asesoría
        r2 = Reserva("RES-04", clientes[0], servicios[2], duracion=3, descuento_pct=5.0, impuesto_pct=0.0)  # Crea reserva
        r2.confirmar(logger)  # Confirma reserva
        comprobante = r2.procesar(logger)  # Procesa y genera comprobante
    except ErrorSistemaSoftwareFJ as exc:  # Captura cualquier error del dominio
        logger.registrar("ERROR", "Operación 8 fallida al procesar asesoría", str(exc))  # Registra error
    else:  # Guarda y reporta comprobante
        reservas.append(r2)  # Añade reserva procesada
        logger.registrar("INFO", f"Operación 8 exitosa: {comprobante}")  # Registra comprobante

    # Operación 9 (Inválida): Intentar procesar una reserva que fue cancelada
    try:  # Crea reserva de alquiler de equipo, la cancela y luego intenta procesarla
        r3 = Reserva("RES-05", clientes[0], servicios[1], duracion=5)  # Crea reserva pendiente
        r3.cancelar("Cambio de cronograma del cliente", logger)  # Cancela la reserva
        r3.procesar(logger)  # Intenta procesar una reserva cancelada -> lanza ErrorReserva
    except ErrorReserva as exc:  # Captura error de estado inválido
        logger.registrar("ERROR", "Operación 9 controlada: no se puede procesar reserva cancelada", str(exc))  # Registra error

    # Operación 10 (Inválida/Controlada): Porcentaje de descuento inválido al calcular costo
    try:  # Intenta calcular costo con descuento fuera de rango (150%)
        _ = servicios[1].calcular_costo(duracion=2, descuento_pct=150.0)  # Dispara ErrorCalculoCosto
    except ErrorCalculoCosto as exc:  # Captura error de cálculo
        logger.registrar("ERROR", "Operación 10 controlada: error en cálculo de costo", str(exc))  # Registra error

    finally:  # Bloque final de cierre del flujo completo
        logger.registrar(
            "INFO",
            f"Simulación completada. Clientes: {len(clientes)} | Servicios: {len(servicios)} | Reservas exitosas: {len(reservas)}",
        )  # Resumen final en log
        print("Simulación finalizada. Revisa la consola y el archivo 'logs_software_fj.log'.")  # Mensaje final en pantalla


if __name__ == "__main__":  # Ejecuta la simulación solo cuando main.py es el script principal
    ejecutar_simulacion()  # Llama a la función de las 10 operaciones secuenciales
