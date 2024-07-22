default_conf = """
name_info = true
os_info  = true
cpu_info  = true
ram_usage  = true
gpu_info  = true
gpu_driver  = true
ip  = true

logo_path = '${BASE_DIR}/logo.txt
"""
import os

conf_file = "mfetch.conf"
# exist check
if not os.path.exists(conf_file):
    print("Config file not found, creating one...")
    open(conf_file,'w').write(default_conf)
    print("Config file created.")

conf = open(conf_file).read()


def read_conf():
    infos = []
    logo_path = ''
    
    for line in conf.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        
        if '=' in line:
            key, value = map(str.strip, line.split('='))
            if key.endswith('_info') or key in ['ram_usage', 'ip']:
                if value.lower() == 'true':
                    infos.append(key)
            elif key == 'logo_path':
                logo_path = value.strip("'\"")
    
    base_dir = os.path.dirname(os.path.abspath(conf_file))
    logo_path = logo_path.replace('${BASE_DIR}', base_dir) # so cheap but :balling:
    
    return infos, logo_path