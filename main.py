import logging
from concurrent.futures import ThreadPoolExecutor
from collections import deque
import datetime

from serial import Serial
from serial.tools.list_ports import comports

from youtube_controller import YouTubeController

logging.basicConfig(level="DEBUG", format="[%(asctime)s][%(funcName)s] %(message)s")
log = logging.getLogger()
pool = ThreadPoolExecutor(4)
controller = YouTubeController()

DEFAULT_PORT = "COM4"
PNN_THRESHOLD = 0.10

# logs = []

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

        listen_port(serial)

    except:
        log.error("Fucked!", exc_info=True)
        if serial:
            serial.close()

        controller.close()

        # with open("log.csv", mode="w") as f:
        #     f.writelines(logs)

def listen_port(serial):
    # global logs
    pnns = deque([0]*5, maxlen=5)
    prev_pnn = 0
    prev_rri = 0
    bpm_queue = deque(maxlen=30)
    rri_queue = deque(maxlen=30)

    log.info("Listening port...")
    for line in serial:
        # log.debug(f"Received: {line}")
        bpm, rri = line.decode().split(',')
        bpm_queue.append(float(bpm))
        rri_queue.append(float(rri) - prev_rri)
        prev_rri = float(rri)

        mean_bpm = sum(bpm_queue) / len(bpm_queue)
        pnn = len([i for i in rri_queue if abs(i) > 50]) / len(rri_queue)

        if (pnn - pnns[0]) < -PNN_THRESHOLD:
            log.info("displeasure detected! dispatching...")
            pool.submit(controller.skip)

        log.info(f"mean BPM: {mean_bpm:2.1f}, pNN50: {pnn:1.3f}, pnn diff:{pnn-pnns[0]:1.3f}")
        # logs.append(f"{datetime.datetime.now().isoformat()},{pnn}\n")
        pnns.append(pnn)

if __name__ == "__main__":
    main()
