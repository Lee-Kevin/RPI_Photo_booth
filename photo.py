import picamera
import time
import itertools

s = " Say 'ReSpeaker' to take a photo "

camera = picamera.PiCamera()
camera.resolution = (1366, 768)
camera.framerate = 24
camera.start_preview()
camera.annotate_text = ' ' * 20
camera.annotate_text_size = 28

start_time = time.time()
for c in itertools.cycle(s):
    camera.annotate_text = camera.annotate_text[1:20] + c
    time.sleep(0.1)
    if  time.time() - start_time > 10:
        break
count_down = '12345'
camera.annotate_text_size = 160
for c in count_down:
    camera.annotate_text = c
    time.sleep(1)
    
camera.annotate_text = ''
camera.capture('new.jpg')
camera.annotate_text = 'Printing...'
camera.annotate_text_size = 140
time.sleep(3)
time.sleep(3)
camera.stop_preview()
