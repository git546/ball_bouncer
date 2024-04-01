from design_sets import colors
import random

# 유형별 설정
configurations = {
    'color_tracing': {#무지개 흔적 남는 공
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
            'color': colors['black'],  # 랜덤 색상
            'growth': 1.1,  # 성장률
            'energy_loss': 1.01,  # 에너지 손실율
            'gravity': (0, random.choice([0, random.uniform(0, 1)])),
        },
        
        'gimmick': {
            'on_init' : {
                'BorderToggleGimmick' : 1,
                'Tracer_Gimmick' : 1,
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
    },
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
            'gravity': (0, random.choice([0, random.uniform(0, 1)])),
        },
        
        'gimmick': {
            'on_init' : {
                'BorderToggleGimmick' : 0,
                'Tracer_Gimmick' : 0,
                },
            'on_collision': {
                'ColorSwapGimmick': 1,
                'LineMakeGimmick': 0,
                
            },
            'on_move': {
                'GravityGimmick': 0,
                'TracerMakeGimmick': 0,
                'ColorFadeGimmick' : 0,
                
            }
        }
    },
}
