import pyaudio

p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
num_devices = info.get('deviceCount')

for i in range(num_devices):
    device_info = p.get_device_info_by_host_api_device_index(0, i)
    if device_info.get('maxInputChannels') > 0:
        print(f"Input Device id {i} - {device_info.get('name')}")

# 입력 장치 ID를 확인한 후, 해당 ID를 사용하여 PyAudio 스트림을 설정
input_device_index = int(input("Enter the ID of the virtual audio input device: "))
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=44100,
                input=True,
                input_device_index=input_device_index,
                frames_per_buffer=1024)

print("Recording...")
frames = []
try:
    for _ in range(0, int(44100 / 1024 * 5)):  # 5초 동안 녹음
        data = stream.read(1024)
        frames.append(data)
finally:
    print("Finished recording.")

    # 스트림 닫기
    stream.stop_stream()
    stream.close()
    p.terminate()
