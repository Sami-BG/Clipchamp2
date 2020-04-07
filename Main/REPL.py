from Main.Command import Command


class REPL:
    def __init__(self):
        self.number_of_cmds = 0
        self._repl_is_going = False
        # TODO: This should be of type dictionary[integer --> command], but im not sure of syntax, net is down
        self.map_of_commands: [int, Command] = dict()

    def add_to_map(self, cmd: Command) -> None:
        self.number_of_cmds += 1
        self.map_of_commands[self.number_of_cmds] = cmd

    def quit(self):
        self._repl_is_going = False

    def start_repl(self, home_string):
        self._repl_is_going = True
        while self._repl_is_going:
            usr_in = input(home_string)
            navigate_to_number = 0

            if usr_in == '':
                continue
            try:
                navigate_to_number = int(usr_in)
            except TypeError:
                print("Bad input.")
            except EOFError:
                break

            prompt_cmd = self.map_of_commands.get(navigate_to_number)

            # Not None, aka it returned something.
            if prompt_cmd:
                prompt_cmd.run()

    def getPromptFromMap(self, i):
        return self.map_of_commands.get(i).prompt


