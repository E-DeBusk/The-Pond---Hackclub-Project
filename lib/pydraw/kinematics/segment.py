import pygame
import math
from pygame import gfxdraw


class Segment:
    def __init__(self, x, y, angle, sizes, index, color, scale):
        self.a = pygame.Vector2(x, y)
        self.angle = angle
        self.sizes = sizes
        self.index = index
        self.color = color
        self.scale = scale
        self.b = pygame.Vector2(math.sin(angle) * self.sizes[self.index][1], math.cos(angle) * self.sizes[self.index][1])
        
    def solveA(self):
        self.a.update(
            self.b.x + (self.sizes[self.index][1] * self.scale * math.cos(self.angle)),
            self.b.y + (self.sizes[self.index][1] * self.scale * math.sin(self.angle))
        )
        
    def align(self, c):
        transformation = self.a - pygame.Vector2(c[0], c[1])
        self.angle = math.atan2(transformation.y, transformation.x)
        
        self.a = pygame.Vector2.__add__(c, transformation)
           
    def anchor(self, c):
        self.b = pygame.Vector2(c[0], c[1])
        self.solveA()
        
    def solve(self, c):
        self.align(c)
        self.anchor(c)
        
    def draw(self, surface):
        a_radius = self.sizes[self.index][0]
        b_radius = self.sizes[self.index][0]
        
        if self.index != len(self.sizes) - 1 and a_radius < self.sizes[self.index + 1][0]:
            a_radius = self.sizes[self.index + 1][0]
        
        if self.index != 0 and b_radius < self.sizes[self.index - 1][0]:
            b_radius = self.sizes[self.index - 1][0]
            
        a_radius /= 4
        b_radius /= 4
        
        a_radius *= self.scale
        b_radius *= self.scale
        
        self.outline(surface, self.a, self.b, a_radius, b_radius)
        pygame.draw.circle(surface, (255, 0, 0), self.a, 3)
        pygame.draw.circle(surface, (0, 255, 0), self.b, 3)
        
        gfxdraw.aacircle(surface, int(self.a.x), int(self.a.y), int(a_radius/1.025), self.color)
        gfxdraw.aacircle(surface, int(self.b.x), int(self.b.y), int(b_radius/1.025), self.color)
        
        gfxdraw.filled_circle(surface, int(self.a.x), int(self.a.y), int(a_radius/1.025), self.color)
        gfxdraw.filled_circle(surface, int(self.b.x), int(self.b.y), int(b_radius/1.025), self.color)
    
    def outline(self, surface, n: pygame.Vector2, m: pygame.Vector2, n_radius, m_radius):
        n1, n2 = n.copy(), n.copy()
        m1, m2 = m.copy(), m.copy()
        
        n_angle, m_angle = math.atan2((m - n).y, (m - n).x), math.atan2((n - m).y, (n - m).x)
        
        n1.update(
            n.x + n_radius * math.cos(n_angle + math.pi/2), 
            n.y + n_radius * math.sin(n_angle + math.pi/2)
        )
        n2.update(
            n.x + n_radius * math.cos(n_angle - math.pi/2), 
            n.y + n_radius * math.sin(n_angle - math.pi/2)
        )
        
        m1.update(
            m.x + m_radius * math.cos(m_angle + math.pi/2), 
            m.y + m_radius * math.sin(m_angle + math.pi/2)
        )
        m2.update(
            m.x + m_radius * math.cos(m_angle - math.pi/2), 
            m.y + m_radius * math.sin(m_angle - math.pi/2)
        )
        
        points = [n1, n2, m1, m2]
        
        gfxdraw.aapolygon(surface, points, self.color)
        gfxdraw.filled_polygon(surface, points, self.color)