import os, platform, socket
import cpu, gpu, mem, config
import argparse

def get_local_ip():  # there should be a better way to do this but this is good enough
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
        
    except Exception as e:
        print("Error occurred while fetching local IP address:", e)
        return "127.0.0.1"

def get_uname_info():
    info = platform.uname()
    system = info.system
    node = info.node
    release = info.release
    machine = info.machine

    return system, node, release, machine

def load_from_logo(path='logo.txt'):
    if os.path.isfile(path):
        with open(path, 'r') as f:
            return f.read()
    return os.path.join(__file__, path)

def info():
    infos, logo_path = config.read_conf()
    logo = load_from_logo(logo_path)
    logo_lines = logo.split('\n')
    
    system, node, release, machine = get_uname_info()
    info_dict = {
        "name_info": f"HOST: {node}",
        "os_info": f"OS INFO: {system} {release} {machine}",
        "cpu_info": f"CPU INFO: {cpu.get_cpu_info().info['ProcessorNameString']}",
        "ram_usage": f"Memory: {mem.current_ram_used()/1e9:.2f} GB/{mem.total_ram()/1e9:.2f} GB",
        "gpu_info": f"GPU: {', '.join(gpu.get_gpu_info())}",
        "gpu_driver": f"GPU Driver: {gpu.get_current_gpu_driver()}",
        "ip": f"Local IP Address: {get_local_ip()}"
    }
    
    info_lines = [info_dict[key] for key in infos if key in info_dict]
    
    max_logo_lines = max(len(logo_lines), len(info_lines))
    print('\n')
    
    for i in range(max_logo_lines):
        logo_part = logo_lines[i] if i < len(logo_lines) else ""
        info_part = info_lines[i] if i < len(info_lines) else ""
        print(f"{logo_part:<30} | {info_part}")

    print('\n')


def main():
    parser = argparse.ArgumentParser(description="mfetch")
    parser.add_argument("--logo", metavar="DIR", help="Change logo directory. Use ${BASE_DIR}/ if in the same folder as main.py")
    
    args = parser.parse_args()
    
    if args.logo:
        config.change_logo(args.logo)
        print(f"Logo directory changed to: {args.logo}")
    else:
        info()

if __name__ == "__main__":
    main()