#!/bin/python3

import pandas as pd

df = pd.read_csv('teamlist.tsv', sep=',')

with open('checkout.sh', 'w') as f:
	# create dir if necessary
	f.write('# This is a generated shell script from create_checkout_file.py\n')
	f.write('mkdir student_solutions\n')
	f.write('cd student_solutions\n')
	for key, val in df[['Team', 'url']].iterrows():
		team = val['Team']
		url = val['url']
		commit = val['url'].split('/')[-1]
		f.write('git clone -n https://github.com/{}/cs207project.git {}\n'.format(team, team))
		f.write('cd {}/\n'.format(team))
		f.write('git checkout -b grading {}\n'.format(commit))
		f.write('cd ..\n')
	f.write('cd ..\n')
