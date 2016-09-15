def deleteemptymptiles():
	batfile = "C:\Example\file.bat"
	deleteemptymptiles = open(batfile, 'w')
	deleteemptymptiles.writelines('''
	@echo off
	pushd "E:\HUNT_'''+state+'''
	for %%j in (*) do if %%~zj lss 7900 del "%%~j"
	popd''' + '\n')
	deleteemptymptiles.flush()
	deleteemptymptiles.close()
	time.sleep(1)
	p = Popen(r'start cmd /c ' + batfile, shell=True)
	p.wait()
	time.sleep(1)
	print("All files smaller that 7.90kb have been removed.")