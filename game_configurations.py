from design_sets import colors
import random

Game_width = 1080
Game_height = 1920
BG_color = colors['black']



# 유형별 설정
configurations = {
    'color_tracing': {#무지개 흔적 남는 공
        
        'Game_setting' : {
            'width' : Game_width,
            'height' : Game_height,
            'bg_color' : BG_color,
        },
        
        'border': {
            'center': (550, 960),  # 고정된 중심 위치
            'radius': 350,  # 고정된 반지름
            'thickness': 10,  # 고정된 두께
            'inner_color': colors['black'],  # 내부 색상
            'outer_color': colors['white'],  # 외부 색상
        },
        
        'ball': {
            'position': (540, 960),  # 초기 위치
            'speed': (3, 3),  # 초기 속도
            'radius': 10,  # 공의 반지름
            'color': colors['black'],  # 랜덤 색상
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
                'ColorSwapGimmick': 0,
                'LineMakeGimmick': 0,
                
            },
            'on_move': {
                'GravityGimmick': 0,
                'TracerMakeGimmick': 0,
                'ColorFadeGimmick' : 1,
                
            }
        }
    },
    'mono-swap': {#흑백 색깔바꿈
        'border': {
            'center': (540, 960),  # 고정된 중심 위치
            'radius': 500,  # 고정된 반지름
            'thickness': 10,  # 고정된 두께
            'inner_color': colors['white'],  # 내부 색상
            'outer_color': colors['white'],  # 외부 색상
        },
        
        'ball': {
            'position': (550, 960),  # 초기 위치
            'speed': (5, 2),  # 초기 속도
            'radius': 10,  # 공의 반지름
            'color': colors['black'],  # 랜덤 색상
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
                'ColorFadeGimmick' : 0,
                
            }
        }
    },
    'mono-tracing': {#흑백 채우기
        'border': {
            'center': (540, 960),  # 고정된 중심 위치
            'radius': 350,  # 고정된 반지름
            'thickness': 1,  # 고정된 두께
            'inner_color': colors['white'],  # 내부 색상
            'outer_color': colors['black'],  # 외부 색상
        },
        
        'ball': {
            'position': (550, 460),  # 초기 위치
            'speed': (2, 2),  # 초기 속도
            'radius': 10,  # 공의 반지름
            'color': colors['black'],  # 랜덤 색상
            'growth': 1.1,  # 성장률
            'energy_loss': 1.01,  # 에너지 손실율
            'gravity': (0, random.choice([0, random.uniform(0, 1)])),
        },
        
        'gimmick': {
            'on_init' : {
                'BorderToggleGimmick' : 0,
                'Tracer_Gimmick' : 1,
                },
            'on_collision': {
                'ColorSwapGimmick': 0,
                'LineMakeGimmick': 0,
                
            },
            'on_move': {
                'GravityGimmick': 0,
                'ColorFadeGimmick' : 0,
               
            }
        }
    },
    
    'line-bouncing': {#흑백 채우기
        'border': {
            'center': (540, 960),  # 고정된 중심 위치
            'radius': 350,  # 고정된 반지름
            'thickness': 10,  # 고정된 두께
            'inner_color': colors['black'],  # 내부 색상
            'outer_color': colors['green'],  # 외부 색상
        },
        
        'ball': {
            'position': (550, random.choice([700, 960])), # 초기 위치
            'speed': (7, 2),  # 초기 속도
            'radius': 10,  # 공의 반지름
            'color': colors['green'],  # 랜덤 색상
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
                'ColorSwapGimmick': 0,
                'LineMakeGimmick': 0,
                'Sound_Gimmick' : 'springy-bounce-86214.mp3',
            },
            'on_move': {
                'GravityGimmick': 0,
                'ColorFadeGimmick' : 1,
                'ConnectGimmick' : 1,
            }
        }
    },
}
