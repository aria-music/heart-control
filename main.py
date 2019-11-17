import logging
from concurrent.futures import ThreadPoolExecutor

from serial import Serial
from serial.tools.list_ports import comports

from youtube_controller import YouTubeController

logging.basicConfig(level="DEBUG", format="[%(asctime)s][%(funcName)s] %(message)s")
log = logging.getLogger()
pool = ThreadPoolExecutor(4)
controller = YouTubeController()

DEFAULT_PORT = "COM4"


def main():
    serial = None
    try:
        log.info("Starting...")

        infos = comports()
        if not infos:
            log.info("No ports available.")
            return
        
        log.info("Available ports:")
        for info in infos:
            log.info(info.device)
            log.info(f"    name: {info.name}")
            log.info(f"    desc: {info.description}")
            log.info(f"    prod: {info.product}")

        port = input("*** Enter port (ex. COM4): ") or DEFAULT_PORT

        serial = Serial(port=port, baudrate=115200)
        serial.open()

        listen_port(serial)

    except:
        log.error("Fucked!", exc_info=True)
        if serial:
            serial.close()

def listen_port(serial):
    prev_pnn = 0
    for line in serial:
        log.debug(f"Received: {line}")
        # do fucks to detect pnn change
        pnn = 50
        if (pnn - prev_pnn) > 10:
            pool.submit(controller.skip)

if __name__ == "__main__":
    main()
