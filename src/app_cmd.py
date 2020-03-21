import ft_util
from ft_mgr import FtMgr,FtMgrTaskOps,FtMgrTaskListType
from ft_task import FtTaskParam,FtTask,FtTaskState,FtTaskProperty

gFtMgr = FtMgr('cmd_app')

def __new_task_server(task_para):
    assert task_para != None, 'task_param is none'
    gFtMgr.switch_task('', FtMgrTaskOps.FtMgrTaskNew, task_para)

def __start_task_server(task_id):
    assert task_id != None, 'task_id is none'
    gFtMgr.switch_task(task_id, FtMgrTaskOps.FtMgrTaskProcOn, None)

def __stop_task_server(task_id):
    assert task_id != None, 'task_id is none'
    gFtMgr.switch_task(task_id, FtMgrTaskOps.FtMgrTaskSuspend, None)

def __done_task_server(task_id):
    assert task_id != None, 'task_id is none'
    gFtMgr.switch_task(task_id, FtMgrTaskOps.FtMgrTaskDone, None)

def __resume_task_server(task_id):
    assert task_id != None, 'task_id is none'
    gFtMgr.switch_task(task_id, FtMgrTaskOps.FtMgrTaskResume, None)

def __abandon_task_server(task_id):
    assert task_id != None, 'task_id is none'
    gFtMgr.switch_task(task_id, FtMgrTaskOps.FtMgrTaskDelete, None)

def __sort_server(l_type, t_prop):
    gFtMgr.sort_task_list(l_type, t_prop)
    print('Done!')

def __sort_help_print():
    print('**** Sort Help E ****')

    print('list: Done %d, Working %d, FtMgrAbandon %d'%(FtMgrTaskListType.FtMgrAbandon, FtMgrTaskListType.FtMgrWorking, FtMgrTaskListType.FtMgrAbandon))

    print('task prop: Prior %d, CreateTime %d'%(FtTaskProperty.FtTaskPrior, FtTaskProperty.FtTaskCreateTime))

    print('**** Sort Help X ****')

def __new_task_ui():
    para = FtTaskParam()

    tmp_input = '\n'

    print('input task name: ')
    while True:
        tmp_input = ft_util.ft_util_read_line()
        if True == ft_util.ft_util_is_read_line_empty(tmp_input):
            print('you must input name')
        else:
            para.task_name = tmp_input
            break

    print('input task prior (default and low is 0xff): ')
    tmp_input = ft_util.ft_util_read_line()
    if True == ft_util.ft_util_is_read_line_empty(tmp_input):
        para.prior = 0xff
    else:
        para.prior = int(tmp_input)

    print('is date task[y/N], default is N: ')
    while True:
        tmp_input = ft_util.ft_util_read_line()
        if True == ft_util.ft_util_is_read_line_empty(tmp_input):
            para.is_date = False
            break
        else:
            if 'N' == tmp_input:
                para.is_date = False
                break
            elif 'y' == tmp_input:
                para.is_date = True
                break
                # Todo : Complete date info
            else:
                print('you must input N or y')

    __new_task_server(para)
    print('new task done!')

def __print_tasks():
    tmp_list = gFtMgr.get_task_list(FtMgrTaskListType.FtMgrWorking)
    ft_util.ft_util_dump_task_list(tmp_list, 'on_task')

    cur_task = gFtMgr.get_cur_task()
    if cur_task != None:
        print('CurTaskInfo...>')
        cur_task.dump()
        print('\n')

    tmp_list = gFtMgr.get_task_list(FtMgrTaskListType.FtMgrDone)
    ft_util.ft_util_dump_task_list(tmp_list, 'done_task')

    tmp_list = gFtMgr.get_task_list(FtMgrTaskListType.FtMgrAbandon)
    ft_util.ft_util_dump_task_list(tmp_list, 'abandon_task')

def __set_workspace_ui():
    print('Please Input ABSOLUTE-Path..')
    tmp_input = '\n'

    tmp_input = ft_util.ft_util_read_line()
    if tmp_input != '\n':
        gFtMgr.set_workspace(tmp_input)
    else:
        print('could\'t be none')

def __reset_task_db():
    gFtMgr.reset_task_db()

def __print_menu():
    print('\nFunctions --------------------->')
    print('new[n]           --- new a task')
    print('start[s] xxx     --- start xxx task')
    print('pause[p] xxx     --- pause task')
    print('finish[f] xxx    --- finish xxx task')
    print('abandon[ab] xxx  --- abandon xxx task')
    print('resume [r] xxx   --- resume or redo xxx task')
    print('print            --- print all task')
    print('reset            --- reset task rec db')
    print('help[h]          --- help(menu)')
    print('exit[q]          --- quit app')
    print('sort -l xx -c yy --- -l for type of list, -c for t_prop, -h for help')

    print('\nSettings --------------------->')
    print('print_ust[pu]    --- print user settings')
    print('set_work_path    --- set_workspace path')

    print('(dev)mgr_dump[md]    --- dump mgr info(for developer)')

def __parse_cmd(cmd):
    if cmd == 'help' or cmd == 'h' or cmd == '\n':
        __print_menu()
        return

    if cmd == 'q' or cmd == 'exit':
        print('GoodBye!\n')
        exit(0)

    if cmd == 'print':
        __print_tasks()
        return

    if cmd == 'reset':
        __reset_task_db()
        return

    if cmd == 'new' or cmd == 'n':
        __new_task_ui()
        return

    cmd_arg_l = ft_util.ft_util_format_cmd_split(cmd)
    if cmd_arg_l[0] == 'start' or cmd_arg_l[0] == 's':
        __start_task_server(cmd_arg_l[1])
        return

    cmd_arg_l = ft_util.ft_util_format_cmd_split(cmd)
    if cmd_arg_l[0] == 'pause' or cmd_arg_l[0] == 'p':
        __stop_task_server(cmd_arg_l[1])
        return

    cmd_arg_l = ft_util.ft_util_format_cmd_split(cmd)
    if cmd_arg_l[0] == 'finish' or cmd_arg_l[0] == 'f':
        __done_task_server(cmd_arg_l[1])
        return

    if cmd == 'mgr_dump' or cmd == 'md':
        assert None != gFtMgr, 'none ft'
        gFtMgr.dump_mgr_info()
        return

    cmd_arg_l = ft_util.ft_util_format_cmd_split(cmd)
    if cmd_arg_l[0] == 'resume' or cmd_arg_l[0] == 'r':
        __resume_task_server(cmd_arg_l[1])
        return

    cmd_arg_l = ft_util.ft_util_format_cmd_split(cmd)
    if cmd_arg_l[0] == 'abandon' or cmd_arg_l[0] == 'ab':
        __abandon_task_server(cmd_arg_l[1])
        return

    cmd_arg_l = ft_util.ft_util_format_cmd_split(cmd)
    if cmd_arg_l[0] == 'sort':
        if cmd_arg_l[1] == '-h':
            __sort_help_print()
        if cmd_arg_l[1] == '-l':
            if (len(cmd_arg_l) != 5):
                print('should enter: sort -l xx -c yy')
            __sort_server(int(cmd_arg_l[2]), int(cmd_arg_l[4]))
        return

    print('ERROR: Invalid Cmd Input -- %s'%(cmd))


if __name__ == "__main__":
    print('Welcome to FastTodo, input [h] for help')
    __print_menu()
    while True:

        cmd = ft_util.ft_util_read_line()
        __parse_cmd(cmd)

