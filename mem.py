import os
import platform
import subprocess
import re
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
            ps = subprocess.Popen(['ps', '-caxm', '-orss,comm'], stdout=subprocess.PIPE).communicate()[0].decode()
            vm = subprocess.Popen(['vm_stat'], stdout=subprocess.PIPE).communicate()[0].decode()

            # Iterate processes
            processLines = ps.split('\n')
            sep = re.compile('[\s]+')
            rssTotal = 0 # kB
            for row in range(1,len(processLines)):
                rowText = processLines[row].strip()
                rowElements = sep.split(rowText)
                try:
                    rss = float(rowElements[0]) * 1024
                except:
                    rss = 0 # ignore...
                rssTotal += rss

            # Process vm_stat
            vmLines = vm.split('\n')
            sep = re.compile(':[\s]+')
            vmStats = {}
            for row in range(1,len(vmLines)-2):
                rowText = vmLines[row].strip()
                rowElements = sep.split(rowText)
                vmStats[(rowElements[0])] = int(rowElements[1].strip('\.')) * 4096

            used_ram = vmStats["Pages active"]
            total_ram = rssTotal
        
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
            
            memoryStatus = MEMORYSTATUSEX()
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