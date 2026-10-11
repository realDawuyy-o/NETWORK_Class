import socket


class FTPClient:
    def __init__(self, host, port=21, timeout=5):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.control_socket = None

    def connect(self):
        """Create a TCP connection to the FTP server."""
        self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.control_socket.settimeout(self.timeout)
        self.control_socket.connect((self.host, self.port))
        print(self.recv_response())

    def recv_response(self):
        """Read a line from the FTP server."""
        if self.control_socket is None:
            return ""

        data = self.control_socket.recv(4096)
        return data.decode("utf-8", errors="replace")

    def login(self, username="anonymous", password=""):
        """Send username and password to the FTP server."""
        self.send_command(f"USER {username}")
        self.send_command(f"PASS {password}")

    def send_command(self, command):
        """Send a command to the FTP server."""
        if self.control_socket is None:
            raise ConnectionError("Not connected to FTP server")

        self.control_socket.sendall((command + "\r\n").encode("utf-8"))
        print(self.recv_response())

    def list_files(self):
        """List files in the current directory."""
        self.send_command("LIST")

    def download_file(self, remote_path, local_path):
        """Download a file from the server."""
        # TODO: implement passive mode + file transfer logic
        print(f"Downloading {remote_path} to {local_path}")

    def upload_file(self, local_path, remote_path):
        """Upload a file to the server."""
        # TODO: implement file transfer logic
        print(f"Uploading {local_path} to {remote_path}")

    def close(self):
        """Close the FTP connection."""
        if self.control_socket:
            self.control_socket.close()
            self.control_socket = None


if __name__ == "__main__":
    ftp_client = FTPClient("127.0.0.1", port=21)
    try:
        ftp_client.connect()
        ftp_client.login("user", "pass")
        ftp_client.list_files()
    finally:
        ftp_client.close()
