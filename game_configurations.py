from design_sets import colors
import random

# 유형별 설정
configurations = {
    'mono-swap': {#흑백 색깔바꿈
        'border': {
            'center': (450, 300),  # 고정된 중심 위치
            'radius': 250,  # 고정된 반지름
            'thickness': 10,  # 고정된 두께
            'inner_color': colors['black'],  # 내부 색상
            'outer_color': colors['white'],  # 외부 색상
        },
        
        'ball': {
            'position': (450, 150),  # 초기 위치
            'speed': (3, 3),  # 초기 속도
            'radius': 10,  # 공의 반지름
            'color': colors['white'],  # 랜덤 색상
            'growth': 1.1,  # 성장률
            'energy_loss': 1.01,  # 에너지 손실율
            'gravity': (0, 0.0),
        },
        
        'gimmick': {
            'on_init' : {
                'BorderToggleGimmick' : 1, 
                },
            'on_collision': {
                'ColorSwapGimmick': 0,
                'LineMakeGimmick': 0,
                
            },
            'on_move': {
                'GravityGimmick': 0,
                'TracerMakeGimmick': 1,
                'ColorFadeGimmick' : 1,
                
            }
        }
    }
}
