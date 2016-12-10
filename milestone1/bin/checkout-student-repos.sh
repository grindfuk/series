#!usr/bin/bash
# Run this from the root directory to checkout all the student repos. 

mkdir student_solutions

cd student_solutions
git clone -n https://github.com/slac207/cs207project.git slac207
cd slac207/
git checkout -b grading cf745542a52e44ddadfa2d753eaee65f9cfce9de
cd ..

git clone -n https://github.com/gitrdone4/cs207project.git gitrdone4
cd gitrdone4/
git checkout -b grading ed14b8edc6152e6aca65f08a2db57803e924df6b
cd ..

git clone -n https://github.com/cs207-2016/cs207project.git cs207-2016
cd cs207-2016/
git checkout -b grading fb9d1e4e732387e60b9c25c8a5cd0667da8284c7
cd ..

git clone -n https://github.com/ecnc/cs207project.git ecnc
cd ecnc/
git checkout -b grading 10b5c92ba7a0169bd5723cacd0e7fc4ccf1528df
cd ..

git clone -n https://github.com/glacierscse/cs207project.git glacierscse
cd glacierscse/
git checkout -b grading 988d3494347878549d7be72378f168f8a2b11db9
cd ..

git clone -n https://github.com/CSE-01/cs207project.git CSE-01
cd CSE-01/
git checkout -b grading 131bdcad57ad2fc2ffefef4a4664a39d359c6f53
cd ..

git clone -n https://github.com/rubix-cube/cs207project.git rubix-cube
cd rubix-cube/
git checkout -b grading dabe4cd98dcbcb6698db71d8187d6a3db1da6209
cd ..

git clone -n https://github.com/ATeamHasNoName/CS207Project.git ATeamHasNoName
cd ATeamHasNoName/
git checkout -b grading 93f15b5fd398856aa1a2866b2170a8f7e229bd63
cd ..

git clone -n https://github.com/jovhscript/cs207project.git jovhscript
cd jovhscript/
git checkout -b grading d76e4997922e8c5af728fcb0cb528186e25f3b14
cd ..

# cd ..
# cp tests/run_tests.py 
