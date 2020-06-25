from Main import ClipchampCmds
from Main.Command import Command
from Main.REPL import REPL


# Class for REPL of clipchamp. Repl commands are added in init function. Repl is started with start_clipchamp.
class ClipChamp:

    def __init__(self):
        self.repl = REPL()
        self.sessions = []
        add_log_cmd = Command("add", "Add a new Logging Session", ClipchampCmds.add_new_logging_session)
        view_logging_cmd = Command("view", "View logging sessions", ClipchampCmds.view_logging_sessions)
        remove_logging_cmd = Command("remove", "Remove a channel", ClipchampCmds.remove_logging_session)
        quit_cmd = Command("quit", "Quit", self.repl.quit)

        self.repl.add_to_map(add_log_cmd)
        self.repl.add_to_map(view_logging_cmd)
        self.repl.add_to_map(remove_logging_cmd)
        self.repl.add_to_map(quit_cmd)

    def start_clipchamp(self, home_string):
        self.repl.start_repl(home_string)

    def pop_session_at_index(self, index):
        self.sessions.pop(index)

    def add_session(self, session):
        self.sessions.append(session)


def get_sessions(clipchamp: ClipChamp):
    return clipchamp.sessions
