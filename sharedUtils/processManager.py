import subprocess
import signal
import os


class ProcessManager:
    def __init__(self, application_path):
        self.application_path = application_path
        self.application_name = application_path.rsplit('/', 1)[-1]

    def restart(self):
        running_processes = self.get_running_processes()
        targeted_process_list = self.get_targeted_processes(running_processes)
        if len(targeted_process_list) > 0:
            pids = self.get_pids(targeted_process_list)
            for pid in pids:
                os.kill(int(pid), signal.SIGTERM)
                print("Killed process {}".format(pid))
        subprocess.Popen(["Python3", self.application_path])
        print("Started {}".format(self.application_path))

    def kill(self):
        running_processes = self.get_running_processes()
        targeted_process_list = self.get_targeted_processes(running_processes)
        if len(targeted_process_list) > 0:
            pids = self.get_pids(targeted_process_list)
            for pid in pids:
                os.kill(int(pid), signal.SIGTERM)
                print("Killed process {}".format(pid))
        else:
            print("No running processes named {}".format(self.application_name))

    def get_running_processes(self):
        cmd = ['ps', '-Af']
        pipe = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        processes = pipe.communicate()[0].decode('utf-8')
        print(processes)
        return processes

    def get_targeted_processes(self, running_processes):
        targeted_process_list = []
        for line in running_processes.split('\n'):
            if self.application_name in line:
                targeted_process_list.append(line)
        return targeted_process_list

    def get_pids(self, process_list):
        pid_list = []
        for process in process_list:
            process_components = process.split()
            pid = process_components[1]
            pid_list.append(pid)
        return pid_list

    def get_application_name(self):
        return self.application_name
