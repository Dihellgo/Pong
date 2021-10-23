"""JEU DE PONG"""

"""Import des modules et fonctions nécéssaires"""
import tkinter as Tk
import random
from math import sin, cos, pi, sqrt
from threading import Thread
from time import sleep


"""Définition des fonctions nécessaires au programme"""
def wCentre(objet):
    """Renvoie les coordonnées du centre du widget"""
    objet.update()
    return(objet.winfo_width()/2, objet.winfo_height()/2)

def press(event):
    key_press[event.keysym]=True
    move_launch(event)
         
def release(event):
    key_press[event.keysym]=False

def move(event):
    while key_press != {"z":False, "s":False, "Up":False, "Down":False, "q":False, "d":False}:
        if key_press["Up"]:
            plateauJeu.move(raquette2, 0, -10)
        if key_press["z"]:
            plateauJeu.move(raquette1, 0, -10)
        if key_press["Down"]:
            plateauJeu.move(raquette2, 0, 10)
        if key_press["s"]:
            plateauJeu.move(raquette1, 0, 10)
        if key_press["q"] and key_press["d"]:
            balle.versLaDroite()
        sleep(0.03)
    global does_move
    does_move = False

def move_launch(evt):
    global does_move
    if not does_move:
        does_move = True
        a = MonThread(evt)
        a.start()
    

"""Création des classes nécessaires au programme"""
class MonThread(Thread):
    def __init__(self, evt):
        Thread.__init__(self)
        self.evt = evt

    def run(self):
        move(self.evt)
        


class BalleJeu():
    """Crée un objet de type Balle affiché sur le canvas donné"""
    def __init__(self, canv):
        self.__x, self.__y = wCentre(canv)
        self.__dirx, self.__diry = self.defDirDepart()
        self.__contact_raquette = False
        self.__vitesse = 1
        self.balle = canv.create_oval(self.__x - canv.winfo_height()/30, self.__y + canv.winfo_height()/30, self.__x + canv.winfo_height()/30, self.__y - canv.winfo_height()/30, fill = "#0f0")

    def defDirDepart(self):
        """Définie la direction de départ de la balle"""
        self.__xdepart=random.random()
        while self.__xdepart >= 0.95 or self.__xdepart < 0.35:
            self.__xdepart=random.random()
        return self.__xdepart * random.choice([1, -1]), sqrt(1-self.__xdepart**2) * random.choice([1, -1])

    def move(self):
        """Déplace la balle"""
        #Sauvegarde les coordonnées de la balle avant déplacement
        self.__pastx = self.__x
        self.__pasty = self.__y
        #Définie les nouvelles coordonnées de la balle
        plateauJeu.update()
        self.__x += plateauJeu.winfo_width()/130 * self.__dirx * self.__vitesse
        self.__y -= plateauJeu.winfo_width()/130 * self.__diry * self.__vitesse
        #Déplace la balle
        plateauJeu.move(self.balle, self.__x-self.__pastx,self.__y - self.__pasty)
        FEN.after(25, self.move)
        self.__vitesse *= 1.001
        self.chDir()

    def chDir(self):
        if self.__y < plateauJeu.winfo_height()/130:
            self.__diry *= -1

        elif self.__y > plateauJeu.winfo_height()*129/130:
            self.__diry *= -1

        if self.__contact_raquette <=0 and (len(plateauJeu.find_overlapping(plateauJeu.coords(raquette1)[0], plateauJeu.coords(raquette1)[1], plateauJeu.coords(raquette1)[2], plateauJeu.coords(raquette1)[3])) > 1 or len(plateauJeu.find_overlapping(plateauJeu.coords(raquette2)[0], plateauJeu.coords(raquette2)[1], plateauJeu.coords(raquette2)[2], plateauJeu.coords(raquette2)[3])) > 1):
            self.__dirx *= -1
            self.__contact_raquette = 5

        else:
            self.__contact_raquette -=1
    
    def versLaDroite(self):
        self.__dirx = abs(self.__dirx)

        
        
"""Définition des constantes et des scores"""
FEN = Tk.Tk()

#Récupère la taille de l'écran
window_height = int(FEN.winfo_screenheight()*0.9)
window_width = int(FEN.winfo_screenwidth()*0.99)

FEN.resizable(width=False, height=False)
FEN.geometry("%sx%s+%s+%s" %(window_width, window_height, 0, 0))
FEN.title('JEU DE PONG')

#Initialisation des scores des joueurs et de la variable pour les afficher
scoreJ1 = 0
scoreJ2 = 0
scoreJ1Var = Tk.StringVar(value=str(0)*(3-len(str(scoreJ1)))+str(scoreJ1))
scoreJ2Var = Tk.StringVar(value=str(0)*(3-len(str(scoreJ2)))+str(scoreJ2))

#Initialisation de la ligne d'affichage
score_gauche = Tk.Label(FEN, bg = '#000', font = ('Liberation Sans Sérif', 20), text = scoreJ1Var.get(), fg = '#ff0')
score_droite = Tk.Label(FEN, bg = '#000', font = ('Liberation Sans Sérif', 20), text = scoreJ2Var.get(), fg = '#ff0')
titre = Tk.Canvas(FEN, height=window_height/20, width=int(window_width-score_gauche.winfo_reqwidth()-score_droite.winfo_reqwidth()))
#Affichage des variables pour initialiser correctement les valeurs
score_gauche.grid(column=0, row=0)
score_droite.grid(column=2, row=0)
titre.grid(column= 1, row=0)
#
titre.create_text(wCentre(titre), text = 'JEU DE PONG', font = ('Liberation Sans Sérif', 20), fill = "#b24933")
#
score_gauche.grid_forget()
score_droite.grid_forget()
titre.grid_forget()
#

#Initialisation du plateau de jeu
plateauJeu = Tk.Canvas(FEN, height = window_height-titre.winfo_height(), width = window_width, bg = '#4e50c0')

#Affichage des variables pour initialiser correctement les valeurs
plateauJeu.grid(column= 0, row = 1, columnspan = 3)
#
raquette1 = plateauJeu.create_rectangle(window_width/20, wCentre(plateauJeu)[1] + plateauJeu.winfo_height()/10, window_width/15, wCentre(plateauJeu)[1] - plateauJeu.winfo_height()/10, fill = "#fff")
raquette2 = plateauJeu.create_rectangle(19 * window_width/20, wCentre(plateauJeu)[1] + plateauJeu.winfo_height()/10, 14 * window_width/15, wCentre(plateauJeu)[1] - plateauJeu.winfo_height()/10, fill = "#fff")

balle = BalleJeu(plateauJeu)
#
plateauJeu.grid_forget()
#

does_move = False

#Déplacement des raquettes
key_press={"z":False, "s":False, "Up":False, "Down":False, "q":False, "d":False}

for key in ["Up", "z", "s", "Down", "q", "d"]:
    FEN.bind_all('<KeyPress-%s>' %key, press)   
    FEN.bind_all('<KeyRelease-%s>' %key, release)

#Définition des événements
FEN.after(100, balle.move)

#Affichage du jeu et lancement de la boucle
if __name__ == '__main__':
    score_gauche.grid(column=0, row=0)
    score_droite.grid(column=2, row=0)
    titre.grid(column= 1, row=0)
    plateauJeu.grid(column= 0, row = 1, columnspan = 3)

    FEN.mainloop()
