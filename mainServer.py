from Server import Server
import sys


def main():
    if len(sys.argv) != 2:
        print("Argument should be the port number to listen")
        exit()

    hostAddress = '127.0.0.1'
    port = int(sys.argv[1])
    server = Server(host=hostAddress, port=port, isOnline=True)
    server.initializeServer()
    server.waitForClients()


if __name__ == "__main__":
    main()
