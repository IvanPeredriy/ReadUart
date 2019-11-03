import sys
import glob
import serial


def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


if __name__ == '__main__':
    print(serial_ports())
    print("Choose COMx")
    ser = serial.Serial()
    ser.port = input()
    print(ser.port + ' choosed')
    print("Choose baudrate")
    ser.baudrate = int(input())      # 115200
    print(str(ser.baudrate) + ' choosed')
    numerator = 0
    name_of_file = 'file.txt'
    file = open(name_of_file, 'w')
    ser.open()
    for x in range(10000000):
        buf = str(ser.readlines(10))
        if buf.find('done') > 0:
            print(str(numerator) + ' iteration done!')
            file.close()
            numerator = numerator + 1
            name_of_file = str(numerator) + '_file.txt'
            file = open(name_of_file, 'w')
            buf = str(ser.readlines(10))
        file.write((buf[buf.find('\'') + 1:buf.find('\\')]) + '\n')
    ser.close()
    file.close()
