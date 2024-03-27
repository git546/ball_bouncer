from design_sets import colors
import random

# 유형별 설정
configurations = {
    'type1': {
        'border': {
            'center': (450, 300),  # 고정된 중심 위치
            'radius': 250,  # 고정된 반지름
            'thickness': 10,  # 고정된 두께
            'inner_color': colors['white'],  # 내부 색상
            'outer_color': colors['black'],  # 외부 색상
        },
        'ball': {
            'position': (450, 150),  # 초기 위치
            'speed': (3, 3),  # 초기 속도
            'radius': 10,  # 공의 반지름
            'color': colors['black'],  # 랜덤 색상
            'growth': 1.1,  # 성장률
            'energy_loss': 1.01,  # 에너지 손실율
            'gravity': (0, 0.5),
        },
        'gimmick': 'ColorSwapGimmick',
    }
    # 추가 유형 설정...
}
