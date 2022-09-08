import shutil
mc_dir = 'C:/Users/Bee/AppData/Roaming/MultiChain'
try:
	shutil.rmtree(mc_dir)
except OSError as e:
        print(e)
print('Delete MultiChain dir success.')
