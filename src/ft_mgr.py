import ft_util
import ft_task
from ft_task import FtTaskParam,FtTask,FtTaskState,FtTaskDb
from ft_ust import FtUst

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
    FtMgrTaskResume = 6

g_db_file_name = 'ft_task_rec.db'

class FtMgr(object):
    def __init__(self, name):
        self.name = name
        self.mgr_state = FtMgrState.FtMgrIdle
        self.cur_task = None

        self.on_task_list = []
        self.abandon_task_list = []
        self.done_task_list = []

        self.__init_ust()
        self.__init_db_task_rec()

        print('mgr: %s created'%(self.name))

    def __init_ust(self):
        self.ust = FtUst()

    def __init_tasks_from_db_result(self, db_rec_result):
        print(db_rec_result)
        # TODO: create tasks
        for x in db_rec_result:
            obj = ft_task.create_task_by_rec_db(x)

            obj.set_task_file(self.task_rec_db, self.__compose_task_file_name(obj.task_id + '.log'), False)

            state = obj.get_state()

            if FtTaskState.FtTaskDone != state:
                self.on_task_list.append(obj)

                if FtTaskState.FtTaskWorking == state:
                    self.cur_task = obj
                    self.mgr_state = FtMgrState.FtMgrWorking

            else:
                self.done_task_list.append(obj)
        print('recover done')


    def __init_db_task_rec(self):
        db_file = self.__compose_task_file_name(g_db_file_name)
        self.task_rec_db = FtTaskDb(db_file)

        self.__init_tasks_from_db_result(self.task_rec_db.load_all_tasks(False))

    def reset_task_db(self):
        self.task_rec_db.close()
        ft_util.ft_util_rm_file(self.__compose_task_file_name(g_db_file_name))

        self.__init_db_task_rec()

    def __compose_task_file_name(self, file_name):
        return (self.ust.query('workspace_path') + file_name)

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
        elif op == FtMgrTaskOps.FtMgrTaskResume:
            self.__resume_task(tmp_task)

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

        task.set_task_file(self.task_rec_db, self.__compose_task_file_name(task.task_id + '.log'), True)

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

    def __resume_task(self, task):
        # TODO: this will search twice
        if task.resume() < 0:
            print('resume failed...')
        ft_util.ft_util_pop_task_from_list(task, self.done_task_list)
        self.on_task_list.append(task)

    def get_cur_task(self):
        return self.cur_task

    def get_task_list(self):
        return self.on_task_list

    def get_abandon_task_list(self):
        return self.abandon_task_list

    def get_done_task_list(self):
        return self.done_task_list

    def set_workspace(self, path):
        self.ust.set('workspace_path', path)
        # TODO: Reload file_path for every task

    def get_workspace(self):
        return self.ust.query('workspace_path')




