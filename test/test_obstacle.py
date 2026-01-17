"""Obstacle 클래스 테스트"""
import pytest
from obstacle import Obstacle
from constants import GRID_WIDTH, GRID_HEIGHT


class TestObstacle:
    def test_obstacle_creation(self):
        """장애물 생성 테스트"""
        snake_body = [(15, 15), (14, 15), (13, 15)]
        food_pos = (10, 10)
        obstacle = Obstacle(5, snake_body, food_pos)
        
        assert len(obstacle.get_positions()) == 5
    
    def test_obstacle_no_overlap_with_snake(self):
        """장애물이 뱀과 겹치지 않는지 테스트"""
        snake_body = [(15, 15), (14, 15), (13, 15)]
        food_pos = (10, 10)
        obstacle = Obstacle(5, snake_body, food_pos)
        
        for pos in obstacle.get_positions():
            assert pos not in snake_body
    
    def test_obstacle_no_overlap_with_food(self):
        """장애물이 먹이와 겹치지 않는지 테스트"""
        snake_body = [(15, 15), (14, 15), (13, 15)]
        food_pos = (10, 10)
        obstacle = Obstacle(5, snake_body, food_pos)
        
        assert food_pos not in obstacle.get_positions()
    
    def test_obstacle_within_bounds(self):
        """장애물이 그리드 범위 내에 있는지 테스트"""
        snake_body = [(15, 15)]
        food_pos = (10, 10)
        obstacle = Obstacle(10, snake_body, food_pos)
        
        for pos in obstacle.get_positions():
            x, y = pos
            assert 0 <= x < GRID_WIDTH
            assert 0 <= y < GRID_HEIGHT
    
    def test_obstacle_collision_detection(self):
        """장애물 충돌 감지 테스트"""
        snake_body = [(15, 15)]
        food_pos = (10, 10)
        obstacle = Obstacle(3, snake_body, food_pos)
        
        positions = obstacle.get_positions()
        # 장애물 위치와 충돌하면 True
        assert obstacle.check_collision(positions[0]) == True
        
        # 장애물 없는 위치는 False
        assert obstacle.check_collision((0, 0)) == False
    
    def test_zero_obstacles(self):
        """장애물 0개 생성 테스트"""
        snake_body = [(15, 15)]
        food_pos = (10, 10)
        obstacle = Obstacle(0, snake_body, food_pos)
        
        assert len(obstacle.get_positions()) == 0
