from car_message.raspberry.connector import connector
from car_message.raspberry.wrappers import handle_exception


@handle_exception
def app():
    while True:
        command = connector.receive_command()
        if command:
            print(command)


app()
