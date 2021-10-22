"""Création du Thread pour le mouvement des raquettes"""
class ThreadMove(Thread):
    def __init__(self, evt):
        Thread.__init__(self)
        self.evt = evt

    def run(self):
        move(self.evt)
