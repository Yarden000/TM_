'''
this file is only used for testing and wont be used in the game
'''

import numpy as np
import pygame, sys
import random
import math
import time
'''
a = np.empty((4, 4), '<U5')
print(a)

a[1, 1] = 'hello'
print(a)



a = np.array([pygame.image.load('../graphics/test/desert.png'), pygame.image.load('../graphics/test/plains.png')])
print(a.dtype)

a = np.empty((4, 4), 'object')
print(a)
a[1, 1] = pygame.image.load('../graphics/test/desert.png')
a[1, 2] = pygame.Vector2(1, 2)
print(a)

a1 = np.array([1.0, 3.5])
a2 = np.array([pygame.image.load('../graphics/test/desert.png'), pygame.image.load('../graphics/test/plains.png')])
a3 = np.array(['g', 'h'])
b = np.array([a1, a3])
print(b)
print(b.dtype)

a = np.array(['hellosss', 'good'])
print(a.dtype)
'''


VEC_2 = pygame.Vector2

def biggest_vector(vec_list):
    mag_list = [i.magnitude() for i in vec_list]
    smalest_mag = max(mag_list)
    index = mag_list.index(smalest_mag)
    return vec_list[index]

def smallest_vector(vec_list):
    mag_list = [i.magnitude() for i in vec_list]
    smalest_mag = min(mag_list)
    index = mag_list.index(smalest_mag)
    return vec_list[index]

def v1_same_direction_as_v2(v1, v2):
    if v2.magnitude() != 0:
        return abs(v1.dot(v2)) / v2.magnitude() * v2.normalize()
    return v1


