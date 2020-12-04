# SBSE_project
### How to get gcov from the subject programs
1. Download the subject programs in https://sir.csc.ncsu.edu/php/index.php (You need to register for download, and make sure to download **linux** version if you use linux), and mts file (You can find it in "Download Tools" tab)
2. Delete all the contents in `<program_name>/source`
3. Copy the contents from `<program_name>/versions.alt/versions.seeded/<version>` to `<program_name>/source`
4. Delete the comments in `FaultSeeds.h` to put the fault in the program.
5. Compile the program with parameters **-fprofile-arcs -ftest-coverage** (You may need **-std=c11** for newer versions)
6. Copy the mts file from `mts/bin/bsh/mts` to `<program_name>/source` (Note that you have to add/modify the MTS_PATH and CLASSPATH in mts file. Specifically, MTS_PATH refers to the `mts` folder, and CLASSPATH refers to `mts/bin` folder)
7. Make test scripts via `./mts .. ./<program_name.exe> ../testplans.alt/<version>/<universe file> R test.sh NULL NULL` (For specific command explanation, https://sir.csc.ncsu.edu/content/mts-usage.php provides firm usage explanation) (Also note that this command is run from the inside of `source` directory)
8. Modify test scripts to generate code coverage information for each test cases(`sed -i 's/> ..\/ou/;gcov -i *.c/g ' test.sh`, `sed -i 's/tputs\//;mv sed.c.gcov ..\/outputs\//g' test.sh`, `sed -i 's/2>\&1//g' test.sh`)
9. Run the program (`./test.sh`)
10. You can see the code coverage information in `<program_name>/outputs`
