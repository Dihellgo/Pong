"""Ce fichier contient les définitions des fonctions utilisés dans le jeu"""

def wCentre(objet):
    """Renvoie les coordonnées du centre du widget"""
    objet.update()
    return(objet.winfo_width()/2, objet.winfo_height()/2)


def press(event):
    "Définie la touche pressé et lance le mouuvement"
    key_press[event.keysym]=True
    move_launch(event)


def release(event):
    """Définie la touche n'étant plus pressée"""
    key_press[event.keysym]=False


def move_launch(evt):
    """Lance la fonction déplaçant les raquettes dans un nouveau thread, si cette fonction n'est pas lancée"""
    global does_move
    if not does_move:#Si la fonction déplaçant les raquettes n'est pas lancée
        does_move = True
        a = MonThread(evt)
        a.start()


def move(event):
    """Déplace les raquettes"""
    while key_press != {"z":False, "s":False, "Up":False, "Down":False}:#Tant qu'une touche déplaçant une raquette est pressée
        if key_press["Up"]:
            plateauJeu.move(raquette2, 0, -10)
        if key_press["z"]:
            plateauJeu.move(raquette1, 0, -10)
        if key_press["Down"]:
            plateauJeu.move(raquette2, 0, 10)
        if key_press["s"]:
            plateauJeu.move(raquette1, 0, 10)
        sleep(0.03)
    global does_move
    does_move = False