def rect_rect(rect1, rect2):  # insired by https://stackoverflow.com/questions/62028169/how-to-detect-when-rotated-rectangles-are-colliding-each-other
        rect1_vec1_mag = rect1.vec1.magnitude()
        rect1_vec2_mag = rect1.vec2.magnitude()
        rect2_vec1_mag = rect2.vec1.magnitude()
        rect2_vec2_mag = rect2.vec2.magnitude()
        if (rect1.vec1.dot(rect1.vec2) + rect2.vec1.dot(rect2.vec2)) != 0:
            raise ValueError("The vectors aren't perpendicular.")
        if rect1_vec1_mag * rect1_vec2_mag * rect2_vec1_mag * rect2_vec2_mag == 0:
            raise ValueError("A vector in null.")
        
        #rect corners
        rect1_corners = (
            rect1.pos + rect1.vec1 + rect1.vec2, 
            rect1.pos + rect1.vec1 - rect1.vec2, 
            rect1.pos - rect1.vec1 + rect1.vec2, 
            rect1.pos - rect1.vec1 - rect1.vec2
        )
        rect2_corners = (
            rect2.pos + rect2.vec1 + rect2.vec2, 
            rect2.pos + rect2.vec1 - rect2.vec2, 
            rect2.pos - rect2.vec1 + rect2.vec2, 
            rect2.pos - rect2.vec1 - rect2.vec2
        )
        # finding the corner projections on the two axies of the other rect
        rect1_progections_on_rect2_axis1 = []
        rect1_progections_on_rect2_axis2 = []
        for corner in rect1_corners:
            distance_vector = VEC_2(corner) - VEC_2(rect2.pos) 
            rect1_progections_on_rect2_axis1.append((distance_vector.dot(rect2.vec1) * rect2.vec1) / (rect2_vec1_mag ** 2))
            rect1_progections_on_rect2_axis2.append((distance_vector.dot(rect2.vec2) * rect2.vec2) / (rect2_vec2_mag ** 2))

        rect2_progections_on_rect1_axis1 = []
        rect2_progections_on_rect1_axis2 = []
        for corner in rect2_corners:
            distance_vector = VEC_2(corner) - VEC_2(rect1.pos) 
            rect2_progections_on_rect1_axis1.append((distance_vector.dot(rect1.vec1) * rect1.vec1) / (rect1_vec1_mag ** 2))
            rect2_progections_on_rect1_axis2.append((distance_vector.dot(rect1.vec2) * rect1.vec2) / (rect1_vec2_mag ** 2))
            
        # finding the external projections
        list = [projection.dot(rect2.vec1.normalize()) for projection in rect1_progections_on_rect2_axis1]
        external_rect1_progections_on_rect2_axis1 = [min(list) * rect2.vec1.normalize(), max(list) * rect2.vec1.normalize()]

        list = [projection.dot(rect2.vec2.normalize()) for projection in rect1_progections_on_rect2_axis2]
        external_rect1_progections_on_rect2_axis2 = [min(list) * rect2.vec2.normalize(), max(list) * rect2.vec2.normalize()]

        list = [projection.dot(rect1.vec1.normalize()) for projection in rect2_progections_on_rect1_axis1]
        external_rect2_progections_on_rect1_axis1 = [min(list) * rect1.vec1.normalize(), max(list) * rect1.vec1.normalize()]

        list = [projection.dot(rect1.vec2.normalize()) for projection in rect2_progections_on_rect1_axis2]
        external_rect2_progections_on_rect1_axis2 = [min(list) * rect1.vec2.normalize(), max(list) * rect1.vec2.normalize()]

        # finding if all the lines conecting the projections hit the rectangles
        requirement1 = False
        requirement2 = False
        requirement3 = False
        requirement4 = False
        displacement_vectors = []
        if external_rect1_progections_on_rect2_axis1[0].dot(external_rect1_progections_on_rect2_axis1[1]) < 0:
            requirement1 = True
            deepest_projection = smallest_vector(external_rect1_progections_on_rect2_axis1)
            displacement_vectors.append(-v1_same_direction_as_v2(rect2.vec1, deepest_projection) - deepest_projection)
        elif external_rect1_progections_on_rect2_axis1[0].magnitude() < rect2_vec1_mag or external_rect1_progections_on_rect2_axis1[1].magnitude() < rect2_vec1_mag:
            requirement1 = True
            deepest_projection = smallest_vector(external_rect1_progections_on_rect2_axis1)
            displacement_vectors.append(v1_same_direction_as_v2(rect2.vec1, deepest_projection) - deepest_projection)
        else: 
            return False, None

        if external_rect1_progections_on_rect2_axis2[0].dot(external_rect1_progections_on_rect2_axis2[1]) < 0:
            requirement2 = True
            deepest_projection = smallest_vector(external_rect1_progections_on_rect2_axis2)
            displacement_vectors.append(-v1_same_direction_as_v2(rect2.vec2, deepest_projection) - deepest_projection)
        elif external_rect1_progections_on_rect2_axis2[0].magnitude() < rect2_vec2_mag or external_rect1_progections_on_rect2_axis2[1].magnitude() < rect2_vec2_mag:
            requirement2 = True
            deepest_projection = smallest_vector(external_rect1_progections_on_rect2_axis2)
            displacement_vectors.append(v1_same_direction_as_v2(rect2.vec2, deepest_projection) - deepest_projection)
        else: 
            return False, None

        if external_rect2_progections_on_rect1_axis1[0].dot(external_rect2_progections_on_rect1_axis1[1]) < 0:
            requirement3 = True
            deepest_projection = smallest_vector(external_rect2_progections_on_rect1_axis1)
            displacement_vectors.append(-v1_same_direction_as_v2(rect1.vec1, deepest_projection) - deepest_projection)
        elif external_rect2_progections_on_rect1_axis1[0].magnitude() < rect1_vec1_mag or external_rect2_progections_on_rect1_axis1[1].magnitude() < rect1_vec1_mag:
            requirement3 = True
            deepest_projection = smallest_vector(external_rect2_progections_on_rect1_axis1)
            displacement_vectors.append((v1_same_direction_as_v2(rect1.vec1, deepest_projection) - deepest_projection) * -1)
        else: 
            return False, None

        if external_rect2_progections_on_rect1_axis2[0].dot(external_rect2_progections_on_rect1_axis2[1]) < 0:
            requirement4 = True
            deepest_projection = smallest_vector(external_rect2_progections_on_rect1_axis2)
            displacement_vectors.append(-v1_same_direction_as_v2(rect1.vec2, deepest_projection) - deepest_projection)
        elif external_rect2_progections_on_rect1_axis2[0].magnitude() < rect1_vec2_mag or external_rect2_progections_on_rect1_axis2[1].magnitude() < rect1_vec2_mag:
            requirement4 = True
            deepest_projection = smallest_vector(external_rect2_progections_on_rect1_axis2)
            displacement_vectors.append((v1_same_direction_as_v2(rect1.vec2, deepest_projection) - deepest_projection) * -1)
        else: 
            return False, None

        if requirement1 and requirement2 and requirement3 and requirement4:
            minimal_displacement = smallest_vector(displacement_vectors)
            return True, minimal_displacement
        
