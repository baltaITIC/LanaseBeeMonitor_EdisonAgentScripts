__docformat__ = 'restructuredtext en'
__author__ = 'CSIRO'
__version__ = 'e1.0'


# List of of libraries being used in this script
import usb.core
import usb.util
import usb.backend.libusb1
import sys
import os
import time
import subprocess
import psycopg2
sys.path.append('ScriptsFuncionales/')

import mosquitto_publisher

#-------To get agent id from data base
conn_string = "host='localhost' dbname='iot-sensors' user='postgres' password='postgres'"
conn = psycopg2.connect(conn_string)
#cur = conn.cursor()
cur = conn.cursor()
ID_Agent="0"
ID_rfid="0"
try:
    #Execute SQL query using execute() method
    cur.execute('select pk_id_agent from agent order by pk_id_agent DESC LIMIT 1')
    ID_Agent = str(cur.fetchone())
    ID_Agent = ID_Agent[1:(len(ID_Agent)-2)]

    cur.execute('select pk_id_sensor_rfid from sensor_rfid order by pk_id_sensor_rfid DESC LIMIT 1')
    ID_rfid = str(cur.fetchone())
    #Split string to obtain just characters
    ID_rfid = ID_rfid[1:(len(ID_rfid)-2)]
    print (ID_Agent,ID_rfid)
    #Fetch a single row using fetchone() method and store the result in avariable
    conn.commit()
except psycopg2.Error as error:
    print("Error: {}".format(error))
cur.close()
conn.close()
#---------------

# Adjust the MACHINE_ID with the id of the mini computer being used
# The machine id being used will reflect on the log file name
COMPUTER_TYPE = 'Edison'
factory_sn_file = log_file = open('/factory/serial_number', 'r')
COMPUTER_SN = ''.join([COMPUTER_TYPE, '-', factory_sn_file.read(16)]) 
factory_sn_file.close()


MACHINE_ID = 'H01'
MACHINE_ID = COMPUTER_SN


# Adjust the LOG_FILE_LOCATION with the location of the log file being stored
# The default location is /home/csiro
LOG_FILE_LOCATION = '/home/root/.cache/obexd/'

# Adjust the SLEEPING_INTERVAL with the preferred sleeping interval (in second)
SLEEPING_INTERVAL = 0.5

# Following are all the hardware parameters to communicate with the RFID reader (MTI RU-824)
VENDOR_ID = 0x24e9
PRODUCT_ID = 0x0824
HEADER = bytearray([0x43, 0x49, 0x54, 0x4D, 0xFF])
CMD_PWR240_CYC20 = bytearray([18, 0, 240, 0, 0, 0, 20, 0, 0, 87, 36])
CMD_PWR240_CYC30 = bytearray([18, 0, 240, 0, 0, 0, 30, 0, 0, 150, 227])
CMD_DYNAMIC_Q = bytearray([50, 1, 0, 0, 0, 0, 0, 0, 0, 67, 116])
CMD_NON_CONT = bytearray([2, 1, 0, 0, 0, 0, 0, 0, 0, 65, 128])
CMD_ENABLE_FASTID = bytearray([6, 3, 2, 34, 0, 0, 0, 0, 0, 163, 77])
CMD_INV = bytearray([64, 0, 0, 0, 0, 0, 0, 0, 0, 44, 94])

# backend = usb.backend.libusb1.get_backend(find_library=lambda x: "/lib/libusb-1.0.so.0")
RFID_READER = list(usb.core.find(find_all=True, idVendor=VENDOR_ID, idProduct=PRODUCT_ID))

# Declare two global variables with empty string as their initial value
active_date = ''
active_log_file_name = ''


def create_new_log_file():
    """
    Create a new empty log file for the current date.
    """
    # Global variable declaration to access global variable active_date
    # and global variable active_log_file_name
    global active_date
    global active_log_file_name

    # Get the current system date
    active_date = time.strftime('%Y.%m.%d')

    # Prepare the active log file name
    active_log_file_name = ''.join([LOG_FILE_LOCATION, active_date, '-', MACHINE_ID, '.csv'])

    # If the file name is not exist, create the new log file
    if not os.path.exists(active_log_file_name):
        log_file = open(active_log_file_name, 'w')
        log_file.write('# bee_detection_data v_1_1_3\n')
        log_file.close()


