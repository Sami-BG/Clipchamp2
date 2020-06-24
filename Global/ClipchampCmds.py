from multiprocessing import Process, Pipe
from AutoClipper import Logger
from Twitch import TwitchAPI as Ttv

list_of_logging_sessions = [] # Triple of (LoggingSession, Process, Connection to pipe)
completed_sessions = []


def view_logging_sessions():
    to_return = [f"\t[{index}] - {channel_name}\n" for index, channel_name in enumerate(list_of_logging_sessions)]
    print("\nVIEWING:\n")
    for string_name in to_return:
        print(string_name)


def remove_logging_session():
    view_logging_sessions()
    usr_in = input("Type the number corresponding to the channel you want to remove: ")

    if usr_in == "":
        return

    try:
        number = int(usr_in)
        session, process, parent_conn = list_of_logging_sessions.pop(number)
        # Send stop command through pipe
        try:
            parent_conn.send('STOP')
        except BrokenPipeError as e:
            print(f"Pipe broken, tried to remove offline streamer. Filename: {e.filename}")
        # Join process
        process.join()
        # Append to completed sessions
        completed_sessions.append(session)
    except TypeError:
        print("Number please.")
    except IndexError:
        print("Out of bounds.")


def add_new_logging_session():
    usr_in = input("Type the name of the channel you want to log, or click enter to go back and do nothing:")

    if usr_in == "":
        return

    if Ttv.get_user_id(usr_in) is None:
        print(f'Channel {usr_in} does not exist.')
        return

    session = Logger.LoggingSession(usr_in)

    parent_conn, child_conn = Pipe()
    p = Process(target=session.run_logging, args=(child_conn,))
    list_of_logging_sessions.append((session, p, parent_conn))
    p.start()

    print(f'Added {usr_in}')
