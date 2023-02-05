
import numpy as np
import pandas as pd
from Extract import extract
from random import randint
import time
import os
import random
#print(randint(0,9))

def convert(seconds): 
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
      
    return "%d:%02d:%02d" % (hour, minutes, seconds) 

if __name__ == "__main__":
    
    directory = r'\instance'
    df_solution_all = pd.DataFrame(columns=['Instancia','Maquina Maior Custo','Maquina 2','MakeSpam','Tempo'])
    # iterate over files in
    # that directory
    file = 0
    for filename in os.listdir(directory):
        file += 1
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            print(f)
        maquinas, jobs, list_jobs1, df_preparation = extract(f)
        list_jobs = list(range(1,jobs+1))
        df_solution = pd.DataFrame(columns=['maquina','x','y','value'])
        list_jobs_unused = list_jobs.copy()
        # escolhe os primeiro job
        
        aux = 0 + maquinas
        inicio = time.time()
    
        for r in range(1, maquinas+1):
            
            df_solution.loc[r] = [r, maquinas+jobs-1, list_jobs[r-1], df_preparation.loc[maquinas+jobs-1,list_jobs[r-1]]]
            list_jobs_unused.remove(list_jobs[r-1])
    
        for jobs_un in list_jobs_unused:
            aux +=1
            maquina_less_used = df_solution.groupby('maquina')['value'].sum().idxmin()
            df_solution.loc[aux] = [maquina_less_used, df_solution[df_solution['maquina']==maquina_less_used]['y'].iat[-1], jobs_un, df_preparation.loc[df_solution[df_solution['maquina']==maquina_less_used]['y'].iat[-1], jobs_un]]
    
        for r in range(jobs+1, jobs+maquinas+1):
            aux +=1
            df_solution.loc[aux] = [r-jobs, df_solution[df_solution['maquina']==r-jobs]['y'].iat[-1], jobs+maquinas, df_preparation.loc[r-jobs,df_solution[df_solution['maquina']==r-jobs]['y'].iat[-1]]]
        
        #df_solution_all.loc[f] = [filename,df_solution_contrutivo.groupby('maquina')['value'].sum()[1],df_solution_contrutivo.groupby('maquina')['value'].sum()[2],df_solution_contrutivo.groupby('maquina')['value'].sum().sum(),convert(tempo)]

        df_solution_contrutivo = df_solution.copy()
        df_solution_troca_simples = df_solution.copy()
        fim = time.time()
        tempo = fim - inicio
        #df_solution_all.loc[f+'Contrutivo'] = [filename,df_solution_troca_simples.groupby('maquina')['value'].sum().max(),df_solution_contrutivo.groupby('maquina')['value'].sum()[2],df_solution_contrutivo.groupby('maquina')['value'].sum().sum(),convert(tempo)]

    
        best = 0
    
    
        for changes in range(5000):
            list_maquinas = list(range(1,maquinas+1))
            
            i = df_solution.groupby('maquina')['value'].sum().idxmax()
            j = df_solution.groupby('maquina')['value'].sum().idxmin()
            
            a = np.random.choice(df_solution[df_solution["maquina"]==i]['x'][1:])
            b = np.random.choice(df_solution[df_solution["maquina"]==j]['x'][1:])

            if a in df_solution[df_solution["maquina"]==i]['x'].to_list() and b in df_solution[df_solution["maquina"]==j]['x'].to_list():
                df_solution_back = df_solution.copy()
                df_solution['y'] = np.where((df_solution['y'] == a) & (df_solution['maquina'] == i), b, df_solution['y'])
                df_solution['x'] = np.where((df_solution['x'] == a) & (df_solution['maquina'] == i), b, df_solution['x'])
                df_solution['y'] = np.where((df_solution['y'] == b) & (df_solution['maquina'] == j), a, df_solution['y'])
                df_solution['x'] = np.where((df_solution['x'] == b) & (df_solution['maquina'] == j), a, df_solution['x'])

                best += 1
                
                for i, infos in df_solution.iterrows():
                    df_solution['value'][i] = df_preparation.loc[infos['x'], infos['y']]
                if (df_solution.groupby('maquina')['value'].sum().max()  < (df_solution_troca_simples.groupby('maquina')['value'].sum().max())):
                    df_solution_troca_simples = df_solution.copy()
                    print(df_solution_troca_simples.groupby('maquina')['value'].sum())
                    best = 0
                else:
                    df_solution = df_solution_back.copy()
                if best == 100:
                    print('\n------ 100 tentativas sem aprimoramento -------\n')
                  
                    df_solution_all.loc[f] = [filename,df_solution_troca_simples.groupby('maquina')['value'].sum().max(),df_solution_troca_simples.groupby('maquina')['value'].sum()[2],df_solution_troca_simples.groupby('maquina')['value'].sum().sum(),convert(tempo)]
                    break

                df_solution_all.loc[f] = [filename,df_solution_troca_simples.groupby('maquina')['value'].sum().max(),df_solution_troca_simples.groupby('maquina')['value'].sum()[2],df_solution_troca_simples.groupby('maquina')['value'].sum().sum(),convert(tempo)]
        fim = time.time()
        tempo = fim - inicio
        print(convert(tempo)) 