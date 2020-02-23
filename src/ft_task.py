import sys
sys.path.append('./base/')

import ft_util
from mini_db import MiniDBPerItem, MiniDB

def task_state_i2a(state_int):
    if state_int == FtTaskState.FtTaskIdle:
        return 'TaskIdle'
    if state_int == FtTaskState.FtTaskWorking:
        return 'Working'
    if state_int == FtTaskState.FtTaskDone:
        return 'Done'
    if state_int == FtTaskState.FtTaskDone:
        return 'Abandon'

def create_task_by_rec_db(db_result):
    assert db_result != None, 'null db_result'
    assert len(db_result) != 1, 'len of input must be one'

    para = FtTaskParam()

    para.task_name = db_result[1]
    para.prior = int(db_result[2])

    task_obj = FtTask(para)
    #Load Other Params
    task_obj.task_id = db_result[0]
    task_obj.state = int(db_result[3])
    task_obj.create_time = db_result[4]
    task_obj.start_time = db_result[5]
    task_obj.end_time = db_result[6]

    return task_obj


class FtTaskState(object):
    FtTaskIdle = 0
    FtTaskWorking = 1
    FtTaskDone = 2
    FtTaskAbandon = 3

class FtTaskParam(object):
    def __init__(self):
        self.task_id = '' #set by mgr, don't modify in app
        self.task_name = None
        self.prior = 0xff #bigger, the higher
        self.is_date = False
        self.date_time = None

        self.db_handle = None
        self.log_file_name = None

g_db_on_table_name = 'task_tbl0'

class FtTaskDb(object):
    def __init__(self, filename):
        self.db_hdl = MiniDB(filename)
        self.all_l = None

        assert self.db_hdl != None, 'create DB failed!!!'

        self.__init_items_and_tbl()

    def __init_items_and_tbl(self):
        self.all_l = []

        self.__item_task_id = MiniDBPerItem('task_id', 'VARCHAR(255)', True)
        self.all_l.append(self.__item_task_id)

        self.__item_task_name = MiniDBPerItem('task_name', 'VARCHAR(255)', False)
        self.all_l.append(self.__item_task_name)

        self.__item_prior = MiniDBPerItem('prior', 'INTEGER', False)
        self.all_l.append(self.__item_prior)

        self.__item_state = MiniDBPerItem('state', 'INTEGER', False)
        self.all_l.append(self.__item_state)

        self.__item_create_time = MiniDBPerItem('create_time', 'UNSIGNED BIG INT', False)
        self.all_l.append(self.__item_create_time)

        self.__item_start_time = MiniDBPerItem('start_time', 'UNSIGNED BIG INT', False)
        self.all_l.append(self.__item_start_time)

        self.__item_end_time = MiniDBPerItem('end_time', 'UNSIGNED BIG INT', False)
        self.all_l.append(self.__item_end_time)

        self.db_hdl.init_tbl(g_db_on_table_name, self.all_l)

    def insert(self, task_obj):
        assert task_obj != None, 'shold not be None'

        self.__item_task_id.set_val(task_obj.task_id)
        self.__item_task_name.set_val(task_obj.name)
        self.__item_prior.set_val(task_obj.prior)
        self.__item_state.set_val(task_obj.state)
        self.__item_create_time.set_val(task_obj.create_time)
        self.__item_start_time.set_val(task_obj.start_time)
        self.__item_end_time.set_val(task_obj.end_time)

        self.db_hdl.insert(g_db_on_table_name, self.all_l)

    def __get_item_obj(self, tag):
        if tag == 'task_id':
            return self.__item_task_id
        if tag == 'task_name':
            return self.__item_task_name
        if tag == 'prior':
            return self.__item_prior
        if tag == 'state':
            return self.__item_state
        if tag == 'create_time':
            return self.__item_create_time
        if tag == 'start_time':
            return self.__item_end_time
        if tag == 'end_time':
            return self.__item_end_time
        assert 0, 'tag invalid!! %s'%(tag)

    def update_by_id(self, tag, val, task_id):
        assert task_id != None, 'shold not be None'
        assert tag != None, 'shold not be None'
        assert val != None, 'shold not be None'

        taskid_item_obj = self.__get_item_obj('task_id')
        target_item_obj = self.__get_item_obj(tag)

        taskid_item_obj.set_val(task_id)
        target_item_obj.set_val(val)

        tmp_l = [taskid_item_obj, target_item_obj]

        self.db_hdl.update(g_db_on_table_name, tmp_l)

    def load_all_tasks(self, is_task_abandoned):
        if is_task_abandoned == False:
            state_obj = self.__get_item_obj('state')
            state_obj.set_val(FtTaskState.FtTaskIdle)
            tmp_l = [state_obj]

            res_idle = self.db_hdl.lookup(g_db_on_table_name, tmp_l)

            state_obj.set_val(FtTaskState.FtTaskWorking)
            res_working = self.db_hdl.lookup(g_db_on_table_name, tmp_l)
            if 0 != len(res_working):
                res_idle.append(res_working[0])

            return res_idle

    def close(self):
        self.db_hdl.close()

class FtTask(object):
    def __init__(self, params):
        self.task_id = ' '
        self.name = params.task_name
        self.prior = params.prior
        self.state = FtTaskState.FtTaskIdle

        self.create_time = ft_util.ft_util_get_cur_ts()

        self.start_time = 0
        self.end_time = 0

        self.date_time = params.date_time
        self.is_date = params.is_date

        self.is_update = False

    def __touch(self):
        # TODO: Need Lock
        self.is_update = True

    def need_update(self):
        return self.is_update

    def begin_update(self):
        # TODO: Lock Here
        pass

    def end_update(self):
        # TODO: UnLock Here
        pass

    def get_state(self):
        return self.state

    def start(self):
        self.start_time = ft_util.ft_util_get_cur_ts()
        self.state = FtTaskState.FtTaskWorking

        self.db_handle.update_by_id('start_time', self.start_time, self.task_id)
        self.db_handle.update_by_id('state', self.state, self.task_id)

        print('task %s-%s just start'%(self.task_id, self.name))

    def abandon(self):
        self.end_time = ft_util.ft_util_get_cur_ts()
        self.state = FtTaskState.FtTaskIdle

        self.db_handle.update_by_id('end_time', self.end_time, self.task_id)
        self.db_handle.update_by_id('state', self.state, self.task_id)

        print('task %s-%s just abandon'%(self.task_id, self.name))

    def stop(self):
        self.end_time = ft_util.ft_util_get_cur_ts()
        self.state = FtTaskState.FtTaskIdle

        self.db_handle.update_by_id('end_time', self.end_time, self.task_id)
        self.db_handle.update_by_id('state', self.state, self.task_id)

        print('task %s-%s just stop'%(self.task_id, self.name))

    def done(self):
        self.end_time = ft_util.ft_util_get_cur_ts()
        self.state = FtTaskState.FtTaskDone

        self.db_handle.update_by_id('end_time', self.end_time, self.task_id)
        self.db_handle.update_by_id('state', self.state, self.task_id)

        print('task %s-%s just done'%(self.task_id, self.name))

    def dump(self):
        #       id     name   crea    stat   prio  is_da state 
        print('%20s\t %16s\t %11d\t %11d\t %6d\t %8d\t %12s\t'%(self.task_id, self.name, self.create_time, self.start_time, self.prior, self.is_date, task_state_i2a(self.state)))

    def __insert_to_db(self):
        self.db_handle.insert(self)

    def set_task_file(self, db_handle, log_f):
        self.db_handle = db_handle
        self.log_file_name = log_f

        self.__insert_to_db()


