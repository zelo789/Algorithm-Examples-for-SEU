"""运行本地网页动画演示。

用法：
python visualize.py
python visualize.py --port 8765
python visualize.py --dump-json
"""

from __future__ import annotations

import argparse
import json
import webbrowser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from algorithms.visualization import build_visualizer_algorithm, build_visualizer_payload

ROOT_DIR = Path(__file__).resolve().parent
VISUALIZER_DIR = ROOT_DIR / "visualizer"


class VisualizerHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, directory=str(VISUALIZER_DIR), **kwargs)

    def _write_json(self, status: int, payload: object, send_body: bool) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if send_body:
            self.wfile.write(body)

    def _serve_api(self, send_body: bool) -> bool:
        parsed = urlparse(self.path)
        if parsed.path == "/api/data":
            self._write_json(200, build_visualizer_payload(), send_body)
            return True

        if parsed.path == "/api/algorithm":
            params = {key: values[-1] for key, values in parse_qs(parsed.query).items() if values}
            algorithm_id = params.pop("algorithm", "")
            try:
                payload = build_visualizer_algorithm(algorithm_id, params)
            except ValueError as exc:
                self._write_json(400, {"error": str(exc)}, send_body)
                return True
            self._write_json(200, payload, send_body)
            return True

        return False

    def do_GET(self) -> None:
        if self._serve_api(send_body=True):
            return

        parsed = urlparse(self.path)
        if parsed.path == "/":
            self.path = "/index.html"
        else:
            self.path = parsed.path
        super().do_GET()

    def do_HEAD(self) -> None:
        if self._serve_api(send_body=False):
            return

        parsed = urlparse(self.path)
        if parsed.path == "/":
            self.path = "/index.html"
        else:
            self.path = parsed.path
        super().do_HEAD()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="打开算法可视化演示页面")
    parser.add_argument("--port", type=int, default=8000, help="本地服务端口")
    parser.add_argument("--no-browser", action="store_true", help="只启动服务，不自动打开浏览器")
    parser.add_argument("--dump-json", action="store_true", help="打印前端使用的 JSON 数据后退出")
    args = parser.parse_args(argv)

    if args.dump_json:
        print(json.dumps(build_visualizer_payload(), ensure_ascii=False, indent=2))
        return

    handler = partial(VisualizerHandler)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    url = f"http://127.0.0.1:{args.port}"

    if not args.no_browser:
        webbrowser.open(url)

    print(f"Visualizer running at {url}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nVisualizer stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
