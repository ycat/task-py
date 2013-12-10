from plumbum import BG
# cmd1
# cmd3
# cmd2.after(lambda: Success(cmd1) and Success(cmd2) and Success(cmd3))

class Task:
    NOT_STARTED = 0
    RUNNING = 1
    COMPLETED = 2
    
    def __init__(self, cmd, description, stdout_log, stderr_log):
        self.cmd = cmd
        self.description = description
        self.stdout_log = stdout_log
        self.stderr_log = stderr_log
        self.process = None
        self.depends = []
        self.trigger_fn = None
    
    def run(self):
        self.is_running = True
        self.process = (self.cmd > stdout_log >= stderr_log) & BG

    def status(self):
        if self.process is None:
            return NOT_STARTED
        elif self.poll():
            return COMPLETED
        else:
            return RUNNING

    def return_code(self):
        if self.process is not None:
            return self.process.returncode
        else:
            return None
    
    def poll(self):
        if self.process is not None:
            return self.process.poll()
        else:
            return False

    def after(self, f):
        self.trigger_fn = f
        for name in f.func_code.co_names:
            obj = eval(name)
            if isinstance(obj, Cmd):
                self.depends.append(obj)

def RetCodeEquals(task, ret_code):
    return task.return_code() == ret_code




