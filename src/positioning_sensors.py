import numpy as np
import matplotlib.pyplot as plt
#from matplotlib_scalebar.scalebar import ScaleBar
from scipy import ndimage as ndi
from skimage.segmentation import watershed
from PIL import Image
from IPython.display import display, clear_output

import importlib
import os
import sys
import config.config as cfg

root = os.getcwd() + "/.."
sys.path.insert(0, root)

import config.config as cfg
importlib.reload(cfg)


def f5(i,p,e=4):
    '''
    Pesos exponenciales
    
    W = i*a^(p-r)
    '''
    print(" W = i*a^(p)")
    return i*e**(p)



def getN(W,i,j):
    
    ln = ([])
    
#    c = W[i,j]
    
    ln.append(W[i+1,j])
    ln.append(W[i-1,j])
    ln.append(W[i-1,j-1])
    ln.append(W[i-1,j+1])
    ln.append(W[i+1,j+1])
    ln.append(W[i+1,j-1])
    ln.append(W[i,j+1])
    ln.append(W[i,j-1])
    
    opt = False if W[i,j]<max(ln) else True
    
    return opt



    

def get_coords(seeds):
    coords = np.array([[0,0]])
    for i in range(0,seeds.shape[0]):
        for j in range(0,seeds.shape[1]):
            if seeds[i,j]!=0:
                coords = np.append(coords,[[i,j]],axis=0)
                
        
    return coords[1:]

def makeSpatialScatter(pc,mask,img):
    """
    pc: the centroid
    mask: pixels of interet, 
    img nlt image
    
    returns [distance,variance]
    """

    i = j = 0
    
    p = np.array([i,j])
    d = np.linalg.norm(pc-pc)
    v = (img[pc[0],pc[1]]-img[pc[0],pc[1]])**2

    ls = np.array([[d,v]])
    
    for i in range(1,img.shape[0]):
        for j in range(1,img.shape[1]):
            if mask[i][j]==1:
                p = np.array([i,j])

                d = np.linalg.norm(p-pc)
                
                v = (img[p[0],p[1]]-img[pc[0],pc[1]])**2
        
                ls = np.append(ls,[[d,v]],axis = 0)
 
  
                
    return ls

def variogram(sc,h=30):
    """
    sc: spatial scatter
    
    """
    if np.array(sc).shape[0] > 0:
    
        variogram = np.array([])
        for h in range(1,h):
    
       
            ix = (sc[:,0]>(h-0.5))*(sc[:,0]<=(h+0.5))
            n = np.sum(ix)

            
            if n > 0:
                v = np.sum(sc[ix,1])
                g = v/(2*n)
                variogram = np.append(variogram,g)
            else:
                variogram = np.append(variogram,0)
    else:
        variogram = range(1,h)
    
    return variogram


def getMax(img):
    B = np.zeros(img.shape)
    for i in range(1,B.shape[0]-1):
        for j in range(1,B.shape[1]-1):
            B[i][j] = getN(img,i,j)
    
    positionsB = B*(img>0)
    locationsP = np.zeros(img.shape)
    for i in range(0,img.shape[0]):
        for j in range(0,img.shape[1]):
            locationsP[i][j] = 1 if positionsB[i][j]==1 else 0
            
    return locationsP

def waterShedRegions(S,C):
    """
    S: Seeds
    C: Coordinates
    """
    
    mask = np.zeros(S.shape, dtype=bool)
    #we set to 1 all the coordinates C in the mask
    mask[tuple(C.T)] = True

    markers, _ = ndi.label(mask)
    labels = watershed(-S, markers, mask=S)
    
    L = np.zeros((len(C),S.shape[0],S.shape[1]))
    
    for i in range(len(L)):
        c = C[i]
        L[i] = (labels == labels[c[0]][c[1]])
    
    return L

def getMaximumVariance(S,th):
    """
    th ={0,100}
    """
    S_flatten = S.flatten()
    vmax = np.max(S_flatten)
    vmin = np.min(S_flatten)
    vrange = (vmax-vmin)**2/2
    max_var = th * vrange/100
    return max_var

