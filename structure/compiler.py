import pygame, sys
from map import Map
from player import Player
from entities import (
    Entity
    )
from spawner import (
    Spawner
)
from camera import Camera


class Compiler:
    '''
    all the playable part of the game
    '''
    
    def __init__(self):
        self.outside_range_enteties = []

        self.displayable_entenies = []  # need to add a way of ordering from clostest to farthest
        self.collisionable_enteties = []

        self.camera = Camera()
        self.map = Map()
        self.displayer = Displayer(self.map, self.camera, self.displayable_entenies)

        self.chunks = [
            [
                [] for i in range(self.map.chunk_number)
            ] for j in range(self.map.chunk_number)
        ]   # a list of all the enteties in each chunk

        self.spawner = Spawner(self.camera, self.map, self.chunks, self.displayable_entenies)

        self.player = Player(self.displayable_entenies)

        
    def run(self, dt):

        # all the interactions / events / calculations of the game
        self.player.run(dt, self.camera)

        # test
        #self.spawner.spawn_test_ent(pos = (0, 0))
        self.spawner.tiles_loaded()

        self.displayer.run()


class Displayer:
    # il faut ajouter une fonction qui verifie si un element est dans la window avant de le display

    def __init__(self, map, camera, displayable_entenies):
        self.screen = pygame.display.get_surface()
        self.map = map
        self.camera = camera
        self.displayable_entenies = displayable_entenies

    def run(self):
        self.screen.fill('blue')               
        self.map.display(self.camera)
        for i in self.displayable_entenies:
            # trier selon la position
            i.display(self.camera)
        #print(len(self.displayable_entenies))
        pygame.display.update()