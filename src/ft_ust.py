
class FtUst(object):
    def __init__(self):
        self.workspace_path = '../dummy/'

    def import_ust(self, usf):
    	pass

    def export_ust(self, usf):
    	pass

    def query(self, key):
    	# FIXME:
    	if key == 'workspace_path':
    		return self.workspace_path

    def set(self, key, val):
    	pass

    def set_without_saving(self, key, val):
    	pass

    def sync(self):
    	pass