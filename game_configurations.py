from design_sets import colors
import random
import math

#---------------------기본 초기화--------------------------------
# 화면 및 게임 설정 상수
GAME_WIDTH = 1080
GAME_HEIGHT = 1920
BG_COLOR = colors['black']
MONO_BG_COLOR = colors['black']

# Border 설정 상수
CENTER = (550, 960)
RADIUS = 500
THICKNESS = 10

#Border 색 설정
INNER_COLOR = colors['black']  # 내부 색상
OUTER_COLOR = colors['white']  # 외부 색상
MONO_INNER_COLOR = colors['black']  # 내부 색상
MONO_OUTER_COLOR = colors['white']  # 외부 색상

#Ball 설정
BALL_POSITION = (540, 960)
BALL_SPEED = (2, 2)

BALL_RADIUS = 10

BALL_COLOR = colors['black']
MONO_BALL_COLOR = colors['black']

BALL_GROWTH = 1.1
BALL_ENERGY_LOSS = 1.01
BALL_GRAVITY = (0, 0.2)

#UNI 옵션 용
UNI_COLOR = random.choice(list(colors.values()))
UNI_BG_COLOR = colors['black']
UNI_INNER_COLOR = colors['black']

#복부 호동순 용 변수
OR10 = random.choice([0,1])
OR10_2 = random.choice([0,1])
#위치 초기화
def random_position_in_circle(center, radius):
    angle = random.uniform(0, 2 * math.pi)  # 0에서 360도 사이의 각도
    distance = random.uniform(0, radius)  # 원의 중심부터 반지름까지의 랜덤 거리
    x = center[0] + distance * math.cos(angle)
    y = center[1] + distance * math.sin(angle)
    
    return (int(x), int(y))

#---------------------추가적 초기화--------------------------------
# Randomly choose background color
def Mono_Setting():
    # Define color options
    color_options = [colors['black'], colors['white']]
    
    # Choose a random background color
    mono_bg_color = random.choice(color_options)
    
    # Determine the outer and inner colors based on the background color
    if mono_bg_color == colors['black']:
        mono_outer_color = colors['white']
        mono_inner_color = colors['black']
    else:
        mono_outer_color = colors['black']
        mono_inner_color = colors['white']
    
    # Set the ball color to be the same as the outer color
    mono_ball_color = mono_outer_color
    
    return mono_bg_color, mono_outer_color, mono_inner_color, mono_ball_color

#UNI 컬러 결정
def adjust_color_based_on_brightness(UNI_COLOR):
    #평균 밝기 계산
    brightness = sum(UNI_COLOR) / 3
    
    # 밝기에 따라 배경색과 내부 색상 설정
    if brightness < 128:  # 흑색에 가까운 경우
        UNI_BG = colors['white']  # 백색
        UNI_INNER = colors['white']  # 백색
    else:  # 백색에 가까운 경우
        UNI_BG = colors['black']  # 흑색
        UNI_INNER = colors['black']  # 흑색
    
    return UNI_BG, UNI_INNER

UNI_BG_COLOR, UNI_INNER_COLOR = adjust_color_based_on_brightness(UNI_COLOR)
MONO_BG_COLOR, MONO_OUTER_COLOR, MONO_INNER_COLOR, MONO_BALL_COLOR = Mono_Setting()
BALL_POSITION = random_position_in_circle(CENTER, RADIUS-BALL_RADIUS-THICKNESS-50)

# Ball 설정 - 초기 크기가 더 크고 점차 작아지는 설정
BALL_RADIUS_INITIAL_SHRINK = RADIUS  # 초기 반지름을 더 크게 설정
BALL_GROWTH_SHRINK = 0.97       # 성장률을 0.9로 설정하여 점차 작아짐
SHRINK_BALL_POSITION = (540, 960)

