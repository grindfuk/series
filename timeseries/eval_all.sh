#!/bin/bash

# download all repos
#python3 download_files.py


# make results directory
if [ ! -d 'results' ]; then
	mkdir results
fi

# now execute tests on each team
for f in `ls fixed_student_solutions/cs207project`; do
	if [ -d "fixed_student_solutions/cs207project/$f" ]; then
		echo "processing team $f:"
		# copy tail of test file to individualized header
		cp -rf fixed_student_solutions/cs207project/$f/all_tests_head.py  fixed_student_solutions/cs207project/$f/all_tests.py
		cat all_tests_tail.py >> fixed_student_solutions/cs207project/$f/all_tests.py
		# copy run tests file
		cp run_tests.py fixed_student_solutions/cs207project/$f/run_tests.py
		# execute tests
		python3 fixed_student_solutions/cs207project/$f/run_tests.py > results/$f.txt 2>results/$f.err.log
	fi
done