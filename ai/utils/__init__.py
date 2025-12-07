from .game_api import GameAPI

"""
Package d'utilitaires pour l'IA
"""
from .geometry import (
    Point,
    Rectangle,
    Circle,
    distance_between,
    manhattan_distance,
    chebyshev_distance,
    angle_between_points,
    point_in_rect,
    rectangles_overlap,
    line_intersection,
    closest_point_on_segment,
    grid_to_world,
    world_to_grid,
    get_direction_vector,
    calculate_bounding_box,
    point_in_polygon,
    is_point_visible,
    lerp,
    lerp_point,
    calculate_centroid
)
__all__ = ['GameAPI',
           'Point',
    'Rectangle',
    'Circle',
    'distance_between',
    'manhattan_distance',
    'chebyshev_distance',
    'angle_between_points',
    'point_in_rect',
    'rectangles_overlap',
    'line_intersection',
    'closest_point_on_segment',
    'grid_to_world',
    'world_to_grid',
    'get_direction_vector',
    'calculate_bounding_box',
    'point_in_polygon',
    'is_point_visible',
    'lerp',
    'lerp_point',
    'calculate_centroid']