# 유형별 설정
configurations = {
    'fade_color_tracing': {
        'Game_setting': {
            'width': GAME_WIDTH,
            'height': GAME_HEIGHT,
            'bg_color': MONO_BG_COLOR,
        },
        
        'border': {
            'center': CENTER,
            'radius': RADIUS,
            'thickness': THICKNESS,
            'inner_color': MONO_INNER_COLOR,
            'outer_color': MONO_OUTER_COLOR,
        },
        
        'ball': {
            'position': BALL_POSITION,
            'speed': BALL_SPEED,
            'radius': BALL_RADIUS,
            'color': MONO_BALL_COLOR,
            'growth': BALL_GROWTH,
            'energy_loss': BALL_ENERGY_LOSS,
            'gravity': BALL_GRAVITY,
        },
        
        'gimmick': {
            'on_init' : {
                'BorderToggleGimmick' : OR10_2,
                },
            'on_collision': {
                'ColorSwapGimmick': 0,
                'LineMakeGimmick': 0, 
            },
            'on_move': {
                'BallBorderFadeGimmick' : OR10_2 * random.choice([0,1]),
                'BallFadeGimmick' : 1-OR10_2,
                'Tracer_Gimmick' : OR10,
                'PermanentTracerGimmick' : 1-OR10,
                
            }
        }
    },
    
    
    
    'fade_color_connect': {
        'Game_setting': {
            'width': GAME_WIDTH,
            'height': GAME_HEIGHT,
            'bg_color': MONO_BG_COLOR,
        },
        
        'border': {
            'center': CENTER,
            'radius': RADIUS,
            'thickness': THICKNESS,
            'inner_color': MONO_INNER_COLOR,
            'outer_color': MONO_OUTER_COLOR,
        },
        
        'ball': {
            'position': BALL_POSITION,
            'speed': BALL_SPEED,
            'radius': BALL_RADIUS,
            'color': MONO_BALL_COLOR,
            'growth': BALL_GROWTH,
            'energy_loss': BALL_ENERGY_LOSS,
            'gravity': BALL_GRAVITY,
        },
        
        'gimmick': {
            'on_init' : {
                'BorderToggleGimmick' : OR10,
                },
            'on_collision': {
                'ColorSwapGimmick': 0,
                'LineMakeGimmick': 1,
            },
            'on_move': {
                'BallBorderFadeGimmick' : OR10,
                'BallFadeGimmick' : 1-OR10,          
            }
        }
    },
    
    'fade_color_shrink': {
        'Game_setting': {
            'width': GAME_WIDTH,
            'height': GAME_HEIGHT,
            'bg_color': MONO_BG_COLOR,
        },
        'border': {
            'center': CENTER,
            'radius': RADIUS,
            'thickness': THICKNESS,
            'inner_color': MONO_INNER_COLOR,
            'outer_color': MONO_OUTER_COLOR,
        },
        'ball': {
            'position': SHRINK_BALL_POSITION,
            'speed': BALL_SPEED,
            'radius': BALL_RADIUS_INITIAL_SHRINK,
            'color': MONO_BALL_COLOR,
            'growth': BALL_GROWTH_SHRINK,
            'energy_loss': BALL_ENERGY_LOSS,
            'gravity': (0,0),
        },
        'gimmick': {
            'on_init': {
                'BorderToggleGimmick': OR10,
            },
            'on_collision': {
            },
            'on_move': {
                'ConnectGimmick': 1,
                'BallFadeGimmick' : 1-OR10,
                'BallBorderFadeGimmick' : OR10,
            }
        }
    },
    
    'uni_color_connect': {
        'Game_setting': {
            'width': GAME_WIDTH,
            'height': GAME_HEIGHT,
            'bg_color': UNI_BG_COLOR,
        },
        
        'border': {
            'center': CENTER,
            'radius': RADIUS,
            'thickness': THICKNESS,
            'inner_color': UNI_INNER_COLOR,
            'outer_color': UNI_COLOR,  
        },
        
        'ball': {
            'position': BALL_POSITION,
            'speed': BALL_SPEED,
            'radius': BALL_RADIUS,
            'color': UNI_COLOR,
            'growth': BALL_GROWTH,
            'energy_loss': BALL_ENERGY_LOSS,
            'gravity': BALL_GRAVITY,
        },
        
        'gimmick': {
            'on_init' : {
                'BorderToggleGimmick' : OR10,
                },
            'on_collision': {
                'ColorSwapGimmick': 0,
                'ConnectGimmick': 1,
            },
            'on_move': {       
                'ConnectGimmick': 1,
            }
        }
    },
    
    'uni_color_connect_shrink': {
        'Game_setting': {
            'width': GAME_WIDTH,
            'height': GAME_HEIGHT,
            'bg_color': UNI_BG_COLOR,
        },
        
        'border': {
            'center': CENTER,
            'radius': RADIUS,
            'thickness': THICKNESS,
            'inner_color': UNI_INNER_COLOR,
            'outer_color': UNI_COLOR,
        },
        
        'ball': {
            'position': SHRINK_BALL_POSITION,
            'speed': BALL_SPEED,
            'radius': BALL_RADIUS_INITIAL_SHRINK,  # 초기 크기가 더 큰 반지름
            'color': UNI_COLOR,
            'growth': BALL_GROWTH_SHRINK,  # 성장률을 0.9로 설정
            'energy_loss': BALL_ENERGY_LOSS,
            'gravity': (0,0),
        },
        
        'gimmick': {
            'on_init' : {'BorderToggleGimmick' : OR10},
            'on_collision': {'ConnectGimmick': 1, 'ColorSwapGimmick': 0},
            'on_move': {'ConnectGimmick': 1}
        }
    },
    
    'mono_swap': {#흑백 색깔바꿈
        'Game_setting': {
            'width': GAME_WIDTH,
            'height': GAME_HEIGHT,
            'bg_color': MONO_BG_COLOR,
        },
        
        'border': {
            'center': CENTER,
            'radius': RADIUS,
            'thickness': THICKNESS,
            'inner_color': MONO_INNER_COLOR,
            'outer_color': MONO_OUTER_COLOR,
        },
        
        'ball': {
            'position': BALL_POSITION,
            'speed': BALL_SPEED,
            'radius': BALL_RADIUS,
            'color': MONO_BALL_COLOR,
            'growth': BALL_GROWTH,
            'energy_loss': BALL_ENERGY_LOSS,
            'gravity': BALL_GRAVITY,
        },
        
        'gimmick': {
            'on_init' : {
                'BorderToggleGimmick' : 0,
                },
            'on_collision': {
                'ColorSwapGimmick': 1,
                'LineMakeGimmick': 0,
                
            },
            'on_move': {
                'BallBorderFadeGimmick' : 0,
                'BallFadeGimmick' : 0,
                'Tracer_Gimmick' : 1,
                'PermanentTracerGimmick' : 0,
                
            }
        }
    },
    'mono_tracing': {#흑백 채우기
        'Game_setting': {
            'width': GAME_WIDTH,
            'height': GAME_HEIGHT,
            'bg_color': MONO_BG_COLOR,
        },
        
        'border': {
            'center': CENTER,
            'radius': RADIUS,
            'thickness': THICKNESS,
            'inner_color': MONO_INNER_COLOR,
            'outer_color': MONO_OUTER_COLOR,
        },
        
        'ball': {
            'position': BALL_POSITION,
            'speed': BALL_SPEED,
            'radius': BALL_RADIUS,
            'color': MONO_BALL_COLOR,
            'growth': BALL_GROWTH,
            'energy_loss': BALL_ENERGY_LOSS,
            'gravity': BALL_GRAVITY,
        },
        
        'gimmick': {
            'on_init' : {
                'BorderToggleGimmick' : 0,
                },
            'on_collision': {
                'LineMakeGimmick': 0,
                
            },
            'on_move': {
                'Tracer_Gimmick' : OR10,
                'PermanentTracerGimmick' : 1-OR10,
                
            }
        }
    },
    
    'mono_connect': {#흑백 채우기
        'Game_setting': {
            'width': GAME_WIDTH,
            'height': GAME_HEIGHT,
            'bg_color': MONO_BG_COLOR,
        },
        
        'border': {
            'center': CENTER,
            'radius': RADIUS,
            'thickness': THICKNESS,
            'inner_color': MONO_INNER_COLOR,
            'outer_color': MONO_OUTER_COLOR,
        },
        
        'ball': {
            'position': BALL_POSITION,
            'speed': BALL_SPEED,
            'radius': BALL_RADIUS,
            'color': MONO_BALL_COLOR,
            'growth': BALL_GROWTH,
            'energy_loss': BALL_ENERGY_LOSS,
            'gravity': BALL_GRAVITY,
        },
        
        'gimmick': {
            'on_init' : {
                'BorderToggleGimmick' : 0,
                },
            'on_collision': {
                'ConnectGimmick': 1,
                
            },
            'on_move': {
                'PermanentTracerGimmick' : 0,
            }
        }
    },
    
    'mono_shrink': {
        'Game_setting': {
            'width': GAME_WIDTH,
            'height': GAME_HEIGHT,
            'bg_color': MONO_BG_COLOR,
        },
        'border': {
            'center': CENTER,
            'radius': RADIUS,
            'thickness': THICKNESS,
            'inner_color': MONO_INNER_COLOR,
            'outer_color': MONO_OUTER_COLOR,
        },
        'ball': {
            'position': SHRINK_BALL_POSITION,
            'speed': BALL_SPEED,
            'radius': BALL_RADIUS_INITIAL_SHRINK,
            'color': MONO_BALL_COLOR,
            'growth': BALL_GROWTH_SHRINK,
            'energy_loss': BALL_ENERGY_LOSS,
            'gravity': (0,0),
        },
        'gimmick': {
            'on_init': {
                'BorderToggleGimmick': 0,
            },
            'on_collision': {
                'ColorSwapGimmick': OR10,
            },
            'on_move': {
                'ConnectGimmick': 1-OR10,
            }
        }
    },
    
    }
