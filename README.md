Optimization approach to locate light pollution sensor in cities

It reproduces Figures 9-11 of the paper: Optimization of Sensor Locations for a Light Pollution Monitoring Network.

In this project you can verify the results at different levels. 

1. You can simply check the figures 9-11 of the paper in the folder ""
2. You can re-run the optimization process to reproduce the results given the influence regions maps or
3. Generate a project from the ground to redo the whole experiment from the region maps. 


For the option 1 go to folder /reports/figures
For the option 2 and 3 you need to setup a python 3 environment.

1. Create an virtualenv
2. Install the required packages
3. go to the root folder and run python scripts 1, 2 and 3
4. Verify the results in the folder reproduce. 

Project Organization
--------------------

```

.
├── AUTHORS.md
├── LICENSE
├── README.md
├── config
│   ├── __pycache__
│   │   └── config.cpython-39.pyc
│   └── config.py
├── data
│   └── locations
│       └── queretaro
│           ├── prioridades
│           └── qro_light_th
├── experiments
│   ├── paper_experiment
│   │   ├── reproduce_paper_experiment.txt
│   │   ├── results
│   │   │   ├── Figure_11.pdf
│   │   │   ├── figure_09.pdf
│   │   │   ├── figure_10.pdf
│   │   │   ├── optimum_arguments.csv
│   │   │   └── optimum_values.csv
│   │   └── semivariances
│   │       ├── semivariance050512022.csv
│   │       └── semivariance050512022mask.csv
│   ├── reproduce_paper_experiment.txt
│   └── reproduce_paper_experiment_2.txt
├── intructions.md
├── notebooks
│   ├── Example ploting with rasterio.ipynb
│   ├── paso1_construir_base_de_datos_semivarianza.ipynb
│   ├── paso2_lightPollexperiments.py
│   ├── paso3_resultados.ipynb
├── reproduce
│   ├── 01_precalculate_regions_of_influence.py
│   ├── 03_generate_figures.py
│   └── paso2_lightPollexperiments.py
├── requirements.txt
└── src
    ├── __pycache__
    ├── manageExperiments.py
    ├── network_fitness.py
    ├── positioning_sensors.py
    └── regionGrowing.py
```

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

```
zation_sensor_locations_results/reproduce$ neofetch
            .-/+oossssoo+/-.               rlopez3@cgeoqro 
        `:+ssssssssssssssssss+:`           --------------- 
      -+ssssssssssssssssssyyssss+-         OS: Ubuntu 20.04.4 LTS x86_64 
    .ossssssssssssssssssdMMMNysssso.       Host: OpenStack Nova 24.0.0 
   /ssssssssssshdmmNNmmyNMMMMhssssss/      Kernel: 5.4.0-132-generic 
  +ssssssssshmydMMMMMMMNddddyssssssss+     Uptime: 114 days, 18 hours, 4 mins 
 /sssssssshNMMMyhhyyyyhmNMMMNhssssssss/    Packages: 2293 (dpkg), 4 (snap) 
.ssssssssdMMMNhsssssssssshNMMMdssssssss.   Shell: bash 5.0.17 
+sssshhhyNMMNyssssssssssssyNMMMysssssss+   Terminal: /dev/pts/3 
ossyNMMMNyMMhsssssssssssssshmmmhssssssso   CPU: Intel Xeon (Cascadelake) (16) @ 
ossyNMMMNyMMhsssssssssssssshmmmhssssssso   GPU: 00:02.0 Red Hat, Inc. QXL parav 
+sssshhhyNMMNyssssssssssssyNMMMysssssss+   Memory: 7739MiB / 32110MiB 
.ssssssssdMMMNhsssssssssshNMMMdssssssss.
 /sssssssshNMMMyhhyyyyhdNMMMNhssssssss/                            
  +sssssssssdmydMMMMMMMMddddyssssssss+                             
   /ssssssssssshdmNNNNmyNMMMMhssssss/
    .ossssssssssssssssssdMMMNysssso.
      -+sssssssssssssssssyyyssss+-
        `:+ssssssssssssssssss+:`
            .-/+oossssoo+/-.
```

