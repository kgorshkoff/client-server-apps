import yaml
import getpass
import datetime
import actions
from socket import socket
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument(
    '-c', '--config', type=str,
    required=False, help='sets config file path'
)
parser.add_argument(
    '-host', '--host', type=str,
    required=False, help='set server IP'
)
parser.add_argument(
    '-p', '--port', type=str,
    required=False, help='set server port'
)
args = parser.parse_args()

default_config = {
    'host': 'localhost',
    'port': 8000,
    'buffersize': 1024
}

if args.config:
    with open(args.config) as file:
        file_config = yaml.load(file, Loader=yaml.Loader)
        default_config.update(file_config)


def execute(command):
        sock.send(command.encode())
        b_response = sock.recv(default_config.get('buffersize'))
        print(b_response.decode())


host, port = default_config.get('host'), default_config.get('port')

try:
    account = input('Enter your name:')
    # message = to_address = ''
    # encoding = 'ascii'
    # groups = []
    # password = getpass.getpass('Enter your password: ')
    sock = socket()
    sock.connect((host, port))
    execute(actions.presence(account))

    # while True:
    #     execute(actions.presence('testtest'))
    #     sleep(2)
    #     for i in groups:
    #         print(i, end=', ')
    #     print('')

    #     menu = {}
    #     menu['1'] = "Send message" 
    #     menu['2'] = "Join room"
    #     menu['3'] = "Leave room"
    #     menu['4'] = "Quit"
    #     options = menu.keys()
    #     for entry in options: 
    #         print(entry, menu[entry])

    #     selection = input("\nPlease select:") 
    #     if selection == '1':
    #         while True:
    #             menu = {}
    #             menu['1'] = "Message" 
    #             menu['2'] = "Select reciever"
    #             menu['3'] = "Encoding"
    #             menu['4'] = "Send message"
    #             menu['5'] = "Quit"
    #             options = menu.keys()
    #             for entry in options: 
    #                 print(entry, menu[entry])

    #             selection = input("\nPlease select:")
    #             if selection == '1':
    #                 message = input('Input message: ')
    #             elif selection == '2':
    #                 to_address = input('Input reciever: ')
    #             elif selection == '3':
    #                 encoding = input('Input encoding: ')
    #             elif selection == '4':
    #                 if message == '' or to_address == '':
    #                     print('Select reciever and write the message')
    #                 else:
    #                     option = actions.msg(account, to_address, message, encoding)
    #                     execute(option)
    #                     msg = ''
    #             elif selection == '5':
    #                 break
    #             else:
    #                 print('Unknown option selected!')

    #     elif selection == '2':
    #         room = input('Select room (with #prefix): ')
    #         option = actions.join(account, room)
    #         groups.append(room)
    #     elif selection == '3':
    #         room = input('Select room (with #prefix): ')
    #         option = actions.leave(account, room)
    #         groups.remove(room)
    #     elif selection == '4':             
    #         option = actions.quit()
    #     else: 
    #         print("Unknown option selected!")

    #     execute(option)

except KeyboardInterrupt:
    print('Client shutting down')
