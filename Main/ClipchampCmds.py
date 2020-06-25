from Main import Clipchamp as C


def view_logging_sessions(champ: C.ClipChamp):
    to_return = [f"\t[{index}] - {channel_name}\n" for index, channel_name in enumerate(C.get_sessions(champ))]
    print("\nVIEWING:\n")
    for string_name in to_return:
        print(string_name)


def remove_logging_session(champ: C.ClipChamp):
    usr_in = input("Type the number corresponding to the channel you want to remove: ")
    view_logging_sessions(champ)

    if usr_in == "":
        return

    try:
        number = int(usr_in)
        champ.pop_session_at_index(number)
    except TypeError:
        print("Number please.")
    except IndexError:
        print("Out of bounds.")


def add_new_logging_session(champ: C.ClipChamp):
    usr_in = input("Type the name of the channel you want to log, or click enter to go back and do nothing:")

    # TODO: This just appends a string. It should later append a Clipchamp Session object here.
    if usr_in == "":
        return

    champ.add_session(usr_in)
    print(f'Added {usr_in}')
