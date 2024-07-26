import sys
import subprocess
import warnings
import platform
import re
import os

def getoutput(cmd, successful_status=(0,)):
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode in successful_status:
            return result.stdout.strip()
        else:
            warnings.warn(f"Command {cmd} failed with status {result.returncode}", UserWarning)
    except Exception as e:
        warnings.warn(str(e), UserWarning)
    return None

class CPUInfoBase:
    def __init__(self):
        self.info = {}

    def get_nbits(self):
        return platform.architecture()[0]

    def is_32bit(self):
        return self.get_nbits() == '32bit'

    def is_64bit(self):
        return self.get_nbits() == '64bit'

    def get_n_cpus(self):
        return os.cpu_count()

class LinuxCPUInfo(CPUInfoBase):
    def __init__(self):
        super().__init__()
        self.info['uname_m'] = getoutput(['uname', '-m'])
        try:
            with open('/proc/cpuinfo') as f:
                for line in f:
                    if ':' in line:
                        name, value = [s.strip() for s in line.split(':', 1)]
                        if name == 'model name': # very hacky name change lol
                            name = 'ProcessorNameString'
                        self.info[name] = value
        except FileNotFoundError:
            warnings.warn("/proc/cpuinfo not found", UserWarning)

class DarwinCPUInfo(CPUInfoBase):
    def __init__(self):
        super().__init__()
        self.cpu_name = getoutput(['Sysctl', '-n', 'machdep.cpu.brand_string'])
        self.info = {}
        self.info['ProcessorNameString'] = self.cpu_name

class WindowsCPUInfo(CPUInfoBase):
    def __init__(self):
        super().__init__()
        self.info['arch'] = platform.machine()
        self.info.update(self.get_registry_info())


    def get_registry_info(self):
        import winreg
        info = {}
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
            for i in range(winreg.QueryInfoKey(key)[1]):
                name, value, _ = winreg.EnumValue(key, i)
                info[name] = value
        except FileNotFoundError:
            warnings.warn("Registry key not found", UserWarning)
        return info

def get_cpu_info():
    system = platform.system().lower()
    if system == 'linux':
        return LinuxCPUInfo()
    elif system == 'darwin':
        return DarwinCPUInfo()
    elif system == 'windows':
        return WindowsCPUInfo()
    else:
        raise NotImplementedError(f"CPU information retrieval not implemented for {system}")