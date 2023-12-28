import psutil
import datetime
import ipaddress

def is_internal_ip(ip_address):
    internal_ip_prefixes = ['127', '192', '10', '198', '255', '172']
    for prefix in internal_ip_prefixes:
        if ip_address.startswith(prefix):
            return True
    return False

def get_process_info(process):
    return f"PID: {process.info['pid']}, Parent: {process.info['ppid']}, Name: {process.info['name']}"

def get_network_info(connection):
    remote_ip = connection.raddr[0] if connection.raddr else None
    if remote_ip and not is_internal_ip(remote_ip) and ':' not in remote_ip:
        return remote_ip
    return None

def write_to_log(file_path, data):
    # 清空文件内容
    with open(file_path, 'w'):
        pass
    
    with open(file_path, 'a') as log_file:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_file.write(f"{timestamp}\n")
        for item in data:
            if item:
                log_file.write(f"{item}\n")

if __name__ == "__main__":
    # 获取当前进程和网络连接
    current_processes = [get_process_info(p) for p in psutil.process_iter(['pid', 'ppid', 'name'])]
    current_connections = [get_network_info(conn) for conn in psutil.net_connections(kind='inet')]

    # 写入日志文件
    write_to_log('/var/log/check/previous-app.log', current_processes)
    write_to_log('/var/log/check/previous-net.log', filter(None, current_connections))

    print("初始进程和网络连接已记录到 /var/log/check/previous-app.log 和 /var/log/check/previous-net.log 文件中。")
