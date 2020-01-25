import ft_util
from ft_mgr import FtMgr,FtMgrTaskOps
from ft_task import FtTaskParam,FtTask,FtTaskState

gFtMgr = FtMgr('cmd_app')

def __new_task_server(task_para):
	assert task_para != None, 'task_param is none'
	gFtMgr.switch_task('', FtMgrTaskOps.FtMgrTaskNew, task_para)

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

def __print_menu():
	print('new[n]           --- new a task')
	print('start[s] xxx     --- start xxx task')
	print('pause[p]         --- pause task')
	print('finish[f] xxx    --- finish xxx task')
	print('abandon[ab] xxx  --- abandon xxx task')
	print('resume [r] xxx   --- resume or redo xxx task')
	print('print            --- print all task')
	print('help[h]          --- help(menu)')
	print('exit[q]          --- quit app')

	print('(dev)mgr_dump    --- dump mgr info(for developer)')

def __parse_cmd(cmd):
	if cmd == 'help' or cmd == 'h':
		__print_menu()
		return

	if cmd == 'q' or cmd == 'exit':
		print('GoodBye!\n')
		exit(0)

	if cmd == 'print':
		return

	if cmd == 'new' or cmd == 'n':
		__new_task_ui()
		return

	if cmd == 'mgr_dump':
		assert None != gFtMgr, 'none ft'
		gFtMgr.dump_mgr_info()
		return

	print('ERROR: Invalid Cmd Input -- %s'%(cmd))


if __name__ == "__main__":
	print('Welcome to FastTodo, input [h] for help')
	__print_menu()
	while True:

		cmd = ft_util.ft_util_read_line()
		__parse_cmd(cmd)

