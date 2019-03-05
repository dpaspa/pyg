import olefile
ole = olefile.OleFileIO('/home/dpaspa/MEGA/Business/Synertec/Spimaco/time/test.mpp')
#print ole.get_type('   114/TBkndTask/Var2Data')
#tasks = ole.openstream('   114/TBkndTask/Var2Data')
tasks = ole.openstream(['   114', 'TBkndTask', 'Props'])
print tasks
#data = tasks.read()
for t in tasks:
	print t
	break
m = olefile.OleMetadata()
print m.parse_properties(ole)
ole.close()
