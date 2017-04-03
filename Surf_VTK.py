from __future__ import absolute_import, division, print_function
__author__ = 'Mostafa Hadavand'
__date__ = '2017-03-03'
__version__ = '1.00'



def Surafce_VTK(x,y,z,flname='Surface.vtk',fmt='%.5f'):

    '''
    A function to generate vtk format visualization for 3D surfaces based on triangulation
    '''

    from scipy.spatial import Delaunay
    import numpy as np
    import pandas as pd
    
    Input=np.concatenate((x, y), axis=1)
    TRIANG = Delaunay(Input)
    TRIANG=TRIANG.simplices.copy()
    
    nbpoint=len(x);
    
    if np.mod(nbpoint,3)==1:
        x=np.append(x,[0,0]);
        y=np.append(y,[0,0]);
        z=np.append(z,[0,0]);
    elif np.mod(nbpoint,3)==2:
        x=np.append(x,[0]);
        y=np.append(y,[0]);
        z=np.append(z,[0]);
        
    nbpoint=len(x);
    nTRIANG=len(TRIANG);
    with open(flname, 'w') as outfl:
        outfl.write('# vtk DataFile Version 3.0\n'
                    'vtk output\n'
                    'ASCII\n'
                    'DATASET POLYDATA\n');
        sTRIANGng='POINTS %d float\n'%nbpoint
        outfl.write(sTRIANGng);
        DF=pd.DataFrame()
        DF['X1']=x[:-2:3]
        DF['Y1']=y[:-2:3]
        DF['Z1']=z[:-2:3]
        
        DF['X2']=x[1:-1:3]
        DF['Y2']=y[1:-1:3]
        DF['Z2']=z[1:-1:3]
        
        DF['X3']=x[2::3]
        DF['Y3']=y[2::3]
        DF['Z3']=z[2::3]
        DF.to_csv(outfl, header=False, index=False, sep=' ',
                                           float_format=fmt)
        
        sTRIANGng='POLYGONS %d %d\n'%(nTRIANG,4*nTRIANG)
        outfl.write(sTRIANGng);
        A3=3*np.ones((len(TRIANG),1))
        TRIANG=np.append(A3,TRIANG,axis=1)
        DF=pd.DataFrame(data=TRIANG)
        DF.to_csv(outfl, header=False, index=False, sep=' ',
                                           float_format='%d')
    