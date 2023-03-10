Optimization approach to locate light pollution sensor in cities

It reproduces Figures 9-11 of the paper: Optimization of Sensor Locations for a Light Pollution Monitoring Network

Project Organization
--------------------

    .
    ├── AUTHORS.md
    ├── LICENSE
    ├── README.md
    ├── bin
    ├── config
    ├── data
    │   ├── external
    │   ├── interim
    │   ├── processed
    │   └── raw
    ├── docs
    ├── notebooks
    ├── reports
    │   └── figures
    └── src
        ├── data
        ├── external
        ├── models
        ├── tools
        └── visualization


Instructions:

Proved with python 3.9.13

0. Generate a virtual env.
1. Cd to virtual env
2. git clone https://github.com/rdglpz/reproduce_optimization_sensor_locations_results.git
3. Install the requirements

Screen -S experiment
$python experiment/python 01_precalculate_regions_of_influence.py
Ctrl + a + d
$ screen -r experiment (r of reattach)


Technical References
https://medium.com/swlh/how-to-use-screen-on-linux-to-detach-and-reattach-your-terminal-2f52755ff45e

https://docs.python.org/3/library/venv.html
https://www.freecodecamp.org/news/manage-multiple-python-versions-and-virtual-environments-venv-pyenv-pyvenv-a29fb00c296f/



