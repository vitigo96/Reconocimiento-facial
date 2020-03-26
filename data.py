import numpy as np
import pandas as pd
import math
import matplotlib
from scipy.stats import variation  


def broadcasting_array(a, L, S):  # Window len = L, Stride len/stepsize = S
    nrows = ((a.shape[0]-L)//S)+1
    return a[S*np.arange(nrows)[:,None] + np.arange(L)]


def preprocessing(data_df, columns, m = 5, S=1, N = 5, niter = 100, kappa = 35, gamma = 0.15):

    dim_col = len(columns)

    median_df = median_filter(data_df, columns=columns, m = m, S=S)
    med_mcv_an_df = anisodiff(median_df, niter=niter,kappa=kappa,gamma=gamma,step=(1.,1.),option=1,ploton=False)

    return med_mcv_an_df


def median_filter(data_df, columns, m = 5, S=1):

    dim_col = len(columns)
    data_array = np.array(data_df[columns])
    #median_array = np.zeros((len(data_df),dim_col))
    median_array = data_array
    broad =  broadcasting_array(data_array, L=m, S=S)
    median_array[m//2:-m//2+1]=np.median(broad, axis=1)
    mediandf = pd.DataFrame(median_array, index= data_df.index, columns= columns)

    return mediandf

def MCV(data_df, N, columns, n = 4, S=1):

    data_array = np.array(data_df[columns])
    mcv_array = data_array.copy()
    c = data_array.copy()
    c1 = data_array.copy()
    c1index = np.array([[i,i] for i in range(len(data_array))])
    average = data_array.copy()

    broad =  broadcasting_array(data_array, L=N+2, S=S)
    c[math.ceil(N/2):-math.ceil(N/2)]=np.array(variation(broad, axis = 1)) #luego se itera para reemplazar los primeros y últimos según los demás parámetros

    '''
    N: posición en la que se identifica el transiente en real_time_disag
    el número de posiciones fijas debe ser mayor a en las que calcula el c1 index para que no se estanque el dataframe y pueda propagarse
    Esto es, c1 y c1index deben estar en otro ciclo
    '''
    
    for i in range(0,len(data_df)):

        if (i < n) or (i > (len(data_df)- (math.ceil(N/2)) -1)): 
            c[i] =  np.fabs(data_df[columns].iloc[i]) + 10 #para asegurarse que estas posiciones nunca tengan el menor coeficiente de variación

        if (i < n) or (i >= (len(data_df)- (2*math.ceil(N/2)) -1)): #El límite superior es para asegurar propagación de la variable
            mcv_array[i] =  data_df[columns].iloc[i]
            #v = data_df[columns].iloc[i]
            c1[i] =  c[i]
            c1index[i] =i  
            average[i] =  data_df[columns].iloc[i]
   
    broad_c =  broadcasting_array(c, L=N+2, S=S)

    c1[math.ceil(N/2):-math.ceil(N/2)] = np.min(broad_c, axis = 1) 
    c1index[math.ceil(N/2):-math.ceil(N/2)] = -(math.ceil(N/2)) + np.argmin(broad_c, axis = 1)

    for i in range(N//2,len(data_df)-math.ceil(N/2)+1):
        c1index[i] = i + c1index[i] 
    
    for i in range(0,n): #restaurar hasta n valores anteriores  
        c[i] =  np.fabs(data_df[columns].iloc[i]) + 10 #para asegurarse que estas posiciones nunca tengan el menos coeficiente de variación 
        c1[i] =  c[i]
        c1index[i] =i  
    
    for i in range(len(data_df)- (math.ceil(N/2)) ,len(data_df)): 
        c1[i] =  c[i]
        c1index[i] =i  

    broad_c1index =  broadcasting_array(c1index, L=N+2, S=S)
    data_broadcast = [data_array[[int(broad_c1index[j][i][0]) for i in range(N+2)]] for j in range(len(broad_c1index))]
    average[math.ceil(N/2):-math.ceil(N/2)] = np.median(data_broadcast, axis = 1)

    for i in range(0, n): #restaurar hasta n valores anteriores
        average[i] =  data_df[columns].iloc[i]

    for i in range(len(data_df)- (2*math.ceil(N/2)) -1,len(data_df)): 
        average[i] =  data_df[columns].iloc[i] 
    
    df = pd.DataFrame(average, index= data_df.index, columns= columns)

    return df



def anisodiff(img,niter=1,kappa=50,gamma=0.1,step=(1.,1.),option=1,ploton=False):
        """
        Anisotropic diffusion.
 
        Usage:
        imgout = anisodiff(im, niter, kappa, gamma, option)
 
        Arguments:
                img    - input image
                niter  - number of iterations
                kappa  - conduction coefficient 20-100 ?
                gamma  - max value of .25 for stability
                step   - tuple, the distance between adjacent pixels in (y,x)
                option - 1 Perona Malik diffusion equation No 1
                         2 Perona Malik diffusion equation No 2
                ploton - if True, the image will be plotted on every iteration
 
        Returns:
                imgout   - diffused image.
 
        kappa controls conduction as a function of gradient.  If kappa is low
        small intensity gradients are able to block conduction and hence diffusion
        across step edges.  A large value reduces the influence of intensity
        gradients on conduction.
 
        gamma controls speed of diffusion (you usually want it at a maximum of
        0.25)
 
        step is used to scale the gradients in case the spacing between adjacent
        pixels differs in the x and y axes
 
        Diffusion equation 1 favours high contrast edges over low contrast ones.
        Diffusion equation 2 favours wide regions over smaller ones.
        """
 
        # initialize output array
        img = img.astype('float32')
        imgout = img.copy()
 
        # initialize some internal variables
        deltaS = np.zeros_like(imgout)
        deltaE = deltaS.copy()
        NS = deltaS.copy()
        EW = deltaS.copy()
        gS = np.ones_like(imgout)
        gE = gS.copy()
 
        # create the plot figure, if requested
        if ploton:
                import pylab as pl
                from time import sleep
 
                fig = pl.figure(figsize=(20,5.5),num="Anisotropic diffusion")
                ax1,ax2 = fig.add_subplot(1,2,1),fig.add_subplot(1,2,2)
 
                ax1.imshow(img,interpolation='nearest')
                ih = ax2.imshow(imgout,interpolation='nearest',animated=True)
                ax1.set_title("Original image")
                ax2.set_title("Iteration 0")
 
                fig.canvas.draw()
 
        for ii in range(niter):

                # calculate the diffs
                deltaS[:-1] = np.diff(imgout,axis=0)
        #        deltaE[:-1] = np.diff(imgout_ex,axis=1)

                # conduction gradients (only need to compute one per dim!)
                if option == 1:
                        gS = np.exp(-(deltaS/kappa)**2.)/step[0]
        #                gE = np.exp(-(deltaE/kappa)**2.)/step[1]
                elif option == 2:
                        gS = 1./(1.+(deltaS/kappa)**2.)/step[0]
        #                gE = 1./(1.+(deltaE/kappa)**2.)/step[1]

                # update matrices
        #        E = gE*deltaE
                S = gS*deltaS

                # subtract a copy that has been shifted 'North/West' by one
                # pixel. don't as questions. just do it. trust me.
                NS[:] = S
        #        EW[:] = E
                NS[1:] -= S[:-1]
        #        EW[:,1:] -= E[:,:-1]

                # update the image
                imgout += gamma*(NS)

                if ploton:
                        iterstring = "Iteration %i" %(ii+1)
                        ih.set_data(imgout)
                        ax2.set_title(iterstring)
                        fig.canvas.draw()
                        # sleep(0.01)

        return imgout