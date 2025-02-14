## 홀 센서 시스템 가능성 파악

**(1) 아두이노, 홀 센서 베드 구축**

- 하드웨어 구성 요소
    - 아두이노 나노 - ATmega328P 기반
        - 센서 데이터를 수집하고 처리하기 위한 중앙 처리 장치
    - 홀 센서 - SparkFun TMAG5273
        - 자기장 감지 센서
        - 3D → 위치 및 방향 정보를 수집
- 아두이노 IDE
    - 사용 버전 - 2.3.4
    - Library Manager를 통해 홀 센서 관련 example을 실행할 수 있는 라이브러리 설치 가능
    
- 홀 센서 핀 커넥터 납땜, 아두이노 나노와 연결
    - 3V3 → 3.3V
    - SDA -> A4
    - SCL -> A5
    - GND → GND
- 홀 센서 사용 관련 링크
    - docs
        https://github.com/sparkfun/SparkFun_Qwiic_Hall_Effect_Sensor_TMAG5273/blob/main/docs/example_basic.md
        
    - examples
        https://github.com/sparkfun/SparkFun_TMAG5273_Arduino_Library/tree/main/examples/Example1_BasicReadings
        
    - 데이터 시트
        https://docs.sparkfun.com/SparkFun_Qwiic_Hall_Effect_Sensor_TMAG5273/assets/component_documentation/tmag5273.pdf
        
- Mac 아두이노 나노 USB 연결 실패 문제
    - 드라이브 설치로 해결
    - 관련 링크
        - https://m.blog.naver.com/redcrow/222844030669
        - https://github.com/adrianmihalko/ch340g-ch34g-ch34x-mac-os-x-driver/blob/master/CH34x_Install_V1.5.pkg

**(2) 자기장 값 시각화 및 사용 거리 파악**

- 자기장 데이터 수집
    - 기존 라이브러리 example 코드 문제 해결
        - 라이브러리에 정의되어 X, Y, Z값을 가져올 수 있는 getXdata(), getYdata(), getZdata()함수 등이 잘 작동하지 않았다.
            
        - → 데이터시트에 적힌 data definition과 address를 사용해 데이터를 직접 가져오도록 코드 작성 → `get_XYZ_data.ino`
    - sampling 주기
        - 여러 시도 중 0.5초마다 한번씩 값을 받아오는게 가장 인식이 잘 됐다.
        - 왜 그런지 이유는 아직 찾지 못했다.
- 자기장 데이터 시각화, 분석
    - 시리얼 통신을 통해 파이썬으로 값 플롯
        - https://coding-kindergarten.tistory.com/179
            - `plot_3Ddata_hall_sensor.py`
            - `plot_2Ddata_hall_sensor.py`
    - 분석 및 결과
        - 1~2cm의 가까운 거리에서만 위치나 방향이 감지됨
        - 멀리서도 감지가 가능한지에 대한 기존 사례와 자료 조사 필요
        - 향후 강한 자석 또는 전자석을 사용하는 방법 검토 필요

**(3) 기존 사용 예시 자료 수집**

- 방향 감지x, 근접 감지용
    - 문 열림, 닫힘 인식
    
    https://www.youtube.com/watch?v=FUs4BphJiW0
    
- 3D 홀센서 전체적인 설명, 실습, plotting 동영상
    - 현재 사용하고 있는 홀 센서와 같은 TMAG5273 모델 사용
    - +-133mT, 강한 자석을 사용하는 것 같다
    - 거리가 좀 떨어져도 인식은 가능하지만 가까이 대고 조금 있어야 값이 변화하는 건 마찬가지인듯
    - 바로 바로 변하는 위치 변화를 감지 가능한지 예제를 더 찾아봐야 할 것 같음
    
    https://www.youtube.com/watch?v=IBSCZk4g4Tk
    
- 손끝에 센서나 자석을 배치하는 것이 아니라 접힘 펴짐 감지를 위해 관절 바깥쪽에 자석과 홀센서를 배치
    - 이렇게 하면 가까워야 감지되는 것을 잘 응용할 수 있다.
    - 하지만 3D 홀센서의 이점을 잘 못살릴 듯하다.
    
- shadow robot 홀 센서 장갑
    - 가볍고, 간단, 정확
    - https://youtu.be/2ggpvigfEZE?feature=shared
    - https://youtu.be/3rZYn62OId8?feature=shared

- 멀리서 방향 감지 예시
    - TMAG5170 사용 → 현재 사용중인 센서와 큰 차이 없어보인다.
    - 더 큰 자석 사용
    
    https://www.youtube.com/watch?v=gMiJQeULRNU