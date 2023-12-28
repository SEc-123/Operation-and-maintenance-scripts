import psutil
import datetime

def get_process_info(process):
    if process.status() == psutil.STATUS_RUNNING:
        return f"{datetime.datetime.now().strftime('%b %d %H:%M:%S')} {process.name()}[PID={process.pid}]:"
    else:
        return None

def get_network_info(connection):
    remote_ip = connection.raddr[0] if connection.raddr else None
    if remote_ip:
        return f"{datetime.datetime.now().strftime('%b %d %H:%M:%S')} Network connection to {remote_ip}:"
    return None

def write_current_info(file_path, data, is_process=True):
    """
    将当前信息写入文件
    """
    with open(file_path, 'w') as current_file:
        for item in data:
            if is_process and item:
                current_file.write(f"{item}\n")
            elif not is_process and item:
                # For network connections, log only remote IP
                current_file.write(f"{item}\n")

def read_file_content(file_path):
    """
    读取文件内容并返回为一个集合
    """
    try:
        with open(file_path, 'r') as log_file:
            lines = log_file.readlines()
        return set(line.strip() for line in lines)
    except FileNotFoundError:
        return set()

def write_to_log(log_file_path, data, ignore_python3=False, ignore_same_pid=True):
    """
    将数据写入日志文件
    """
    with open(log_file_path, 'a') as log_file:
        processed_pids = set()  # To track processed PIDs
        for item in filter(None, data):  # Skip None entries
            if ignore_python3 and 'Name: python3' in item:
                continue
            if ignore_same_pid:
                pid = item.split("[PID=")[1].split("]")[0]  # Extract PID from the item
                if pid in processed_pids:
                    continue
                processed_pids.add(pid)
            log_file.write(f"{item}\n")

def check_for_new_info(previous_info, current_info, log_file_path, ignore_python3=False, ignore_same_pid=True):
    """
    检查当前信息和初始信息的差异，如果有新增，则写入日志文件
    """
    new_info = current_info - previous_info
    if new_info:
        print(f"新增信息写入 {log_file_path}:")
        for item in new_info:
            print(item)
        write_to_log(log_file_path, new_info, ignore_python3=ignore_python3, ignore_same_pid=ignore_same_pid)
    else:
        print(f"没有新增信息")

if __name__ == "__main__":
    # 获取当前运行中的进程和网络连接
    current_processes = [get_process_info(p) for p in psutil.process_iter(['pid', 'name', 'status'])]
    current_connections = [get_network_info(conn) for conn in psutil.net_connections(kind='inet')]

    # 写入当前进程和网络连接信息到文件
    write_current_info('/var/log/check/current-app.log', current_processes)
    write_current_info('/var/log/check/current-net.log', filter(None, current_connections), is_process=False)

    # 获取初始进程和网络连接信息
    previous_processes = read_file_content('/var/log/check/previous-app.log')
    previous_connections = read_file_content('/var/log/check/previous-net.log')

    # 检查新增的
    check_for_new_info(previous_processes, set(current_processes), '/var/ossec/logs/active-responses.log', ignore_python3=True, ignore_same_pid=True)
    check_for_new_info(previous_connections, set(previous_connections), '/var/ossec/logs/active-responses.log', ignore_python3=True, ignore_same_pid=True)
