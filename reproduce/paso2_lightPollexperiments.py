#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 27 22:15:13 2022

@author: rodrigo
"""

#Cargando librerías 
import importlib

import matplotlib.pyplot as plt
import scipy as sp
import numpy as np
import pandas as pd
import os
import sys  

root = os.getcwd() + "/.."

sys.path.insert(0, root)

import src.positioning_sensors as ps
importlib.reload(ps)

import src.network_fitness as netfit
importlib.reload(netfit)

import src.manageExperiments as me
importlib.reload(me)

import config.config as cfg
importlib.reload(cfg)

from geneticalgorithm import geneticalgorithm as ga

import itertools as it

#read_global_variables

plt.style.use("ggplot")

setup = me.readConfigFile("config_exp_15062022_redo_exp.txt")


#cargamos imagenes en luminance e importance
ilumina = setup["folder_input"]+setup["input_ntli"]
niveles = setup["folder_input"]+setup["input_evm"]
sigma_y = setup['filterg_sy']
sigma_x =setup['filterg_sx']
sigma = [sigma_y,sigma_x]

#Loading precalculated local and directed empirical variograms
path2output_semivars = (cfg.experiment 
          + setup["experiment_id"]
          + setup["folder_semivariances"]
          + setup["output_semivariances"] 
                       )


filesv = path2output_semivars + ".csv"
filesvmask = path2output_semivars + "mask.csv"

path2optimum_values_file = (cfg.experiment 
                           + setup["experiment_id"] 
                           + setup["folder_output"] 
                           )

saveOptimumValuesTofile = (path2optimum_values_file
                           + setup["output_values"]
                          )

saveArgsTofile = (path2optimum_values_file
                  + setup["output_args"]
                 )

data = pd.read_csv(filesv)
data_m = pd.read_csv(filesvmask)
variogram_set = np.array(data.iloc[:,3:])
variogram_set_m = np.array(data_m.iloc[:,3:])


#NLTI: luminance
luminance = ps.readIMG(cfg.data + ilumina)

#EAM: Environtmental attention map is the importance
EAM = ps.readIMG(cfg.data + niveles, invert = True)




nonsat,b = ps.desaturate(luminance, th = setup["desaturation_th"])

variograms = variogram_set.reshape(len(variogram_set),nonsat.shape[0],nonsat.shape[1])
variograms_m = variogram_set_m.reshape(len(variogram_set),nonsat.shape[0],nonsat.shape[1])

coords = np.array(data.iloc[:,1:3])

#nonsat2 = sp.ndimage.filters.gaussian_filter(nonsat, sigma, mode='constant')
#nonsat2 = (nonsat2>=22)*nonsat2

NLTI = sp.ndimage.filters.gaussian_filter(nonsat, sigma, mode = 'constant')
NLTI = (NLTI>=setup["neglect_values"])*NLTI



#sensitivity = ps.f5(NLTI,EAM,2)
from IPython.display import clear_output

r2 = list([])
results2 = list([])




allc = setup["sensitivity_c"]
alls = setup["nsensors"]

for i in it.product(allc, alls):
    
    
    clear_output(wait = False)
    c = i[0]
    n_sensors = i[1]
    print(i)
    
    
    sensitivity = ps.f5(NLTI,EAM,c)
    aptitude = netfit.NetworkFitness(NLTI,
                                     EAM, 
                                     sensitivity, 
                                     variograms, 
                                     variograms_m,
                                     coords)
    
    aptitude.selectFitnessFunction("max")
    f = aptitude.f



    #variable ranges, 2 ranges per sensor position (dim*n_sensors) 
    varbound=np.array([[0, nonsat.shape[0]], [0, nonsat.shape[1]]]*n_sensors)
    print("Search Space Boundaries:", varbound)

    dim = len(varbound)

    #algorithms_parameters={'max_num_iteration': None, 'population_size': 500, 'mutation_probability': 0.1, 'elit_ratio': 0.01, 'crossover_probability': 0.5, 'parents_portion': 0.3, 'crossover_type': 'uniform', 'max_iteration_without_improv': None}
#    algorithm_parameters={'max_num_iteration': 1, 'population_size': 2000, 'mutation_probability': 0.1, 'elit_ratio': 0.1, 'crossover_probability': 0.5, 'parents_portion': 0.3, 'crossover_type': 'uniform', 'max_iteration_without_improv': 500}
    algorithm_parameters = setup["ga_params"]
    model=ga(function = f,
             dimension = dim,
             algorithm_parameters = algorithm_parameters,
             variable_type = 'int',
             variable_boundaries = varbound,
             convergence_curve = False)

    
    
    model.run()
    r2.append(model.output_dict["function"])
    results2.append(model.output_dict["variable"])
    
    res_df= pd.DataFrame(results2)
    res_df.to_csv(saveOptimumValuesTofile)

    res_df= pd.DataFrame(r2)
    res_df.to_csv(saveArgsTofile)
    
#res_read = pd.read_csv("results_7x7.csv")

#{"experiment_id": "exp_050512022_consider_flat/", "folder_input": "location/queretaro/", "folder_semivariances": "semivariances/", "folder_output": "results", "input_ntli": "qro_light_th", "input_evm": "prioridades", "output_semivariances": "semivariance050512022", "output_values": "optimum_values", "output_args": "optimum_arguments", "desaturation_th": 63,"neglect_values":22 ,"tolerance_distance": 0.5, "tolerance_angle": 15, "filterg_sx": 0.5, "filterg_sy": 0.5, "gaussian_mode": "constant", "nsensors": [1, 2, 3, 4, 5, 6, 7], "sensitivity_c": [1, 30, 60, 90, 120, 150, 180]}