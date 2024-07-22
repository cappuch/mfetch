import os
import platform

def ram_info():
    total_ram = 0
    used_ram = 0
    
    try:
        if platform.system() == "Linux":
            with open("/proc/meminfo", "r") as f:
                mem_info = f.read().split("\n")
            
            for line in mem_info:
                if "MemTotal" in line:
                    total_ram = int(line.split()[1]) * 1024
                elif "MemAvailable" in line:
                    available_ram = int(line.split()[1]) * 1024
            
            used_ram = total_ram - available_ram
        
        elif platform.system() == "Darwin":
            vm_stat = os.popen('vm_stat').read().split('\n')
            page_size = int(os.popen('pagesize').read().strip())
            
            free_pages = int(vm_stat[1].split()[2].replace('.', ''))
            active_pages = int(vm_stat[2].split()[2].replace('.', ''))
            inactive_pages = int(vm_stat[3].split()[2].replace('.', ''))
            speculative_pages = int(vm_stat[4].split()[2].replace('.', ''))
            wired_pages = int(vm_stat[6].split()[2].replace('.', ''))
            
            total_ram = int(os.popen('sysctl -n hw.memsize').read().strip())
            used_ram = (active_pages + inactive_pages + wired_pages) * page_size
        
        elif platform.system() == "Windows":
            import ctypes
            
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]
            
            memoryStatus = MEMORYSTATUSEX() # SEX
            memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memoryStatus))
            
            total_ram = memoryStatus.ullTotalPhys
            used_ram = memoryStatus.ullTotalPhys - memoryStatus.ullAvailPhys
        
        else:
            raise NotImplementedError(f"Unsupported operating system: {platform.system()}")
        
        return total_ram, used_ram
    
    except Exception as e:
        print(f"Error getting RAM: {e}")
        return 0, 0

def total_ram():
    return ram_info()[0]

def current_ram_used():
    return ram_info()[1]
