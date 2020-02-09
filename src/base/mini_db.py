import sqlite3
import threading
import time 

# https://www.sqlite.org/datatype3.html

class MiniDBPerItem(object):
    def __init__(self, name, datatype, is_primary):
        #cursor.execute('create table user (id varchar(20) primary key, name varchar(20))')
        self.name = name
        self.datatype = datatype
        self.is_primary = is_primary
        self.val = None

        self.__lock = threading.Lock()

    def dump(self):
        print('name: %s, dt: %s'%(self.name, self.datatype))

    def __lock_in(self):
        self.__lock.acquire(blocking = False)
        while True:
            ret = self.__lock.locked()
            if False == ret:
                print('%s: acquire lock failed'%(self.name))
                time.sleep(0.05)
            else:
                #self.__lock.acquire()
                break

    def __unlock(self):
        self.__lock.release()

    def get_create_cmd(self):
        cmd = self.name + ' ' + self.datatype
        if True == self.is_primary:
            cmd = cmd + ' '
            cmd = cmd + 'primary key'

        return cmd

    def set_val(self, val):
        self.__lock_in()
        self.val = val
        self.__unlock()

    def get_op_val(self, is_insert):
        assert self.val != None, 'get_op_val: val could not be None'
        # TODO: Currently, we just support two type, integer and VARCHAR(255)
        if self.datatype == 'INTEGER' or self.datatype == 'UNSIGNED BIG INT':
            return str(self.val)
        else:
            if is_insert == True:
                cmd = ''
                cmd += '\''
                cmd += self.val
                cmd += '\''
                return cmd
            else:
                return self.val


class MiniDB(object):
    def __init__(self, filename):
        assert None != filename, 'null file name'

        self.filename = filename

        self.conn = sqlite3.connect(filename)
        assert None != self.conn, 'connect db failed'

        self.cursor = self.conn.cursor()
        assert None != self.cursor, 'get db cursor failed'

    # must call before every thing
    def init_tbl(self, table_name, items_list):
        cmd = self.__proc_items_list_init(items_list, table_name)
        try:
            self.cursor.execute(cmd)
        except sqlite3.OperationalError as e:
            print(e)
        finally:
            pass

    def __proc_items_list_init(self, items_list, table_name):
        assert None != items_list, 'null list'
        assert 0 != len(items_list), 'list len could not be 0'
        assert None != table_name, 'null table_name'

        idx = 0
        primary_ref_cnt = 0
        primary_idx = 0

        for x in items_list:
            if x.is_primary == True:
                primary_ref_cnt += 1

                if primary_ref_cnt >= 2:
                    break

                primary_idx = idx

            idx += 1

        assert primary_ref_cnt == 1, 'invalid primary_ref_cnt'

        x = items_list[primary_idx]

        cmd = 'create table '
        cmd += table_name
        cmd += ' ('

        cmd += x.get_create_cmd()

        idx = 0
        for x in items_list:
            if idx == primary_idx:
                idx += 1
                continue

            cmd += ', '
            cmd += x.get_create_cmd()

            idx += 1

        cmd += ')'

        print('cmd: %s'%(cmd))
        return cmd

    def insert(self, table_name, items_list):
        cmd = ''
        cmd += 'insert into '
        cmd += table_name + ' ('

        idx = 0

        for x in items_list:
            if idx != 0:
                cmd += ', '
            cmd += x.name
            idx += 1

        cmd += ') values ('

        idx = 0

        for x in items_list:
            if idx != 0:
                cmd += ', '

            cmd += x.get_op_val(True)
            idx += 1

        cmd += ')'

        print('insert cmd %s'%(cmd))
        self.cursor.execute(cmd)

        self.conn.commit()

    def lookup(self, table_name, items_list):
        #TODO: Now we just support one item
        #cursor.execute('select * from user where name=? and pwd=?', ('abc', 'password'))
        cmd = ''
        cmd += 'select * from '
        cmd += table_name + ' where '

        idx = 0

        for x in items_list:

            if idx != 0:
                cmd += ' and '

            cmd += x.name + '=?'

            idx += 1

        #self.cursor.execute('select * from tbl where id=?', (0, ))
        self.cursor.execute(cmd, (items_list[0].get_op_val(False), ))
        values = self.cursor.fetchall()
        return values

    def delete(self, table_name, items_list):
        #DELETE FROM COMPANY WHERE ID = 7
        cmd = ''
        cmd += 'DELETE FROM '
        cmd += table_name + ' where '

        for x in items_list:
            cmd += x.name
            cmd += '= '
            cmd += x.get_op_val(False)

        self.cursor.execute(cmd)

        self.conn.commit()

    def __update_cmd_by_item(self, item):
        return item.name + ' = ' + item.get_op_val(True)

    def update(self, table_name, items_list):
        #UPDATE COMPANY SET ADDRESS = 'Texas' WHERE ID = 6
        cmd = ''
        cmd += 'UPDATE ' + table_name
        cmd += ' set ' + self.__update_cmd_by_item(items_list[1]) + ' where ' + self.__update_cmd_by_item(items_list[0])
        self.cursor.execute(cmd)
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()
        print('db %s is closed..'%(self.filename))