def write_log(reader_sn, epc_list, log_time):
    """
    Write the tags (bee ids) stored in epc_list variable into a currently active log file.
    :param epc_list: list of bee ids been read by the RFID reader
    :param log_time: reading time
    """
    # Global variable declaration to access global variable active_date
    # and global variable active_log_file_name
    global active_date
    global active_log_file_name

    # Create a new log file is the current system date is different
    # than the date stored in the global variable global active_date
    if active_date != time.strftime("%Y.%m.%d"):
        create_new_log_file()

    epc_log = ''
    epc_list = set(epc_list)
    conn_string = "host='localhost' dbname='iot-sensors' user='postgres' password='postgres'"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    for epc in epc_list:
        info_sendt = ''.join([log_time,' ',epc[:24],' ',ID_Agent])
        epc = ''.join([ epc[:24], ',', epc[24:] ])
        #epc_log = ''.join([epc_log, COMPUTER_SN, ',', reader_sn, ',', log_time, ',', epc, '\n'])
        epc_log = ''.join([epc_log, log_time, ' ', epc, ' ', reader_sn, ' ', COMPUTER_SN, '\n'])
        datetime = log_time
        datetime = datetime[0:4]+"-"+datetime[4:6]+"-"+datetime[6:8]+" "+datetime[9:11]+":"+datetime[11:13]+":"+datetime[13:15]
        
        mosquitto_publisher.publisher("rfid", info_sendt)        
        try:
            #Execute SQL query using execute() method          
            cur.execute("""INSERT INTO bee_control(control_date, fk_id_sensor_rfid, fk_id_bee) VALUES(%s,%s,%s)""",(datetime, ID_rfid, epc[:24]))
            conn.commit()
        except psycopg2.Error as error:
            print("Error: {}".format(error))
    cur.close()
    conn.close()
    # Open the currently active log file with append mode
    log_file = open(active_log_file_name, 'a')
    # Append the tags (bee ids) stored in variable epc_log into the active log file
    log_file.write(epc_log)
    # close the active log file
    log_file.close()

    # print('Log: {0}: {1}'.format(active_date, log_time))
    #print('Log: {0}'.format(log_time))
    print(epc_log)


def reformat_epc(epc_barr):
    """
    Reformat the epc data (bee ids) from string of decimal format to string of hexadecimal format
    :param epc_barr: string
    :rtype : string
    """
    # Convert the string of decimal data to list of decimal data
    epc_barr = list(epc_barr)

    # Initialize variable epc_hex with an empty string
    epc_hex = ''

    # Convert each member in list epc_bar to hexadecimal
    # and append it to variable epc_hex
    for epc in epc_barr:
        epc_hex += '{:02X}'.format(epc)

    # Return the value stored in variable epc_hex
    return epc_hex


def initialize_reader():
    """
    Initialize the communication with the RFID reader
    by sending a sequence of command parameters specific to the RFID reader being used (MTI RU-824)
    """
    if len(RFID_READER) <= 0:
        sys.exit('Could not find any RFID Reader.')

    print('Number of RFID Reader found: {0}'.format(len(RFID_READER)))

    for rfid_reader in RFID_READER:
        rfid_reader.set_configuration(configuration=None)
        rfid_reader.reset()
        rfid_reader.write(endpoint=0x01, data=HEADER + CMD_PWR240_CYC20, timeout=None)
        rfid_reader.write(endpoint=0x01, data=HEADER + CMD_DYNAMIC_Q, timeout=None)
        rfid_reader.write(endpoint=0x01, data=HEADER + CMD_NON_CONT, timeout=None)
        rfid_reader.write(endpoint=0x01, data=HEADER + CMD_ENABLE_FASTID, timeout=None)
        response = rfid_reader.read(0x82, 64, timeout=None)


def read_tags():
    """
    Send a set of instructions to RFID reader to start reading the tags (bee ids)
    """
    # Initialise an empty list for variable epc_list
    epc_list = list()

    for rfid_reader in RFID_READER:
        # Send a command to the RFID reader to read the tags (bee ids)
        rfid_reader.write(endpoint=0x01, data=HEADER + CMD_INV, timeout=None)
        # Receive the response from the RFID reader from the previous command
        response = rfid_reader.read(endpoint=0x82, size_or_buffer=64, timeout=None)

        while response[0] != 0x45:
            epc = response[28:52]

            if len(epc) != 0:
                epc_list.append( reformat_epc( epc ) )

            response = rfid_reader.read(endpoint=0x82, size_or_buffer=64, timeout=None)

        reader_sn = usb.util.get_string(rfid_reader, rfid_reader.iSerialNumber)

        # Write the tags (bee ids) stored in variable epc_list into the active log file
        write_log(reader_sn, epc_list, time.strftime('%Y%m%dT%H%M%SZ'))



def start_periodic_reading(sleeping_interval):
    """
    Start a periodic reading with a specific sleeping_interval
    :param sleeping_interval: Idle or sleeping interval (in second) before commencing the next reading cycle
    """
    # Define an infinite loop
    while True:
        # invoke function read_tags() to start reading the tags (bee ids)
        tickle_edison()
        read_tags()
         # Instruct the Python interpreter to sleep / idle for a certain interval
        time.sleep(sleeping_interval)


def tickle_edison():
    """
    Tickle the Edison
    """
    command = "systemd-notify WATCHDOG=1"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    # print(output)


def write_start_log_file():
    """
    Write the start event on start log file
    """
    start_log_file_name = ''.join([LOG_FILE_LOCATION, 'start_log-', MACHINE_ID, '.csv'])

    # Create a start log file if it is not existed
    if not os.path.exists(start_log_file_name):
        log_file = open(start_log_file_name, 'w')
        log_file.close()

    # Open the start log file with append mode
    log_file = open(start_log_file_name, 'a')

    # Append the start time log file
    log_file.write(time.strftime('%Y.%m.%d,%H:%M:%S') + '\n')
    
    # Close the log file
    log_file.close()


def main():
    """
    Main function
    """
    #Wait connection
    #time.sleep(30)
    create_new_log_file()
    write_start_log_file()
    initialize_reader()

    start_periodic_reading(SLEEPING_INTERVAL)
    

if __name__ == '__main__':
    main()
