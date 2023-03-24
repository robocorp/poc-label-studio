import http.server
import logging
import socketserver
from RPA.Browser.Selenium import Selenium

browser_lib = Selenium()

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/annotate":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length).decode("utf-8")
            print(post_data)
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write("Annotation received".encode("utf-8"))
        else:
            super().do_POST()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    port = 8000
    handler = Handler
    handler.extensions_map[".html"] = "text/html"

    httpd = socketserver.TCPServer(("", port), handler)

    logging.info(f"Serving at port {port}")
    browser_lib.open_available_browser(f"http://localhost:{port}")
    httpd.serve_forever()