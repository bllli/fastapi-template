import asyncio
import logging
import threading
import time
import uvicorn
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def start_app():
    uvicorn.run("app:create_app", host="127.0.0.1", port=11459)


# 轮询
def poll_app():
    while True:
        time.sleep(1)
        try:
            resp = requests.get("http://127.0.0.1:11459/")
            assert resp.status_code == 200
        except Exception as e:
            logger.error(e)



def main():
    app_thread = threading.Thread(target=start_app)
    app_thread.start()
    
    poll_thread = threading.Thread(target=poll_app)
    poll_thread.start()

    app_thread.join()
    poll_thread.join()


if __name__ == "__main__":
    asyncio.run(main())
