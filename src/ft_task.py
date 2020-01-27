import ft_util

def task_state_i2a(state_int):
    if state_int == FtTaskState.FtTaskIdle:
        return 'TaskIdle'
    if state_int == FtTaskState.FtTaskWorking:
        return 'Working'
    if state_int == FtTaskState.FtTaskDone:
        return 'Done'
    if state_int == FtTaskState.FtTaskDone:
        return 'Abandon'

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

class FtTask(object):
    def __init__(self, params):
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
        print('task %s-%s just start'%(self.task_id, self.name))

    def abandon(self):
        self.end_time = ft_util.ft_util_get_cur_ts()
        self.state = FtTaskState.FtTaskIdle
        print('task %s-%s just abandon'%(self.task_id, self.name))

    def stop(self):
        self.end_time = ft_util.ft_util_get_cur_ts()
        self.state = FtTaskState.FtTaskIdle
        print('task %s-%s just stop'%(self.task_id, self.name))

    def done(self):
        self.end_time = ft_util.ft_util_get_cur_ts()
        self.state = FtTaskState.FtTaskDone
        print('task %s-%s just done'%(self.task_id, self.name))

    def dump(self):
        #       id     name   crea    stat   prio  is_da state 
        print('%20s\t %16s\t %11d\t %11d\t %6d\t %8d\t %12s\t'%(self.task_id, self.name, self.create_time, self.start_time, self.prior, self.is_date, task_state_i2a(self.state)))



