import numpy as np
import pandas as pd

def extract(file):
    
    list_jobs = []
    list_preparation = []
    f = open(file, 'r')
    maquinas = int(f.readline())
    jobs = int(f.readline())
    for j in range(jobs):
        list_jobs.append(int(f.readline()))
    for j in range(maquinas):
        f.readline()
    for j in range(((jobs+maquinas)*(jobs+maquinas))):
        list_preparation.append(int(f.readline()))
    array_prepartion = np.array(list_preparation)
    array_prepartion = np.reshape(array_prepartion,(jobs+maquinas,jobs+maquinas))
    df_preparation = pd.DataFrame(array_prepartion)
    df_preparation.index += 1
    df_preparation.columns += 1
    for i in df_preparation.columns: 
        if i in range(jobs+1):
            df_preparation[i] = df_preparation[i] + list_jobs[i-1]

    return maquinas, jobs, list_jobs, df_preparation