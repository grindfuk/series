Running all_tests.py
====================

1. Move the files into the student directory and change the directory to that file 
For example:

```
git clone https://github.com/ecnc/cs207project/tree/778b2e1ca4fd7cc522c5d1a2103541126d14e973
cp ./tests/run_tests.py ./ecnc/
cp ./tests/all_tests.py ./ecnc/
cd ./ecnc/
ls
```

2. Modify the imports in `all_tests.py` to import TimeSeries, ArrayTimeseries,
SimulatedTimeSeries according to the
file structure of the student repository. This might include changing the
directory name or file names or adding __init__ files or even the class names
might have to be changed.


3. Run it and save stdout and stderr appropriately.
```
python3 /run_tests.py > results/ecnc.txt 2>results/ecnc.err.log
```
