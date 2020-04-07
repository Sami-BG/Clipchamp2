list_of_logging_sessions = []

def view_logging_sessions():
    to_return = [f"\t[{index}] - {channel_name}\n" for index, channel_name in enumerate(list_of_logging_sessions)]
    print("\nVIEWING:\n")
    for string_name in to_return:
        print(string_name)


def remove_logging_session():
    usr_in = input("Type the number corresponding to the channel you want to remove: ")
    view_logging_sessions()

    if usr_in == "":
        return

    try:
        number = int(usr_in)
        list_of_logging_sessions.pop(number)
    except TypeError:
        print("Number please.")
    except IndexError:
        print("Out of bounds.")


def add_new_logging_session():
    usr_in = input("Type the name of the channel you want to log, or click enter to go back and do nothing:")

    # TODO: This just appends a string. It should later append a Clipchamp Session object here.
    if usr_in == "":
        return

    list_of_logging_sessions.append(usr_in)
    print(f'Added {usr_in}')
