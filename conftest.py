"""pytest 설정 파일 - 프로젝트 루트를 자동으로 sys.path에 추가"""
import sys
import os

# 프로젝트 루트 디렉토리를 sys.path에 추가
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# pygame headless 모드 설정
os.environ['SDL_VIDEODRIVER'] = 'dummy'
