import usb.core
import usb.util
import subprocess
import time

idVendor = 0xAA88
idProduct = 0x8666
repetitions = 3
interval = 0.1


def find_out_endpoint(dev):
    for cfg in dev:
        for intf in cfg:
            ep = next((ep for ep in intf if usb.util.endpoint_direction(
                ep.bEndpointAddress) == usb.util.ENDPOINT_OUT), None)
            if ep:
                return ep.bEndpointAddress
    raise ValueError('Output endpoint not found')


dev = usb.core.find(idVendor=idVendor, idProduct=idProduct)

if dev is None:
    raise ValueError('Device not found')

if dev.is_kernel_driver_active(0):
    try:
        dev.detach_kernel_driver(0)
    except usb.core.USBError as e:
        print(f"Error detaching kernel driver: {e}")
        exit()

try:
    dev.set_configuration()
except usb.core.USBError as e:
    print(f"Error setting configuration: {e}")
    exit()

endpoint = find_out_endpoint(dev)


def get_cpu_temperature():
    try:
        result = subprocess.run(['sensors'], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        for line in output.split('\n'):
            if 'Core 0' in line:
                temp_str = line.split()[2]
                temp_celsius = float(temp_str.strip('+°C'))
                return temp_celsius
    except Exception as e:
        print(f"Error retrieving temperature: {e}")
        return None


def format_temperature_data(temperature):
    temp_hex = f'{int(temperature):02x}'
    if temperature < 16:
        prefix = f'{temp_hex}0c000014000000'
    else:
        prefix = f'{temp_hex}1c000014000000'
    data = bytearray.fromhex(prefix)
    return data


def send_data_repeatedly(data):
    for _ in range(repetitions):
        try:
            dev.write(endpoint, data)
            time.sleep(interval)
        except usb.core.USBError as e:
            print(f"Error sending data: {e}")


while True:
    temperature = get_cpu_temperature()
    if temperature is not None:
        data = format_temperature_data(temperature)
        send_data_repeatedly(data)
    time.sleep(2)
