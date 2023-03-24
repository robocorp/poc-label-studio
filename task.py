import logging
from typing import Dict
import contextlib
import time
import threading
import uvicorn

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from RPA.Browser.Selenium import Selenium
import RPA.Assistant
from RPA.Assistant.types import Size

browser_lib = Selenium()
app = FastAPI()
assistant = RPA.Assistant.Assistant()
results = {}
outcome = None

class Server(uvicorn.Server):
    def install_signal_handlers(self):
        pass

    @contextlib.contextmanager
    def run_in_thread(self):
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()

@app.post("/annotate", response_model=None)
def annotate_handler(post_data: Dict) -> None:
    global outcome
    print(post_data)
    outcome = post_data

@app.get("/annotations", response_model=None)
def get_annotations():
    d = {
        "url": results["url"],
        "tag1": results["tag1"],
        "tag2": results["tag2"],
    }
    print(d)
    return d


def show_main_ui():
    global results
    assistant.add_text_input(
        "url",
        placeholder="URL to an image",
        label="URL"
    )
    assistant.add_text_input(
        "tag1",
        placeholder="First tag",
        label="Tag 1"
    )
    assistant.add_text_input(
        "tag2",
        placeholder="Second tag",
        label="Tag 2"
    )
    results = assistant.ask_user(timeout=500)

def show_second_ui():
    assistant.add_text("Done?")
    assistant.ask_user(timeout=500)

def show_final_ui():
    assistant.add_text("Here is what you tagged:", size=Size.Large)
    assistant.add_text(str(outcome))
    assistant.add_image(results["url"])
    assistant.ask_user(timeout=500)

if __name__ == "__main__":
    port = 8000

    app.mount("/", StaticFiles(directory="./", html = True), name="static")
    print(f"Serving at port {port}")

    config = uvicorn.Config(app, host="127.0.0.1", port=port, log_level="info")
    server = Server(config=config)

    with server.run_in_thread():
        show_main_ui()
        browser_lib.open_available_browser(f"http://localhost:{port}")
        show_second_ui()
        show_final_ui()
        