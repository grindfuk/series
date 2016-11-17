import pandas as pd
import numpy as np
import shutil
import os
import urllib.request
import zipfile
import shutil

df = pd.read_csv('teamlist.tsv', sep=',')

stud_dir = 'student_solutions'
print('copying test files...')
filedir = 'tests'
files_to_copy = ['all_tests.py', 'run_tests.py']
for team in df['Team']:
    for file in files_to_copy:
        try:
             shutil.copy(os.path.join(filedir, file), os.path.join(stud_dir, team, file))
        except:
             print("Cannot copy files over for testing %s", team)

print('done!')
