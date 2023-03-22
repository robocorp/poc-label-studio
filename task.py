import os
import subprocess
from typing import Tuple
import webview
# from RPA.Assistant import Assistant
# from RPA.Assistant.types import Size

# assistant = Assistant()

def evaluate_js(username, password):
    # TODO: check why this isn't working
    def inner(window):
        window.evaluate_js(
        rf"""
        document.getElementById("email").value = {username}
        document.getElementById("password").value = {password}
        """
    )
    
    return inner


def start_webview(username, password):
    import time
    time.sleep(7)
    webview.create_window("Label Studio", "http://localhost:8080/")
    webview.start(debug=True)

def ask_credentials() -> Tuple[str]:
    # assistant.add_text("Create user", Size.Large)
    # assistant.add_text_input("username", placeholder="username", label="Username")
    # assistant.add_password_input("password", label="Password")
    # results = assistant.ask_user()
    # return results["username"], results["password"]
    return "username", "password"

if __name__ == "__main__":
    username, password = ask_credentials()
    os.environ["LABEL_STUDIO_DISABLE_SIGNUP_WITHOUT_LINK"] = "true"
    os.environ["LABEL_STUDIO_USERNAME"] = username
    os.environ["LABEL_STUDIO_PASSWORD"] = password
    proc = subprocess.Popen(["label-studio", "-b"])
    start_webview(username, password)
    proc.terminate()