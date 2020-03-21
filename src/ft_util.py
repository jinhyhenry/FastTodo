import time
import sys
import os

def ft_util_get_cur_ts():
    return int(time.time())

def ft_util_ts2str(ts):
    timeArray = time.localtime(ts)
    return time.strftime("%Y-%m-%d-%H:%M:%S", timeArray)

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
        print('\n task_list - %s is None , Fail to Dump'%(tag))
        return
    print('     task_list %s dump begin --->\n'%(tag))
    #       id     name  crea stat prio  is_da state 
    print('%20s\t %16s\t %11s\t %11s\t %6s\t %8s\t %12s\t'%('task id', 'name', 'create ts', 'start ts', 'prior', 'is_date', 'state'))

    for x in tl:
        x.dump()

    print('\n<--- task_list %s dump end \n'%(tag))

def ft_util_find_task_in_list(tl, tsk_id):
    assert tl != None, 'task list is none'
    for x in tl:
        if x.task_id == tsk_id:
            return x
    return None

def ft_util_pop_task_from_list(task, tl):
    assert task != None, 'task is none'
    assert tl != None, 'task list is none'

    i = 0

    for x in tl:
        if x == task:
            break
        i = i + 1
    if i >= len(tl):
        print('no %d in %d'%(task, tl))
        return -1

    tl.pop(i)
    return 0

def __sort_by_prior(task):
    return task.prior

def __sort_by_create_time(task):
    return task.create_time

def ft_util_sort_task_by_prior(task_list):
    task_list.sort(key = __sort_by_prior)
    return task_list

def ft_util_format_cmd_split(cmd):
    return cmd.split(' ')

def ft_util_file_exist(file_name):
    return os.path.exists(file_name)

def ft_util_rm_file(file_name):
    if ft_util_file_exist(file_name):
        os.remove(file_name)