def rect_circle(circle, rect):  # cilrcle = {'pos': tuple, 'r': int}, rect = {'pos': tuple, 'vec1':vect, 'vec2':vect} vec1, vec2 perpendicular
        vec1_mag = rect.vec1.magnitude()
        vec2_mag = rect.vec2.magnitude()
        if rect.vec1.dot(rect.vec2) != 0:
            raise ValueError("The vectors aren't perpendicular.")
        if vec1_mag == 0 or vec2_mag == 0:
            raise ValueError("A vector in null.")
        
        distance_vector = VEC_2(rect.pos) - VEC_2(circle.pos)

        dist_to_center_1 = distance_vector.dot(rect.vec1) / vec1_mag # distance to the rect center anolg the axis 1
        dist_to_center_2 = distance_vector.dot(rect.vec2) / vec2_mag # distance to the rect center anolg the axis 2
        abs_dist_to_center_1 = abs(dist_to_center_1)
        abs_dist_to_center_2 = abs(dist_to_center_2)
        print(dist_to_center_1, dist_to_center_2)
        dist_1_sign = dist_to_center_1 / abs(dist_to_center_1) if dist_to_center_1 != 0 else 1
        dist_2_sign = dist_to_center_2 / abs(dist_to_center_2) if dist_to_center_2 != 0 else 1

        # definitely not colliding
        if (abs_dist_to_center_1 > vec1_mag + circle.r): return False, None
        if (abs_dist_to_center_2 > vec2_mag + circle.r): return False, None
        # definitly colliding
        if (abs_dist_to_center_1 <= vec1_mag): return True, rect.vec2.normalize() * (abs_dist_to_center_2 - vec2_mag - circle.r) * dist_2_sign
        if (abs_dist_to_center_2 <= vec2_mag): return True, rect.vec1.normalize() * (abs_dist_to_center_1 - vec1_mag - circle.r) * dist_1_sign
        # corner cases
        d1 = abs_dist_to_center_1 - vec1_mag
        d2 = abs_dist_to_center_2 - vec2_mag
        if d1*d1 + d2*d2 <= circle.r * circle.r:
            pushout = (circle.r / math.sqrt(d1*d1 + d2*d2) - 1) * VEC_2(-d1 * dist_1_sign, d2 * dist_2_sign)
            return True, pushout
        return False, None

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption('Survivorio')

        self.clock = pygame.time.Clock()

        self.rect1 = Rect((200, 200), 0, 100, 50)
        self.rect2 = Rect((500, 500), 55, 50, 25)
        self.circle = Circle((500, 500), 80)

    def run(self):
        game_run = True
        while game_run:
            # testing
            #print(self.collision_detector.Rect_Circle({'pos': (2, 2), 'r': 1}, {'pos': (0, 0), 'vec1': VEC_2(1, 1), 'vec2': VEC_2(-1, 1)}))
            for event in pygame.event.get():  # event loop
                if event.type == pygame.QUIT:  # checks if quit
                    pygame.quit()
                    sys.exit()

            # testing
            keys = pygame.key.get_pressed()
            direction = VEC_2()
            angle = 0
            if keys[pygame.K_w]:
                direction.y += -1
            if keys[pygame.K_s]:
                direction.y += 1
            if keys[pygame.K_d]:
                direction.x += 1
            if keys[pygame.K_a]:
                direction.x += -1
            if direction.magnitude() != 0:
                direction = direction.normalize()
            if keys[pygame.K_q]:
                angle -= 1
            if keys[pygame.K_e]:
                angle += 1
            if keys[pygame.K_c]:
                displacement = direction * 10
            else:
                displacement = direction
            #'''
            if keys[pygame.K_0]:
                #self.circle.move(displacement)
                self.circle.move_to_mouse()
            #'''
            if keys[pygame.K_8]:
                #self.rect1.move(displacement)
                self.rect1.move_to_mouse()
                self.rect1.rotate(angle)
            #'''
            if keys[pygame.K_9]:
                #self.rect2.move(displacement)
                self.rect2.move_to_mouse()
                self.rect2.rotate(angle)
            #'''
            self.screen.fill('blue')
            color = 'green'
            start = time.time()
            #collision_state, pushout = rect_circle(self.circle, self.rect1)
            collision_state, pushout = rect_rect(self.rect2, self.rect1)
            print(pushout)
            if collision_state:
                color = 'red'
                if pushout != None:
                    self.rect1.move(-pushout)
                    self.circle.move(pushout)
            end = time.time()
            #print(end - start)
            self.rect1.draw(color)
            #self.circle.draw(color)
            self.rect2.draw(color)

            pygame.display.update()

            dt = self.clock.get_time() / 1000
            pygame.display.set_caption(f"Survivorio | FPS: {str(int(self.clock.get_fps()))} | dt: {str(dt)}")
            self.clock.tick(60) 



class Circle:
    def __init__(self, pos, radius):
        self.pos = pos
        self.r = radius

    def move(self, disipacement):
        self.pos += disipacement

    def move_to_mouse(self):
        self.pos = pygame.mouse.get_pos()

    def draw(self, color):
        pygame.draw.circle(pygame.display.get_surface(), color, self.pos, self.r)

class Rect:
    def __init__(self, pos, angle, length, breadth):
        angle = angle * 180 / math.pi
        self.pos = VEC_2(pos)
        self.vec1 = VEC_2(math.cos(angle), math.sin(angle)) * length
        self.vec2 = VEC_2(math.sin(angle), -math.cos(angle)) * breadth

    def move(self, disipacement):
        self.pos += disipacement

    def move_to_mouse(self):
        self.pos = pygame.mouse.get_pos()

    def rotate(self, angle):
        self.vec1 = self.vec1.rotate(angle)
        self.vec2 = self.vec2.rotate(angle)

    def draw(self, color):
        pygame.draw.line(pygame.display.get_surface(), color, self.pos + self.vec1 + self.vec2, self.pos + self.vec1 - self.vec2, width = 5)
        pygame.draw.line(pygame.display.get_surface(), color, self.pos - self.vec1 + self.vec2, self.pos - self.vec1 - self.vec2, width = 5)
        pygame.draw.line(pygame.display.get_surface(), color, self.pos + self.vec2 + self.vec1, self.pos + self.vec2 - self.vec1, width = 5)
        pygame.draw.line(pygame.display.get_surface(), color, self.pos - self.vec2 + self.vec1, self.pos - self.vec2 - self.vec1, width = 5)


game = Game()
game.run()
