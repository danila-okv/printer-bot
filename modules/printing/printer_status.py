import subprocess
from analytics.logger import log

def get_printer_status() -> str:
    try:
        result = subprocess.run(["lpstat", "-p"], capture_output=True, text=True)
        output = result.stdout.strip().lower()
        print(f"[DEBUG] Статус принтера: {result}")

        if "disabled" in output or not ping_printer():
            return "❌ Принтер отключён"
        elif "idle" in output:
            return "🟢 Принтер готов к печати"
        elif "printing" in output:
            return "🟡 Принтер сейчас печатает"
        else:
            return "⚠️ Состояние принтера не определено"
    except Exception as e:
        return f"❌ Ошибка при проверке принтера: {e}"


def ping_printer(ip: str = "192.168.31.87", count: int = 1, timeout: int = 500) -> bool:
    try:
        result = subprocess.run(
            ["ping", "-c", str(count), "-W", str(timeout), ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
    except Exception:
        return False
