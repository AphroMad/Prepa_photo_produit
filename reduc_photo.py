# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 18:47:44 2019

@author: pierr
"""

# =============================================================================
# Code pour rétrécir au maximum une photo ( on enlève le maximum de blanc sur les contours en fait )
# =============================================================================

Debug = False
bug = False 
pb_name = False 
pb_bordure = False 
oui = False 

from PIL import Image # on importe le module pour avoir les dim de l'image 
from PIL import ImageDraw
from PIL import ImageFont
import glob
import os 

def supimg(path,nom,indice,front, background) : 
    
    front = Image.open(front) # on ouvre les images 
    background = Image.open(background)
    
    ft_l, ft_h = front.size # on choppe leurs tailles 
    bg_l, bg_h = background.size 
    
    ft_centre = [ft_l/2,ft_h/2] # on choppe les milieux des images 
    bg_centre = [bg_l/2,bg_h/2]
    
    img = Image.new('RGBA', background.size,(0,0,0,0)) # on les superpose 
    img.paste(background,(0,0))
    img.paste(front,(int(bg_centre[0]-ft_centre[0]),int(bg_centre[1]-ft_centre[1])-23))
    img.save(path+"\\done\\"+nom+".png")

# =============================================================================
# Commencement (on fait les input)
# =============================================================================
chemin = input("veuillez rentrer le chemin de là où il y a les photos :\n ") # on demande à l'utilisateur de rentrer le chemin et le nom de la photo 
if not os.path.exists(str(chemin)+"\done"): 
   os.makedirs(str(chemin)+"\done")
titre_photo = input("Veuillez aussi entrer le titre que vous voulez pour vos photos :\n " ) # on demande à l'utilisateur de rentrer le nom qui voudra avoir sur ses photos 
emplacement = os.path.dirname(os.path.realpath(__file__)) #returns a string value which represents the directory name from the specified path.
#print(emplacement)
os.chdir(emplacement) # change current directory
# =============================================================================
# on récupère toutes les photos du dossier 
# =============================================================================
if Debug : print("on récupère les photos dans le dossier")
image_list = [] # on créer un tableau dans lequel on va mettre toutes les images 
name_image = [] # on créer un tableau dans lequel on va mettre les noms des images 
for filename in glob.glob(chemin+"\*.jpg" ): # I browse all.jpg files that are in the directory indicated by the variable "chemin".
    im=Image.open(filename)
    image_list.append(im) # I add the image to a table
    name_image.append(os.path.relpath(filename, chemin))
for filename in glob.glob(chemin+"\*.png"): # I browse all.jpg files that are in the directory indicated by the variable "chemin".
    im=Image.open(filename) # on ouvre l'image 
    image_list.append(im) # I add the image to a table
    name_image.append(os.path.relpath(filename,chemin)) # on enregistre l'image avec son nom dans une case du tableau


# =============================================================================
# fonction qui enlève les bordures blanches 
# =============================================================================
if Debug : print("on a récup les images, on enlève les bordures blanches")
for p in range(len(image_list)) : 

    ima = image_list[p] # on choisit la photo 
    #ima = Image.open(chemin) # on ouvre l'image 
    largeur, hauteur = ima.size  # on prend ses dimensions 
    pix = ima.load() # on la charge (pour les pixels)
    
    ok = True 
    h = 0 
    d = largeur - 1 
    g = 0
    b = hauteur - 1
    
    z = 1 # on initialise la variable qui dit qu'on a trouvé une autre couleur que le blanc 
    for i in range(hauteur) : # on parcoure toute la hauteur 
        for l in range(largeur) : # on parcoure toute la longueur 
            if pix[l,i] == (255,255,255) : # on regarde si le pixel est  blanc  
                h = i  # si oui, on donne la limite verticale ou horizontale 
            else : 
                z = 0 # si le pixel est différent de blanc, alors on a finit de rechercher la limite
                if pb_bordure : print("limite haut : ",i,"h = ",h,i,l)

                break # # on sort de la première boucle 
        if z == 0 : break # on sort de la deuxième boucle 
        
    z = 1
    for i in range(hauteur) : 
        for l in range(largeur):
            nl = largeur - 1  - l # on cherche la limite du bas donc on pars du bas de la photo et on va en remontant 
            ni = hauteur - 1  - i # same 
            if pix[nl,ni] == (255,255,255) : 
                b = ni
            else : 
                z = 0 
                if pb_bordure : print("limite bas : ",ni,"b = ",b,i,l)

                break
        if z == 0 : break 
    
    z = 1
    for i in range(largeur) : 
        for l in range(hauteur):
            if pix[i,l] == (255,255,255) : 
                g = i
            else : 
                z = 0 
                if pb_bordure : print("limite gauche : ",i,"g = ",g,i,l)
                break
        if z == 0 : break     
    
    z = 1
    for i in range(largeur) : 
        for l in range(hauteur):
            nl = hauteur - 1  - l 
            ni = largeur - 1  - i 
            if pix[ni,nl] == (255,255,255) : 
                d = ni
                
            else : 
                z = 0 
                if pb_bordure : print("limite droite : ",ni,"d = ",d,i,l)
                break
        if z == 0 : break 

    if pb_bordure : print("là où on va couper : ", g,h,d,b)
    #print("position : \ngauche : ",g,"\nhaut : ",h,"\ndroite : ",d,"\nbas : ",b) # on écrit les pos 
    if pb_bordure : print("avant la modif : ",ima.size)
    ima = ima.crop((g,h,d,b)) # on découpe la photo 
    if pb_bordure : print("après la modif : ", ima.size, "\n")
    if ima.size == (0,0) : ok = False  
    #ima.save(str(chemin)+'\\photo_'+str(p)+'.jpg') # on la ré-enregistre sous un autre nom  
    
    
    # =============================================================================
    # Mise aux bonnes dimensions 
    # =============================================================================
    if ok == True : 
        w,h = ima.size # on choppe les dimensions pour ensuite les comparer 
        if pb_name and ( w == 0 or h == 0 ): im.show()
        if bug : print(w,h,ima.size)
        if w > h : # on regarde si l'image est plus large que haute tout en gardant le ratio 
            basewidth = 600 # on définit la largeur que l'on veut 
            wpercent = (basewidth/float(ima.size[0])) # on divise cette largeur par la vraie largeur de l'image (pour avoir le ratio)
            hsize = int((float(ima.size[1])*float(wpercent))) # on applique ce ratio a notre hauteur 
        else : # sinon, elle est plus haute que large 
            hsize = 470 # on fais la même que plus haut mais avec la hauteur en base 
            hpercent = (hsize/float(ima.size[1]))
            basewidth = int(float(ima.size[0])*float(hpercent))
        if bug :print(w,h,basewidth,hsize,"step2:")
    
        if basewidth > 600 :
            
            basewidth = 575 # on définit la largeur que l'on veut 
            wpercent = (basewidth/float(ima.size[0])) # on divise cette largeur par la vraie largeur de l'image (pour avoir le ratio)
            hsize = int((float(ima.size[1])*float(wpercent))) # on applique ce ratio a notre hauteur 
            
        elif hsize > 470 :
            
            hsize = 445 # on fais la même que plus haut mais avec la hauteur en base 
            hpercent = (hsize/float(ima.size[1]))
            basewidth = int(float(ima.size[0])*float(hpercent))
            
        if bug : print(w,h,basewidth,hsize,'\\photo_'+str(p)+'.jpg')
        ima = ima.resize((basewidth,hsize), Image.ANTIALIAS)
        ima.save(str(chemin)+'\\photo_'+str(p)+'.jpg') # on la ré-enregistre sous un autre nom  
    
        
        # =============================================================================
        # superposition des images
        # =============================================================================
        if Debug : print("on superpose les images")
        supimg(chemin,name_image[p],p,str(chemin)+'\\photo_'+str(p)+'.jpg',emplacement+"\\fond_ecran.jpg")
    
        # =============================================================================
        # supression des images temporaires 
        # =============================================================================
        if Debug : print("on supprime les images inutiles")
        os.remove(str(chemin)+'\\photo_'+str(p)+'.jpg') 

        # =============================================================================
        # rajout du texte 
        # =============================================================================
        #input("test3")  
        if Debug : print("On rajoute le texte et on enregistre tout")
        modif = Image.open(chemin+"\\done\\"+name_image[p]+".png") 
        draw = ImageDraw.Draw(modif)
 
        ici = os.getcwd() # return current working directory 
        
        try : 
            font = ImageFont.truetype(ici+"\\font\\AppleGaramond.ttf",40)
            taille_x,taille_y = ImageDraw.ImageDraw.textsize(draw,titre_photo,font,4)
            pos_x = 756 / 2 - taille_x/2
            draw.text((pos_x ,42),titre_photo,(0,0,0), font = font )
        except Exception as err: 
            print(err)
            

            
        #input("test6")  
        modif = modif.save(chemin+"\\done\\"+name_image[p]+".png")

input("over (appuie sur une touche)")