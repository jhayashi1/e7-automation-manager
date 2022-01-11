import autoshop
import utils

from ppadb.client import Client as AdbClient

def main():
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()

    if len(devices) == 0:
        print('no device attached')
        quit()
    
    #Set device, resolution, and get screenshot of screen
    device = utils.get_device(devices)
    autoshop.parse_shop(device)


if __name__ == "__main__":
    main()