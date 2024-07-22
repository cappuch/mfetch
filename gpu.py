import platform
import subprocess
import time

def get_gpu_info():
    system = platform.system()
    if system == "Windows":
        return get_gpu_info_windows()
    elif system == "Linux":
        return get_gpu_info_linux()
    elif system == "Darwin":
        return get_gpu_info_macos()
    else:
        raise NotImplementedError(f"Unsupported OS: {system}")

def get_gpu_info_windows():
    gpus = []
    try:
        output = subprocess.check_output("wmic path win32_VideoController get name", shell=True)
        lines = output.decode().split("\n")
        for line in lines:
            if line.strip() and line.strip() != "Name":
                gpus.append(line.strip())
    except Exception as e:
        print(f"Error: {e}")
    return gpus

def get_gpu_info_linux():
    gpus = []
    try:
        output = subprocess.check_output("lspci | grep VGA", shell=True)
        lines = output.decode().split("\n")
        for line in lines:
            if line.strip():
                gpus.append(line.strip())
    except Exception as e:
        print(f"Error: {e}")
    return gpus

def get_gpu_info_macos():
    gpus = []
    try:
        output = subprocess.check_output("system_profiler SPDisplaysDataType", shell=True)
        lines = output.decode().split("\n")
        for line in lines:
            if "Chipset Model:" in line:
                gpus.append(line.split(":")[1].strip())
    except Exception as e:
        print(f"Error: {e}")
    return gpus

def get_current_gpu_driver():
    system = platform.system()
    if system == "Windows":
        return get_current_gpu_driver_windows()
    elif system == "Linux":
        return get_current_gpu_driver_linux()
    elif system == "Darwin":
        return get_current_gpu_driver_macos()
    else:
        raise NotImplementedError(f"Unsupported OS: {system}")

def get_current_gpu_driver_windows():
    try:
        output = subprocess.check_output("wmic path win32_VideoController get DriverVersion", shell=True)
        lines = output.decode().split("\n")
        for line in lines:
            if line.strip() and line.strip() != "DriverVersion":
                return line.strip()
    except Exception as e:
        print(f"Error: {e}")
    return None

def get_current_gpu_driver_linux():
    try:
        output = subprocess.check_output("glxinfo | grep 'OpenGL version'", shell=True)
        line = output.decode().strip()
        if line:
            return line.split(":")[1].strip()
    except Exception as e:
        print(f"Error: {e}")
    return None

def get_current_gpu_driver_macos():
    try:
        output = subprocess.check_output("system_profiler SPDisplaysDataType", shell=True)
        lines = output.decode().split("\n")
        for line in lines:
            if "Driver Version:" in line:
                return line.split(":")[1].strip()
    except Exception as e:
        print(f"Error: {e}")
    return None