def getOrientationMaskII(si,sj,atol,Img):
    """
    atol: angle tolerance
    """
    
    # area constrained by angle
    A = np.zeros(Img.shape)
    angle = ps.angle(si,sj)
    angleinf = (angle-atol)
    anglesup = (angle+atol)
    
    for i in range(nonsat.shape[0]):
        for j in range(nonsat.shape[1]):
            
            #sk is the test coordinate. is the sk point inside the cone?
            sk = np.array([i,j])
            
            
            #probar este angulo si esta en el cono
            # b va de 0 a 359.999 
            #is the angle of interest?
            anglek = ps.angle(si,sk)
            
            # correction if angleinf is <0, the anglek are in [0,360)
            if angleinf < 0 and ((anglek > (angleinf%360)) or (anglek<anglesup)) :
                A[i][j] = 1
                    
            if anglesup>=360 and ((anglek > angleinf) or (anglek<(anglesup%360))) :
#                anglesupp = anglesup%360
#                if (anglek > angleinf) or (anglek<(anglesup%360)):

                A[i][j] = 1          
            if (anglek<anglesup) and (anglek>angleinf):
                A[i][j] = 1
    
    return A

def getOrientationMask(d,dtol,S,dx,dy):
    """
    d: direction in grads (0-360)
    dtol: direction tolerance (range) in angle
    S: is a matrix
    """

    gm1 = d-dtol
    gm2 = d+dtol
    m1 = np.tan(np.radians(gm1))
    m2 = np.tan(np.radians(gm2))
    
    print(m1,m2)
    
    setA = np.zeros(S.shape)
    setB = np.zeros(S.shape)
    
    for y in range(S.shape[0]):
        for x in range(S.shape[1]):

            #if angle is in right or left side
            if gm1<90 or gm1>90*3:
                setA[y][x] = 1 if m1*(x-dx)+dy-y <0 else 0
            else:
                setA[y][x] = 0 if m1*(x-dx)+dy-y <0 else 1

            if gm2<90 or gm2>90*3:
                setB[y][x] = 0 if m2*(x-dx)+dy-y <0 else 1
            else:
                setB[y][x] = 1 if m2*(x-dx)+dy-y < 0 else 0

    return setA*setB

def angle(si,sj):
    
    s0 = si-si
    sja = sj-si
#    print(s0)
#    print(sja)
    
    dy =  sja[0]-s0[0]
    dx =  sja[1]-s0[1]
    
    
    if dx!=0 and dy!=0:
        m1= dy/dx
        if dy > 0 and dx > 0:
            
            r = np.rad2deg(np.arctan(m1))

        if dy > 0 and dx < 0:
  
            r = 180+np.rad2deg(np.arctan(m1))

        if dy<=0 and dx < 0:

            r = np.rad2deg(np.arctan(m1))+180

        if dy<=0 and dx > 0:

            r = 360+np.rad2deg(np.arctan(m1))
    
    
    if dy == 0 and dx >0:
        r = 90*0
        
    if dy>0 and dx == 0:
        r = 90*1
        
    if dy == 0 and dx < 0:
        r = 90*2
        
    if dx == 0 and dy < 0:
        r = 90*3
        
    if dx == 0 and dy == 0:
        r = 0
        
    return r
    


    
def getMaxRadio(ac,mv):
    """
    Obtenemos el radio maximo que satisface la maxima varianza (mv) permitida
    dado el acumulado de la varianza en funcion de la distancia
    """
    
    bs = ac <= mv
     
    
    
    nf = np.where(bs==False)

    
    if len(nf[0])>0:
        bs[nf[0][0]:] = False
        radio = np.sum(bs)
    else:
        radio = len(bs)
        
    return radio
                
                

def fillArea(p,accum,radio,direction,mshape):
    emptyZ = np.zeros(mshape)
    emptyMZ = np.zeros(mshape)
    
    dy = p[0]
    dx = p[1]
    
    for r in np.arange(0,radio,0.1):
                    
        #asumiendo que el angulo está centrado en el origen calculamos las coordenadas (y,x) dado la direccon dado por el ángulo en radianes y el tamaño del radio
        y = np.int(np.round(r*np.sin(np.radians(direction))))
        x = np.int(np.round(r*np.cos(np.radians(direction))))

        #we take care of the positive squared boundaries
        #trasladamos las coordenadas a su posición original            
        py = dy+y
        px = dx+x
                
        #validamos que (py,px) estén dentro de los limites de la matriz        
        if py>=mshape[0]:
            py = mshape[0]-1
        elif py < 0 :
            py = 0
                        
        if px>=mshape[1]:
            px = mshape[1]-1
        elif px < 0 :
            px = 0
                    
    
        emptyZ[py,px] = accum[int(r)]
        emptyMZ[py,px] = 1
        
    return emptyZ,emptyMZ
    
    

