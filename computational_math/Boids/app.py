import numpy as np
import ffmpeg
from datetime import datetime
from vispy import app, scene
from vispy.scene.visuals import Text
from functions import *
import os
from numba import cuda
os.environ['CUPY_ACCELERATORS'] = 'cub,cutensor'


app.use_app('pyglet')
asp = 16 / 9
h = 720
w = int(asp * h)
canvas = scene.SceneCanvas(keys='interactive', show=True, size=(w, h))
view = canvas.central_widget.add_view()
view.camera = scene.PanZoomCamera(rect=(0, 0, asp, 1), aspect=1)
face = "Times New Roman"
video = True
frames = 0
counter_mod = 0
N = 100
dt = 0.05
perception = 1./20
vrange = np.array([0.05, 0.1])
arange = np.array([0., 1.0])

t1 = Text("text", parent=canvas.scene, color='orange')
t1.font_size = 18
t1.pos = canvas.size[0] // 2, canvas.size[1] - 20

# x, y, vx, vy, ax, ay
boids = np.zeros((N, 6), dtype=np.float64)
init_boids(boids, asp, vrange)
arrows = scene.Arrow(arrows=directions(boids), arrow_color=(1, 1, 1, 1), arrow_size=5, connect='segments', parent=view.scene)
scene.Line(pos=np.array([[0, 0], [asp, 0], [asp, 1], [0, 1], [0, 0]]),color=(0, 1, 0, 1), connect='strip', method='gl', parent=view.scene)
scene.GridLines((1/6, 1/6), parent=view.scene)


if video:
    fname = f"boids_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
    print(fname)

    process = (
        ffmpeg
            .input('pipe:', format='rawvideo', pix_fmt='rgb24', s=f"{w}x{h}", r=60)
            .output(fname, pix_fmt='yuv420p', preset='slower', r=60)
            .overwrite_output()
            .run_async(pipe_stdin=True)
    )

threadsperblock = (32, 32)
blockspergrid_x = math.ceil(N / threadsperblock[0])
blockspergrid_y = math.ceil(N / threadsperblock[1])
blockspergrid = (blockspergrid_x, blockspergrid_y)
D = cuda.to_device(np.zeros((N, N), dtype=np.float64))
left = cuda.to_device(np.zeros(N, dtype=np.float64))
right = cuda.to_device(np.zeros(N, dtype=np.float64))
bottom = cuda.to_device(np.zeros(N, dtype=np.float64))
top = cuda.to_device(np.zeros(N, dtype=np.float64))
ax = cuda.to_device(np.zeros(N, dtype=np.float64))
ay = cuda.to_device(np.zeros(N, dtype=np.float64))
wa = cuda.to_device(np.zeros((N, 2), dtype=np.float64))
accels = cuda.to_device(np.zeros((N, 5, 2), dtype=np.float64))
tmp = cuda.to_device(np.zeros((N, N, 2), dtype=np.float64))
counter = cuda.to_device(np.zeros(N, dtype=np.float64))
counter2d = cuda.to_device(np.zeros((N, 2), dtype=np.float64))


def update(event):
    global process, boids, D, accels, frames, counter_mod
    frames += 1
    counter_mod += 1
    coeffs = np.array([1,  # alignment
                       0.1,  # cohesion
                       math.sin(counter_mod/100)/10,  # separation
                       0.001,  # walls
                       0.  # noise
                       ], dtype=np.float64)
    coeffs = cuda.to_device(coeffs)
    boids = cuda.to_device(boids)
    new_simulate[blockspergrid, threadsperblock](boids, D, perception, asp, coeffs, left, right, bottom, top, wa, accels, tmp, counter, counter2d)
    boids = boids.copy_to_host()
    coeffs = coeffs.copy_to_host()
    propagate(boids, dt, vrange)
    periodic_walls(boids, asp)
    arrows.set_data(arrows=directions(boids))
    t1.text = f"FPS (GPU): {canvas.fps:0.1f}, coefficients: {coeffs[0]}, {coeffs[1]}, {coeffs[2]}, {coeffs[3]}, {coeffs[4]}, number of boids: {N}"
    if video:
        frame = canvas.render(alpha=False)
        process.stdin.write(frame.tobytes())
    else:
        canvas.update(event)
    if frames > 3600:
        exit()


timer = app.Timer(interval=0, start=True, connect=update)

if __name__ == '__main__':
    canvas.measure_fps()
    app.run()
    if video:
        process.stdin.close()
        process.wait()