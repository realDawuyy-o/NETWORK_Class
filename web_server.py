import socket
import threading


HOST = "127.0.0.1"
PORT = 8000


def handle_client(client_socket, client_address):
    """Handle one client request."""
    try:
        request = client_socket.recv(4096).decode("utf-8", errors="replace")
        print(f"Request from {client_address}:\n{request}")

        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html; charset=utf-8\r\n"
            "Content-Length: 26\r\n"
            "\r\n"
            "<h1>Hello from Python!</h1>"
        )
        client_socket.sendall(response.encode("utf-8"))
    finally:
        client_socket.close()


def start_server(host=HOST, port=PORT):
    """Start the basic HTTP server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"Server listening on http://{host}:{port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, client_address),
                daemon=True,
            )
            client_thread.start()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()
