There are 3 main modes of operation, specified by command line parameters.
There is a configuration in the form of a Python dictionary that is passed to the Robot class constructor. This configuration comes from different sources depending on the mode of operation.

main.py is in the client folder.

---

python3 main.py

This was meant to be the default operation when the project was first started. It was going to be each robot simulator running on a different computer so that networking options could be explored more. But the project took a different direction and this mode is not as useful any more. Now it is used for seeing 1 single robot explore 1 map. In this mode, you can press enter for each step of robot movement.

The configuration for this mode is read from config.txt

---

python3 main.py 1
python3 main.py 2

Since we didn't set up multiple computers to work together, this mode of operation is for seeing 2 robots explore 1 map. It is to be run in 2 different consoles, started at close to the same time.

The configuration for this mode comes from main.py under DEMO_OPTIONS

---

python3 main.py d

This is the mode used to collect lots of data automatically. It will print a list of all of the samples at the end of each map. It has to run for a few hours to collect a good amount of data.

The configurations for this mode are iteratively generated in main.py data_gather_sequence and one_set

---

obstacle probability is a static member of the EnvironmentSimulator class
