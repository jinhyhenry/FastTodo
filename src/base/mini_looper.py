import threading
import time

def ___get_mono_ts_ms():
    return int(1000 * time.monotonic())

class MiniTimerObj(object):
    def __init__(self, duration, cb, arg):
        self.duration = duration
        self.cb = cb
        self.arg = arg

        self.time_to_expose = 0

class MiniLooper(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.is_thr_run = True
        self.name = name

        self.timer_list = []
        self.abandon_timer_list = []

        self.sema = threading.Semaphore(0)
        self.lock = threading.Lock()

        self.cur_timer_node = None

    def __lock(self):
        while True:
            ret = self.lock.locked()
            if False == ret:
                print('%s: aquire lock failed'%(self.name))
                time.sleep(0.05)
            else:
                self.lock.aquire()
                break

    def __unlock(self):
        self.lock.release()

    def __sem_get(self, timeout_set):
        self.sema.acquire(timeout = timeout_set, blocking = True)

    def __sem_give(self):
        self.sema.release()

    def __set_cur_timer_node(self, timer_obj):
        self.__lock()
        self.cur_timer_node = timer_obj
        self.__unlock()

    def __calc_cur_time_timeout_ms(self):
        return 

    def __exec_cur_timer(self):
        self.cur_timer_node.cb(arg)

    # override thread's run(), don't call
    def run(self):
        print('%s: enter...'%(self.name))

        while self.is_thr_run:
            if None == self.cur_timer_node:
                time.sleep(0.05)
            else:
                timeout_set = self.__calc_cur_time_timeout_ms()
                if timeout_set:
                    ret = self.__sem_get(timeout_set)
                    # https://docs.python.org/3/library/threading.html#semaphore-objects
                    if True == ret:
                        self.__exec_cur_timer()
                    else:
                        continue




        print('%s: exit...'%(self.name))

    def start_looper(self):
        self.start()

    def stop_looper(self):
        pass

    def add_timer(self, duration, cb, arg):
        pass

    def remove_timer(self):
        pass

    def send(self, time_out):
        pass

    def destroy(self):
        pass
