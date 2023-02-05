
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
    df_solution_all = pd.DataFrame(columns=['Instancia','Maquina Maior Custo','Maquina 2','MakeSpam','Tempo','Trocas','Trocas Aspiradas'])
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

        trocas_feitas_final = []
        trocas_feitas_aspiradas = []
        best = 0
        best_vidas = 0
        best_vidas2 = 0
        trocas_feitas = []
        trocas_05_percentual = []
        melhor_troca_resultados = []
        melhor_troca_troca = []
        best_50 = 0
        
        for changes in range(2000):
            list_maquinas = list(range(1,maquinas+1))
            
            i = df_solution.groupby('maquina')['value'].sum().idxmax()
            j = df_solution.groupby('maquina')['value'].sum().idxmin()
            
            
            while i==j:
           
                i = np.random.choice(df_solution.groupby('maquina')['value'].sum().index)
                j = np.random.choice(df_solution.groupby('maquina')['value'].sum().index)
             
            
            a = np.random.choice(df_solution[df_solution["maquina"]==i]['x'][1:])
            b = np.random.choice(df_solution[df_solution["maquina"]==j]['x'][1:])
            
            while a==b:
           
                a = np.random.choice(df_solution[df_solution["maquina"]==i]['x'][1:])
                b = np.random.choice(df_solution[df_solution["maquina"]==j]['x'][1:])
             
            tent = 0 
            
            '''
            
            while [a,b] in trocas_feitas:
                tent += 1
                print('Troca ja feita: ' +str([a,b]))
                a = np.random.choice(df_solution[df_solution["maquina"]==i]['x'][1:])
                b = np.random.choice(df_solution[df_solution["maquina"]==j]['x'][1:])
                print(tent)
                if  tent == 100: 
                    print('Nenhuma troca viavel')   
                    break
            '''
            

            if a in df_solution[df_solution["maquina"]==i]['x'].to_list() and b in df_solution[df_solution["maquina"]==j]['x'].to_list():

                df_solution_back = df_solution.copy()
                df_solution['y'] = np.where((df_solution['y'] == a) & (df_solution['maquina'] == i), b, df_solution['y'])
                df_solution['x'] = np.where((df_solution['x'] == a) & (df_solution['maquina'] == i), b, df_solution['x'])
                df_solution['y'] = np.where((df_solution['y'] == b) & (df_solution['maquina'] == j), a, df_solution['y'])
                df_solution['x'] = np.where((df_solution['x'] == b) & (df_solution['maquina'] == j), a, df_solution['x'])

                best += 1
                print('best: '+str(best))

                for y, infos in df_solution.iterrows():
                    df_solution['value'][y] = df_preparation.loc[infos['x'], infos['y']]

                if (df_solution.groupby('maquina')['value'].sum().max()  < (df_solution_troca_simples.groupby('maquina')['value'].sum().max()) and [a,b] not in trocas_feitas):
                    
                    df_solution_troca_simples = df_solution.copy()
                    print(df_solution_troca_simples.groupby('maquina')['value'].sum())
                    best = 0
                    trocas_feitas.append([a,b])
                    trocas_feitas_final.append([a,b])
                    best_vidas2 = best_vidas2 + 1
                    if best_vidas2 > 100:
                        del trocas_feitas[-1]
                    best_50 = 0
                
                elif (df_solution.groupby('maquina')['value'].sum().max()  < (df_solution_troca_simples.groupby('maquina')['value'].sum().max())*0.95 and [a,b] in trocas_feitas):
                    
                    df_solution_troca_simples = df_solution.copy()
                    print(df_solution_troca_simples.groupby('maquina')['value'].sum())
                    trocas_feitas_aspiradas.append([a,b])
                    best = 0
                    best_vidas2 = best_vidas2 + 1
                    if best_vidas2 > 100:
                        del trocas_feitas[0]
                    trocas_feitas.append([a,b])
                    trocas_05_percentual.append([a,b])
                    best_50 = 0
                
                else:

                    melhor_troca_resultados.append(df_solution.groupby('maquina')['value'].sum().max())
                    melhor_troca_troca.append([a,b,i,j])
                    #trocas_feitas.append([a,b])


                    best_vidas = best_vidas + 1
                    if best_vidas > 100:
                        del melhor_troca_resultados[0]
                        del melhor_troca_troca[0]
                        
                    if best != 100: df_solution = df_solution_back.copy()
                    
                    
                if best == 100:

                    print('\n------ 100 tentativas sem aprimoramento trocando para melhor opção -------\n')
                    #trocas_feitas.clear()
                    df_solution = df_solution_back.copy()
                    melhor = melhor_troca_resultados.index(min(melhor_troca_resultados))

                    a = melhor_troca_troca[melhor][0]
                    b = melhor_troca_troca[melhor][1]
                    i = melhor_troca_troca[melhor][2]
                    j = melhor_troca_troca[melhor][3]

                    df_solution['y'] = np.where((df_solution['y'] == a) & (df_solution['maquina'] == i), b, df_solution['y'])
                    df_solution['x'] = np.where((df_solution['x'] == a) & (df_solution['maquina'] == i), b, df_solution['x'])
                    df_solution['y'] = np.where((df_solution['y'] == b) & (df_solution['maquina'] == j), a, df_solution['y'])
                    df_solution['x'] = np.where((df_solution['x'] == b) & (df_solution['maquina'] == j), a, df_solution['x'])

                    #melhor_troca_resultados.clear()
                    #melhor_troca_troca.clear()

                    for i, infos in df_solution.iterrows():
                        df_solution['value'][i] = df_preparation.loc[infos['x'], infos['y']]
                    
                    df_solution_troca_simples = df_solution.copy()
                    print(df_solution_troca_simples.groupby('maquina')['value'].sum())
                    best = 0
                    best_50 += 1
                    trocas_feitas_final.append([a,b])

                #else: best_50 = 0♣

                if best_50 == 5:
                    print('Finalizando por 250 tentativa sem aprimoramento')
                    break


                for i, infos in df_solution.iterrows():
                    df_solution['value'][i] = df_preparation.loc[infos['x'], infos['y']]

                    #df_solution_all.loc[f] = [filename,df_solution_troca_simples.groupby('maquina')['value'].sum().max(),df_solution_troca_simples.groupby('maquina')['value'].sum()[2],df_solution_troca_simples.groupby('maquina')['value'].sum().sum(),convert(tempo)]
                    #print(df_solution_troca_simples.groupby('maquina')['value'].sum())
                    # break
                fim = time.time()
                tempo = fim - inicio
                #print(df_solution_troca_simples.groupby('maquina')['value'].sum())

        df_solution_all.loc[f] = [filename,df_solution_troca_simples.groupby('maquina')['value'].sum().max(),df_solution_troca_simples.groupby('maquina')['value'].sum()[2],df_solution_troca_simples.groupby('maquina')['value'].sum().sum(),convert(tempo),trocas_feitas_final.copy(),trocas_feitas_aspiradas.copy()]
        trocas_feitas_final.clear()
        trocas_feitas_aspiradas.clear()
        print(convert(tempo)) 