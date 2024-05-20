import pygame
from map import Map
from player import Player
from entities import (
    Ressource,
    Animal
)
from spawner import Spawner
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
        self.entity_manager = EntityManager()
        self.displayer = Displayer(self.map, self.camera, self.entity_manager)

        self.spawner = Spawner(self.camera, self.map, self.displayable_entenies)

        self.entity_manager.add_new_entity(Player())


    def run(self, dt):
        # all the interactions / events / calculations of the game
        self.player.run(dt, self.camera)

        # test
        # self.spawner.spawn_test_ent(pos = (0, 0))
        self.spawner.spawn_ent(dt, Animal)
        self.spawner.spawn_ent(dt, Ressource)

        for i in self.displayable_entenies:  # testing
            if not i == self.player:
                i.run(dt)

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
            # FIXME: for i in self.entity_maanager.displayed_entities:
            # trier selon la position
            i.display(self.screen, self.camera)
        # print(len(self.displayable_entenies))
        pygame.display.update()
