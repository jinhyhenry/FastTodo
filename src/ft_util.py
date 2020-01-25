import time
import sys

def ft_util_get_cur_ts():
    return int(time.time())

def ft_util_ts2str(ts):
    timeArray = time.localtime(ts)
    return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

def ft_util_read_line():
    c = sys.stdin.readline()

    # Now , c is end with a '\n', we need to remove that
    if c == '\n':
        return c

    c = c[0 : (len(c) - 1)]

    return c

def ft_util_is_read_line_empty(cmd):
    if cmd == '\n':
        return True

    return False

def ft_util_dump_task_list(tl, tag):
    if None is tl:
        print('task_list - %s is None , Fail to Dump'%(tag))
        return
    print('task_list %s dump begin --->'%(tag))

    for x in tl:
        x.dump()

    print('task_list %s dump end --->'%(tag))
