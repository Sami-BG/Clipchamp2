import os
import random
import string

import logging
import multiprocessing
import socket
from datetime import datetime, timedelta
from emoji import demojize

import AutoClipper.Constants as Const
from Twitch import TwitchAPI as Ttv

TIME_OUT_SEC = 10
ONLINE_ON_INTERVAL = 30


# TODO: This should be in another class GraphingSession. GraphingSession object exists in LoggingSession.
#  ClippingSession should be another class that takes graph and makes clips. Instance of that should also be contained
#  in LoggingSession

def post_process_file(log_file_name: str):
    pass


class LoggingSession(multiprocessing.Process):
    PORT = Const.port
    LENGTH_OF_HASH = 7

    def __init__(self, channel_name: str):
        super().__init__()
        self.child_conn = None
        self.channel_name: str = channel_name
        self.user_id: str = Ttv.get_user_id(channel_name)
        self.start_time: datetime = datetime.now()
        self.log_file_string: str = self.generate_file_name_for_instance()
        self.is_logging = False
        self.is_online = Ttv.isOnline(channel_name)
        # Given unique name so getLogger doesnt interfere with other threads' loggers and is thread safe.
        self._logger = logging.getLogger(name=f'{self.log_file_string}_logger')
        self._formatter = logging.Formatter("%(asctime)s - %(message)s", datefmt='%Y-%m-%d_%H:%M:%S')
        self._logger.setLevel(logging.DEBUG)
        logging_handler = logging.FileHandler(filename=self.log_file_string)
        logging_handler.setFormatter(self._formatter)
        self._logger.addHandler(logging_handler)

    '''
    Returns a string of the file name for the logging instance.
    '''
    def generate_file_name_for_instance(self):
        rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=self.LENGTH_OF_HASH))
        self.log_file_string = f'../Logs/{self.channel_name}_{rand}_{datetime.date(self.start_time)}.log'
        return self.log_file_string

    def run_logging(self, child_conn):
        self.child_conn = child_conn
        self.is_logging = True
        sock = socket.socket()
        sock.setblocking(False)
        sock.settimeout(TIME_OUT_SEC)
        log_path: str = self.start_logging_until_stopped(sock)

        if os.path.getsize(log_path) != 0:
            post_process_file(self.log_file_string)

        self.shutdown()

    # TODO: Make sure that concurrent process works, and that you can cancel this from main process.
    #  Abstract the initialization of self.is_logging to another function which sets it to true, starts
    #  logging, then calls shutdown() to cleanly shutdown this process.

    '''
    Starts the logging process. For this to function properly, it should be called from self.start(), which
    initializes necessary variables and contains the entire flow of the program from logging --> graphing --> clipping
    '''
    def start_logging_until_stopped(self, sock):
        # Uses the socket to connect to Twitch IRC
        sock.connect((Const.server, self.PORT))
        print(f"Connected to {self.channel_name}")
        sock.send(f"PASS {Const.token}\n".encode('utf-8'))
        sock.send(f"NICK {Const.nickname}\n".encode('utf-8'))
        sock.send(f"JOIN #{self.channel_name}\n".encode('utf-8'))
        # First two messages of confirmation received and not logged.
        sock.recv(2048).decode('utf-8')
        sock.recv(2048).decode('utf-8')

        current_time = self.start_time
        while self.is_logging:

            # Only checks if online every X seconds.
            if datetime.now() - current_time > timedelta(seconds=ONLINE_ON_INTERVAL):
                current_time = datetime.now()
                self.is_online = Ttv.isOnline(self.channel_name)

            if not self.is_online:
                print(f'{self.channel_name} is offline.')
                break

            try:
                resp = sock.recv(2048).decode('utf-8')
                if resp.startswith('PING'):
                    sock.send("PONG\n".encode('utf-8'))
                elif len(resp) > 0:
                    self._logger.info(demojize(resp))
            except socket.timeout:
                print(f"{self.channel_name} timed out, {TIME_OUT_SEC} seconds elapsed before message was sent.")
                break

            # Read from pipe connected to main process to see if I should shutdown

            if self.child_conn.poll() and self.child_conn.recv() == 'STOP':
                self.stop_logging()
                print("Stopped logging from main process")
                break

        sock.close()
        return self.log_file_string

    '''
    Stops logging. 
    '''

    def stop_logging(self):
        self.is_logging = False

    '''
    Ends the process.
    '''

    def shutdown(self):
        self.child_conn.close()
        pass


if __name__ == '__main__':
    test = LoggingSession('sco')
    print(test.log_file_string)
    test.start()
