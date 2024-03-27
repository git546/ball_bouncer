from design_sets import colors
import random

# 유형별 설정
configurations = {
    'type1': {
        'color': lambda: random.choice(list(colors.values())),  # 랜덤 색상 선택
        'gimmick': 'ColorSwapGimmick',
    },
    'type2': {
        'color': lambda: colors['white'],  # 고정 색상 선택
        'gimmick': 'GravityGimmick',
    },
    # 추가 유형 정의...
}
