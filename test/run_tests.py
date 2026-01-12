"""테스트 실행 스크립트"""
import sys
import pytest


def run_all_tests():
    """모든 테스트 실행"""
    # 테스트 디렉토리
    test_dir = os.path.dirname(__file__)
    
    # pytest 실행 (verbose 모드)
    # -v: verbose, -s: 출력 표시, --tb=short: traceback 간략하게
    exit_code = pytest.main([test_dir, '-v', '--tb=short'])
    
    return exit_code


if __name__ == '__main__':
    sys.exit(run_all_tests())
