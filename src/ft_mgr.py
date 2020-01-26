import ft_util
from ft_task import FtTaskParam,FtTask,FtTaskState

class FtMgrState():
    FtMgrIdle = 0
    FtMgrWorking = 1
    FtMgrSuspend = 2

class FtMgrTaskOps():
    FtMgrTaskNew = 0
    FtMgrTaskDelete = 1
    FtMgrTaskUpdate = 2
    FtMgrTaskSuspend = 3
    FtMgrTaskProcOn = 4
    FtMgrTaskDone = 5

class FtMgr(object):
    def __init__(self, name):
        self.name = name
        self.mgr_state = FtMgrState.FtMgrIdle
        self.cur_task = None

        self.on_task_list = []
        self.abandon_task_list = []
        self.done_task_list = []

        print('mgr: %s created'%(self.name))

    def dump_mgr_info(self):
        print('Mgr Name is %s'%(self.name))
        ft_util.ft_util_dump_task_list(self.on_task_list, 'on_list')
        ft_util.ft_util_dump_task_list(self.done_task_list, 'done_list')

    def switch_task(self, task_id, op, params):
        print('switch E: op %d, task_id %s'%(op, task_id))

        if op != FtMgrTaskOps.FtMgrTaskNew:
            tmp_task = self.__find_task_by_id(task_id)
            if None == tmp_task:
                print('task_id %s invalid, switch task failed'%(task_id))
                return -1

        if op == FtMgrTaskOps.FtMgrTaskNew:
            self.__new_task(params)

        elif op == FtMgrTaskOps.FtMgrTaskProcOn:
            self.__proc_task(tmp_task)
        elif op == FtMgrTaskOps.FtMgrTaskDone:
            self.__done_task(tmp_task)
        elif op == FtMgrTaskOps.FtMgrTaskSuspend:
            self.__stop_task(tmp_task)

        print('switch_task X success')

        return 0

    def __find_task_by_id(self, task_id):
        tmp_task = ft_util.ft_util_find_task_in_list(self.on_task_list, task_id)
        if None != tmp_task:
            return tmp_task

        tmp_task = ft_util.ft_util_find_task_in_list(self.done_task_list, task_id)
        if None != tmp_task:
            return tmp_task

        tmp_task = ft_util.ft_util_find_task_in_list(self.abandon_task_list, task_id)
        if None != tmp_task:
            return tmp_task

        return None

    def get_mgr_state(self):
        return self.mgr_state

    def __gen_task_id(self):
        #we think we can only create one task in one second
        return ft_util.ft_util_ts2str(ft_util.ft_util_get_cur_ts())

    def __clear_cur_task(self):
        self.cur_task = None

    def __new_task(self, params):
        if params is None:
            assert 0, 'params is None'

        task = FtTask(params)
        assert None != task , 'new task none'

        self.on_task_list.append(task)

        task.task_id = self.__gen_task_id()
        print('new task %s'%(task.task_id))

    def __proc_task(self, task):
        if task is None:
            assert 0, 'task is None'

        if None != self.cur_task:
            self.cur_task.stop()

        self.cur_task = task
        self.cur_task.start()
        self.mgr_state = FtMgrState.FtMgrWorking

    def __done_task(self, task):
        task_state = task.get_state()

        if (FtTaskState.FtTaskWorking == task_state) or (FtTaskState.FtTaskIdle == task_state):
            task.done()
            ft_util.ft_util_pop_task_from_list(task, self.on_task_list)

            self.done_task_list.append(task)

        if (task == self.cur_task):
            self.mgr_state = FtMgrState.FtMgrIdle
            self.__clear_cur_task()

    def __stop_task(self, task):
        task_state = task.get_state()
        if (FtTaskState.FtTaskWorking == task_state):
            task.stop()
            if (task == self.cur_task):
                self.mgr_state = FtMgrState.FtMgrIdle


    def get_cur_task(self):
        return self.cur_task

    def get_task_list(self):
        return self.on_task_list

    def get_abandon_task_list(self):
        return self.abandon_task_list

    def get_done_task_list(self):
        return self.done_task_list