def computeRegions(S,coords,th = 0.6, atol=30, direction_delta = 2,verbose=False):
    """
    S: NLTI  map
    coords: maximum points
    th: valid variannce in %
    atol = angle tolerance 
    direction_delta: angle steps
    verbose: show prints
    """
    
    max_var = getMaximumVariance(S,th)

    setC = np.zeros((len(coords),S.shape[0],S.shape[1]))
    
    z    = np.zeros((len(coords),S.shape[0],S.shape[1]))
    mz   = np.zeros((len(coords),S.shape[0],S.shape[1]))
    
    for i,c in enumerate(coords):
        clear_output(wait=True)
        display( "{:.2f}%".format(100*(i/len(coords))) )
        if verbose == True: print("Coords ", c)
    
        dy = c[0]
        dx = c[1]

        for direction in range(0,360,direction_delta):
            
        
            mask = getOrientationMask(direction,atol,S,dx,dy)

            p = np.array([dy,dx])
            
            sc = makeSpatialScatter(p,mask,S)
            accum = variogram(sc)
            

            # detectamos hasta que indice se cumple el requerimiento de la varianza
            #getVar
            
            # lo primero que se cumpla, rebasa la toleracia de la varianza o encuentre un maximo
            accum = np.append([0],accum)
            radio = getMaxRadio(accum,max_var)  
            
            
            args = np.where((accum[1:]-accum[:-1])<=0)
            radio_first_local_max = radio+1
            
            if len(args[0])>0:
                radio_first_local_max = args[0][0]+1
            
            #print(direction,radio,radio_first_local_max)
            radio = np.min([radio,radio_first_local_max])
           
            
            
            z_aux    = np.zeros((S.shape[0],S.shape[1]))
            mz_aux   = np.zeros((S.shape[0],S.shape[1]))
            
            a_aux, mz_aux = fillArea(p,accum,radio,direction,S.shape)
            
            xor_mask = np.logical_xor(a_aux,mz[i])

            mz[i]+= xor_mask*a_aux
            z[i] += z_aux
            
            #mz[i] += mz_aux
        
        setC[i][c[0]][c[1]]=1
        
        #use a mask to point out that the 0 is for 0 variance associated to the sensor locations
        mz[i][c[0]][c[1]]=0.000000000001
        
        if verbose == True: print("--")
    
    return z,mz,setC
    

    

def readIMG(img, invert = False, null = 255):
    
    
    im1 = np.array(Image.open(cfg.data + img))
    
    if invert == False:
        im1 = np.array(Image.open(cfg.data + img))
        im1 = np.where(im1==null, 0, im1) 
    #    print("categories:", set(im1.flatten()))
    else:
        
        nc = 5
        P = np.where(np.isnan(im1),nc, im1)-1 
        im1 = P.max()-P

    return im1

def plotMasks(mask,L,W):
    ngrid = np.int32(np.ceil(np.sqrt(len(mask))))
    fig, axs = plt.subplots(ngrid, ngrid,figsize = (30,30))
    c=0
    for i in range(ngrid):
        for j in range(ngrid):
            if i * ngrid + j < len(mask):
                axs[i, j].imshow(mask[c])
                axs[i, j].set_title("w: {:.1f}, c {}".format(np.sum(mask[c]*W*L[c]),str(coords[c])))
                c+=1
    plt.show()
    
    
def desaturate(img,th=62):
    
    #B: binary image of the saturated region
    B = img>=th
    
    #T
    T = ndi.distance_transform_edt(B)
    nonsat = img+T
    return [nonsat,T]


def saveRegions(varmask,locations,name = "allcoversnonsatat15percent.csv"):
    
    #flattenizing

    fvm = [varmask[i].flatten() for i in range(len(varmask))]
    df = pd.DataFrame(fvm)
    
    c  = np.array([ps.get_coords(locations[i]) for i in range(len(locations)) ])
    cf = c.flatten()
    coords = cf.reshape(len(locations),2)
    df.insert(0,"coordsy", coords[:,0])
    df.insert(1,"coordsx", coords[:,1])
    df.to_csv(name)
    
#def readRegions(name):


