'''collision detection'''
import math
from settings import(
    VEC_2
)

class CollisionDetector:
    '''responsible for detecting collisions and calculating their pushout'''
    def __init__(self):
        pass

    def collision(self, hitbox1, hitbox2, want_pushout=True):
        '''sorts which collision detection to use'''
        if hitbox1.kind == 'rect':

            if hitbox2.kind == 'rect':
                state, pushout = self.rect_rect(hitbox1, hitbox2)
                if want_pushout:
                    return state, pushout
                return state

            elif hitbox2.kind == 'circle':
                state, pushout = self.rect_circle(hitbox1, hitbox2)
                if want_pushout:
                    return state, pushout
                return state

        elif hitbox1.kind == 'circle':

            if hitbox2.kind == 'rect':
                state, pushout = self.circle_rect(hitbox1, hitbox2)
                if want_pushout:
                    return state, pushout
                return state

            elif hitbox2.kind == 'circle':
                state, pushout = self.circle_circle(hitbox1, hitbox2)
                if want_pushout:
                    return state, pushout
                return state


    def circle_circle(self, circle1, circle2):
        '''circle-circle collision'''
        dist = VEC_2(circle1.pos).distance_to(VEC_2(circle2.pos))
        overlap = -(dist - circle1.r - circle2.r)
        displacement = overlap * (circle1.pos - circle2.pos).normalize()
        if dist < circle1.r + circle2.r:
            return True, displacement
        return False, None

    def smallest_vector(self, vec_list):
        '''returns the vector with the smallest magnitude'''
        mag_list = [i.magnitude() for i in vec_list]
        smalest_mag = min(mag_list)
        index = mag_list.index(smalest_mag)
        return vec_list[index]

    def v1_same_direction_as_v2(self, v1, v2):
        '''
        returns a projection of v1 on v2 that is pointing in the same direction as v2
        similar to projection_vect
        '''
        if v2.magnitude() != 0:
            return abs(v1.dot(v2)) / v2.magnitude() * v2.normalize()
        return v1

    def rect_corners(self, rect):
        '''returns the coordinates of the corners of a rect'''
        return (
            rect.pos + rect.vec1 + rect.vec2,
            rect.pos + rect.vec1 - rect.vec2,
            rect.pos - rect.vec1 + rect.vec2,
            rect.pos - rect.vec1 - rect.vec2
            )

    def projection_vect(self, projected_vector, axis_vector):
        '''returns a projection of v1 on v2'''
        return projected_vector.dot(axis_vector) * axis_vector / axis_vector.magnitude() ** 2

    def external_vectors(self, vector_list, axis_vector):
        '''gives the two vectors whitch projections on the axis would be the farthest apart'''
        axis_vector = axis_vector.normalize()
        l = [vector.dot(axis_vector) for vector in vector_list]
        return [min(l) * axis_vector, max(l) * axis_vector]

    def progections_colliding_with_rect(self, projections, axis_vector):
        '''checks if the line between the tow projections is tuching the rect'''
        axis_vector_mag = axis_vector.magnitude()
        if projections[0].dot(projections[1]) < 0:
            deepest_projection = self.smallest_vector(projections)
            return True, -self.v1_same_direction_as_v2(axis_vector, deepest_projection) - deepest_projection
        elif projections[0].magnitude() < axis_vector_mag or projections[1].magnitude() < axis_vector_mag:
            deepest_projection = self.smallest_vector(projections)
            return True, self.v1_same_direction_as_v2(axis_vector, deepest_projection) - deepest_projection
        else:
            return False, None

    def rect_rect(self, rect1, rect2):
        '''
        insired by https://stackoverflow.com/questions/62028169/how-to-detect-when-rotated-rectangles-are-colliding-each-other
        Separating Axis Theorem (SAT)     
        '''
        rect_vectors = [
            [rect2.vec1, rect2.vec2],
            [rect1.vec1, rect1.vec2]
        ]

        #rect corners
        rect1_corners = self.rect_corners(rect1)
        rect2_corners = self.rect_corners(rect2)

        # finding the corner projections on the two axies of the other rect
        projections = [
            [
                [self.projection_vect(VEC_2(corner) - VEC_2(rect2.pos), rect2.vec1) for corner in rect1_corners], #(progections_on_rect2_axis1, axis_vector)
                [self.projection_vect(VEC_2(corner) - VEC_2(rect2.pos), rect2.vec2) for corner in rect1_corners]  #(progections_on_rect2_axis2, axis_vector)
            ], # rect1
            [
                [self.projection_vect(VEC_2(corner) - VEC_2(rect1.pos), rect1.vec1) for corner in rect2_corners], #(progections_on_rect1_axis1, axis_vector)
                [self.projection_vect(VEC_2(corner) - VEC_2(rect1.pos), rect1.vec2) for corner in rect2_corners]  #(progections_on_rect1_axis2, axis_vector)
            ], # rect2
        ]

        # finding the external projections
        external_projections = [
            [
                self.external_vectors(projections[rect][axis], rect_vectors[rect][axis]) for axis in range(2) # the two axies
            ] for rect in range(2) # the two rects
        ]   # external_projections[rect][axis][the two oposite projections]

        # finding if all the lines conecting the projections hit the rectangles
        displacement_vectors = []
        for rect in range(2):
            for axis in range(2):
                colliding, pushout = self.progections_colliding_with_rect(external_projections[rect][axis], rect_vectors[rect][axis])
                if not colliding:
                    return False, None
                if pushout is not None:
                    displacement_vectors.append(pushout if rect == 0 else -pushout)
        return True, self.smallest_vector(displacement_vectors)

    def circle_rect(self, circle, rect):
        '''inverses the order of the entities so that they are pushed appart instead of pulled together'''
        state, pushout = self.rect_circle(rect, circle)
        if pushout is not None:
            pushout = -pushout
        return state, pushout

    def rect_circle(self, rect, circle):
        '''collisions between rect and circle'''
        vec1_mag = rect.vec1.magnitude()
        vec2_mag = rect.vec2.magnitude()

        distance_vector = VEC_2(rect.pos) - VEC_2(circle.pos)

        # distances to the centers of the rect along its axies
        dist_to_center_1 = distance_vector.dot(rect.vec1) / vec1_mag
        dist_to_center_2 = distance_vector.dot(rect.vec2) / vec2_mag

        abs_dist_to_center_1 = abs(dist_to_center_1)
        abs_dist_to_center_2 = abs(dist_to_center_2)

        dist_1_sign = dist_to_center_1 / abs(dist_to_center_1) if dist_to_center_1 != 0 else 1
        dist_2_sign = dist_to_center_2 / abs(dist_to_center_2) if dist_to_center_2 != 0 else 1

        # definitely not colliding
        if abs_dist_to_center_1 > vec1_mag + circle.r:
            return False, None
        if abs_dist_to_center_2 > vec2_mag + circle.r:
            return False, None

        # definitly colliding
        if abs_dist_to_center_1 <= vec1_mag:
            pushout = -rect.vec2.normalize() * (abs_dist_to_center_2 - vec2_mag - circle.r) * dist_2_sign
            return True, pushout
        if abs_dist_to_center_2 <= vec2_mag:
            pushout = -rect.vec1.normalize() * (abs_dist_to_center_1 - vec1_mag - circle.r) * dist_1_sign
            return True, pushout

        # corner cases
        d1 = abs_dist_to_center_1 - vec1_mag
        d2 = abs_dist_to_center_2 - vec2_mag
        if d1*d1 + d2*d2 <= circle.r * circle.r:
            norm = circle.r / math.sqrt(d1*d1 + d2*d2) - 1
            direction = VEC_2(-d1 * dist_1_sign, d2 * dist_2_sign)
            pushout = norm * direction
            return True, -pushout
        return False, None
