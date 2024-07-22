import os

conf_file = "mfetch.conf"
default_conf = """
name_info = true
os_info = true
cpu_info = true
ram_usage = true
gpu_info = true
gpu_driver = true
ip = true

logo_path = '${BASE_DIR}/logo.txt'
"""

# exist check
if not os.path.exists(conf_file):
    print("Config file not found, creating one...")
    with open(conf_file, 'w') as f:
        f.write(default_conf)
    print("Config file created.")

def read_conf():
    with open(conf_file, 'r') as f:
        conf = f.read()

    infos = []
    logo_path = ''
    
    for line in conf.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        if '=' in line:
            key, value = map(str.strip, line.split('='))
            if key.endswith('_info') or key in ['ram_usage', 'ip', 'gpu_driver']:
                if value.lower() == 'true':
                    infos.append(key)
            elif key == 'logo_path':
                logo_path = value.strip("'\"")
    
    base_dir = os.path.dirname(os.path.abspath(conf_file))
    logo_path = logo_path.replace('${BASE_DIR}', base_dir)
    
    return infos, logo_path

def change_logo(new_dir):
    with open(conf_file, 'r') as f:
        conf = f.read()

    lines = conf.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith('logo_path'):
            lines[i] = f"logo_path = '{new_dir}'"
            break
    
    new_conf = '\n'.join(lines)
    
    with open(conf_file, 'w') as f:
        f.write(new_conf)