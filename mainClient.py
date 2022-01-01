from Client import Client
import sys

def main():
    if len(sys.argv) != 4:
        print("Arguments should be nickname, server's IP address and port number")
        exit()

    nickName = sys.argv[1]
    hostAddress = sys.argv[2]
    port = int(sys.argv[3])
    client = Client(nickName=nickName, host=hostAddress, port=port)
    client.initializeClient()
    client.handleServerConnection()


if __name__ == "__main__":
    main()
