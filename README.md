通过检查进程和网络连接的脚本，类似于文件完整性的检查。

通过strat.py记录初始进程状态或者网络连接状态，通过check.py检测新增的进程和网络连接来确认是否有异常，有两种类型：

strat.py与check.py #定义记录格式为syslog的格式 

strat.py（无格式）与check.py（无格式） #没有定义记录格式

start.py只需要在最初使用一次，记录后，讲check.py与定时任务联动即可，有新增或者变化会写入/var/ossec/logs/active-responses.log日志中，日志路径可自行修改。

By checking scripts for processes and network connections, similar to checking file integrity.
Record the initial process status or network connection status through strata. py, and check if there are any abnormalities by detecting newly added processes and network connections through checkout. py. There are two types:
Strata. py and check. py # Define the record format as syslog format
Strata. py (unformatted) and check. py (unformatted) # No record format defined
Start. py only needs to be used once initially, and after recording, it can be linked with scheduled tasks by checking. py. Any additions or changes will be written to the/var/ossec/logs/active responses. log log log, and the log path can be modified on its own.