def gom(si,sj,atol,Img):
    """
    gom: get orienttion mask
    atol: angle tolerance
    """
    
    # area constrained by angle
    A = np.zeros(Img.shape)
    ang = angle(si,sj)
    angleinf = (ang-atol)
    anglesup = (ang+atol)
    
    # en vez de recorrer toda la imagen, usar crecimiento de regiones inicializado en si
    # considerar si los vecinos sk;
    # 1) están dentro de angle inf y angle sup
    for i in range(Img.shape[0]):
        for j in range(Img.shape[1]):
            
            #sk is the test coordinate. is the sk point inside the cone?
            sk = np.array([i,j])
            
            
            #probar este angulo si esta en el cono
            # b va de 0 a 359.999 
            #is the angle of interest?
            anglek = angle(si,sk)
            
            # correction if angleinf is <0, the anglek are in [0,360)
            
            s1 =  (angleinf < 0) and ((anglek > (angleinf%360)) or (anglek<anglesup))
            s2 = (anglesup>=360 and ((anglek > angleinf) or (anglek<(anglesup%360))))
            s3 = (anglek<anglesup) and (anglek>angleinf)
            
            
#            if (angleinf < 0) and ((anglek > (angleinf%360)) or (anglek<anglesup)) :
#                A[i][j] = 1
                    
#            if anglesup>=360 and ((anglek > angleinf) or (anglek<(anglesup%360))) :
#                A[i][j] = 1   
                
#            if (anglek<anglesup) and (anglek>angleinf):
#                A[i][j] = 1
                

            #if (s1 or s2 or s3) and (d(sk,si) inside the range): 
            #    A[i][j] = 1
            
            if (s1 or s2 or s3):
                A[i][j] = 1
    
    return A

def gom_growing(si,sj,atol,Img):
    # area constrained by angle
    A = np.zeros(Img.shape)
    ang = angle(si,sj)
    angleinf = (ang-atol)
    anglesup = (ang+atol)
    
    d = np.sum((si-sj)**2)**(1/2)
    
    print(t)
    #Img = self.Img
    #1) pila que recuerda las celdas por visitar
    self.stack = []
        
    #2) matriz que marca las celdas visitadas
    visit = np.zeros(self.Img.shape)
        
    #3) t es la tupla semilla y se marca como visitada
    visit[t] = 1
        
    #4) se guarda la tupla en la pila
    self.stack.append(t)
    
def perimeter(img):
    '''
    
    '''
    perimeter = list([])
    for i in range(0,img.shape[1]):
        perimeter.append((0,i))

    for i in range(0,img.shape[1]):
        perimeter.append((img.shape[1]-1,i))
    
    for i in range(0,img.shape[0]):
        perimeter.append((i,0))

    for i in range(0,img.shape[0]):
        perimeter.append((i,img.shape[1]-1))
        
    return perimeter

def detectRegion(s,flatMeansDecrease):
    '''
    the flatt region is considered or not region of influence depending of flatMeansDecreaseVariable
    s is the time series
    d: derivative
    
    we cut at first decrease. 
    if no decrease we take the last index
    
    flatMeansDecrease = True
    [0,2,3,4,5,5,5,5,4]
             |
            cut
            
    flatMeansDecrease = False
    
     [0,2,3,4,5,5,5,5,4]
                    |
                   cut
    
    
    '''
    
    d = np.array(s[1:] - np.array(s[:-1]))

    cut = len(d)
    
    for i,j in enumerate(d):
        #Flat means decrease
        
        decrease = j<0
        
        if flatMeansDecrease:
            
            decrease = (j<=0)
        
        if  decrease:
            
            cut = i
            
            break
            
    return cut

def constructMask(si,img,flatMeansDecrease):
    
    '''
    
    '''
    
    from skimage.draw import line
    
    sv = np.zeros(img.shape)
    
    msk = np.zeros(img.shape)
    
    corner = perimeter(img)
    
    for x in corner:
        
        rr, cc = line(si[0], si[1], x[0], x[1])
        
        l = list([])
        
        
        for i in range(len(rr)):
            
            a = (rr[i],cc[i])
            
            l.append(img[a])
            
        #calculate the differences
        
        derivative = np.array(l[1:] - np.array(l[:-1]))
        
        #we detect the first derivative with the decresase of semivariogram
        
        if len(np.where((derivative <= 0)*1==1)[0])>0:
            
            ix = np.where((derivative <= 0)*1==1)[0][0]+0
            
        else:
            
            #the last index possible in derivative vector
            
            ix = len(derivative)-1
        
        ix = detectRegion(l,flatMeansDecrease)
        
        
        #we mark this with one
        #detect if msk[x,y] has been aleady assigned
    #    for i in range(ix+1):
            
        msk[rr[:ix+1],cc[:ix+1]] = 1
    
    return msk
    
    
    
        
    
    
    
    
    
    