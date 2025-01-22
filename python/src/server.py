import socket
from socketserver import BaseRequestHandler, TCPServer
from threading import Thread

from handler import process_request
from utils import RESPSerializer, RESPParser


class RedisLiteHandler(BaseRequestHandler):
    def handle(self):
        while True:
            try:
                request = self.request.recv(512)
                if not request:
                    print("Empty request received, closing connection.")
                    return

                print(f"Received request from {self.client_address}")

                response = process_request(request)
                self.request.sendall(response)

            except Exception as e:
                print(f"Error handling request: {e}")
                error_response = RESPSerializer(e).serialize(error=True)
                self.request.sendall(error_response)
        self.request.close()


def start_redis_workers(n_workers=2):
    TCPServer.allow_reuse_address = True
    with TCPServer(("", 6379), RedisLiteHandler) as serv:
        serv.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        for n in range(n_workers):
            t = Thread(target=serv.serve_forever)
            t.daemon = True
            t.start()

        print("Redis Server started on port 5379...")
        serv.serve_forever()


if __name__ == "__main__":
    try:
        start_redis_workers()
    except KeyboardInterrupt:
        print("stopping server...")
        import sys

        sys.exit(0)
