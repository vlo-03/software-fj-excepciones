from datetime import datetime  # Importa datetime para registrar fecha y hora exacta de cada evento
from pathlib import Path  # Importa Path para manejar rutas de archivos de forma segura


class GestorLogs:
    """Gestiona el registro de eventos y errores en un archivo de texto plano (.log)."""

    def __init__(self, nombre_archivo: str = "logs_software_fj.log") -> None:
        self.ruta_log = Path(nombre_archivo)  # Define la ruta del archivo de registro

    def registrar(self, nivel: str, mensaje: str, detalle_error: str = "") -> None:
        """Escribe una línea con marca de tiempo, nivel y mensaje en el archivo de log."""
        marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Obtiene fecha y hora actual
        nivel_limpio = nivel.strip().upper()  # Normaliza el nivel (INFO, WARNING, ERROR, etc.)
        linea = f"[{marca_tiempo}] [{nivel_limpio}] {mensaje.strip()}"  # Construye la línea base del log
        if detalle_error:  # Si hay detalle de excepción o encadenamiento, lo agrega
            linea += f" | Detalle: {detalle_error.strip()}"  # Concatena el detalle técnico
        linea += "\n"  # Añade salto de línea para el siguiente registro

        try:  # Intenta abrir y escribir en el archivo de logs
            with self.ruta_log.open("a", encoding="utf-8") as archivo:  # Abre en modo anexar (append)
                archivo.write(linea)  # Escribe la línea en el archivo de log
        except OSError as exc:  # Captura fallos de escritura en disco sin detener el programa
            print(f"[AVISO DE LOG] No se pudo escribir en {self.ruta_log}: {exc}")  # Informa por consola
