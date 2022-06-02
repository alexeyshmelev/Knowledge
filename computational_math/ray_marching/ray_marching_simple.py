import time
import numpy as np
import taichi as ti
from shader_funcs import *

ti.init(arch=ti.opengl)
# ti.init(arch=ti.gpu)
# ti.init(arch=ti.cpu)

# Resolution and pixel buffer

asp = 16/9
h = 720
w = int(asp * h)
res = w, h
AA = 2

# Fields (should always be before first call of any taichi scope kernels)

global_time = ti.field(dtype=ti.f32, shape=())
mouse_pos = ti.Vector.field(2, dtype=ti.f32, shape=())
mouse_btn = ti.field(dtype=ti.i32, shape=(2, ))
mouse_btn_prev = ti.field(dtype=ti.i32, shape=(2, ))
flags = ti.field(dtype=ti.i32, shape=(8, ))
materials = ti.Vector.field(3, dtype=ti.f32, shape=(10,))
pixels = ti.Vector.field(3, dtype=ti.f32, shape=res)
flag = ti.field(dtype=ti.f32, shape=())

materials.from_numpy(np.array([[1.0, 0.7, 0.0],  # cube color without texture
                               [0.08, 0.8, 0.8],  # floor color
                               [0.1, 0.2, 0.7],  # torus color
                               [0.6, 0.7, 0.6],  # plane color
                               [1.0, 0.0, 0.0],  # vertical capsule color
                               [0.0, 1.0, 0.0],  # rounded cylinder color
                               [0.0, 0.0, 1.0],  # rounded octahedron color
                               [0.0, 0.7, 1.0],
                               [0.0, 0.0, 0.0],  # border color (toon shading)
                               [0.5, 0.8, 0.9]   # background
                               ], dtype=np.float32))


@ti.func
def texture(uv, s):
    """
    Задание текстуры
    :param uv: плоскость для отрисовка текстуры
    :param s: количество колебаний
    :return: цвет текстуры в данной очке
    """
    d = sd_box(uv, vec2(1.))
    col = vec3(0.)
    if d < 0:
        col = vec3(1.0, 0.6, 0.1)
        col *= 0.8 + 0.2 * skewsin(s * d, 0.8)
        col *= 1.0 - ti.exp(-7.0 * abs(d))
    return col


@ti.func
def boxmap_texture(p, n, k, s):
    """
    Наложение текстры на куб
    :param p: точка на кубе
    :param n: нормаль
    :param k: коэффициент смешивания проекций (для кубика не важно, так как в его гранях есть очень резкий переход в нормалях)
    :param s: количество колебаний (для текстуры)
    :return: цвет текстуры
    """
    xcol = texture(vec2(p.y, p.z), s)
    ycol = texture(vec2(p.z, p.x), s)
    zcol = texture(vec2(p.x, p.y), s)
    w = abs(n)**k
    return (xcol * w.x + ycol * w.y + zcol * w.z) / w.sum()


@ti.func
def rotate_cube(p):
    """
    Поворот кубика
    :param p: точка на луче rd (на поверхности какой-то фигуры)
    :return: перенесённая точка после поворота
    """
    t = global_time[None]
    m = rot_x(1. * t)
    return m @ p


@ti.func
def translate_cube(p):
    """
    Параллельный перенос кубика
    :param p: точка на луче rd (на поверхности какой-то фигуры)
    :return: перенесённая точка после параллельного переноса
    """
    t = global_time[None]
    return p - vec3(ti.sin(1. * t), 0., 0.)


@ti.func
def dist_vector(p):
    """
    Нахождение расстояния до всех объектов в сцене
    :param p: точка на луче rd (на поверхности какой-то фигуры)
    :return: вектор с расстояниями до всех объектов в сцене
    """
    d1 = sd_box(translate_cube(rotate_cube(p)), vec3(0.5))
    d2 = p.y + 1.5
    d3 = sd_torus(p, vec2(5., 0.5))
    d4 = sd_plane(p, vec3(0.5), 6.)
    d5 = sd_verticalCapsule(p-2, vec3(2), 0.2)
    d6 = sd_roundedCylinder(p+vec3(2., -2., 2.), 0.1, 0.1, 2.)
    d7 = sd_Octahedron(p+vec3(-1., -2., -4.), 2.)
    d8 = sd_Link(p+vec3(-1., -2., 4.), 1.6, 0.4, 0.1)
    return vec8(d1, d2, d3, d4, d5, d6, d7, d8)


@ti.func
def dist(p):
    """
    Нахождение минимального расстояния среди расстояний до всех объектов в сцене
    :param p: точка на луче rd (на поверхности какой-то фигуры)
    :return: минимальное расстояния среди расстояний до всех объектов в сцене
    """
    return dist_vector(p).min()


@ti.func
def dist_mat(p):
    """
    Нахождение материала и его индекса в массиве материалов
    :param p: точка на луче rd (на поверхности какой-то фигуры)
    :return: материала и его индекс в массиве материалов
    """
    return argmin(dist_vector(p))


MAX_STEPS = 100
MAX_DIST = 200.
EPS = 1e-3


@ti.func
def ambient_occlusion(p, n):
    """
    Тень от глобального освещение. Как работает: берут несколько точек на луче (недалеко от точки p), попавшем в точку p, считают два расстояния (до точки p и до ближайшей поверхности),
    на каждом шаге применяют какой-то коэффициент затухания и по сумме этих вычислений находят общий результат затенения точки p
    :param p: точка на луче rd (на поверхности какой-то фигуры)
    :param n: нормаль
    :return: вклад глобального затенения в цвет
    """
    occ = 0.
    weight = 1.
    for i in range(8):
        len = 0.01 + 0.02 * i ** 2
        d = dist(p + n * len)*2.
        occ += (len - d) * weight
        weight += 0.85

    return 1. - clamp(0.6 * occ, 0., 0.8)


@ti.func
def raymarch(ro, rd):
    """
    :param ro: точка испускания луча
    :param rd: направления в точку падения
    :return: расстояние, индекс материала, точка на луче rd

    """
    p = vec3(0.)
    d = 0.
    mat_i = 0
    for i in range(MAX_STEPS):
        p = ro + d * rd
        ds, mat_i = dist_mat(p) # mat_i
        d += ds
        if ds < EPS:
            break
        if d > MAX_DIST:
            mat_i = -1
            break
    return d, mat_i, p


@ti.func
def raymarch_outline(ro, rd, ow):
    """
    Основоной алгоритм реализации трёхмерной графики. Как работает: для каждого покселя испускается луч, далее мы начинаем по нему перемещаться с шагом, равным минимальному расстоянию до какого-либо объекта,
    далее так как все фигуры у нас задаются процедурно (т.е. функциями, которые как раз возвращают нам расстояние от той точке на луче, где мы остановились, до границы конкретной фигуры), если
    расстояние становится меньше EPS, то argmin нам даёт фигуру и номер цвета из materials)
    :param ro: где расположена камера
    :param rd: направление в сторону каждого пикселя на экране (он идёт дальше, пока не пересечёт какой-то объект)
    :param ow: расстояние, на котором рисуется граница
    :return: длина вектора rd, материал, точка на луче rd (на поверхности какой-то фигуры)
    """
    p = ro
    d = 0.
    ds, mat_i = dist_mat(p)
    min_dist = ds
    mat_i = 0
    for i in range(MAX_STEPS):
        min_dist = min(min_dist, ds)
        d += ds
        p = ro + d * rd
        ds, mat_i = dist_mat(p)
        if ds < EPS:
            break
        if d > MAX_DIST:
            mat_i = -1
            break
        if ds > min_dist and min_dist < ow:
            mat_i = -2
            break
    return d, mat_i, p


e_x = vec3(EPS, 0., 0.)
e_y = vec3(0., EPS, 0.)
e_z = vec3(0., 0., EPS)


@ti.func
def normal(p, rd):
    """
    Вычисление нормали к поверхности
    :param p: точка на луче rd (на поверхности какой-то фигуры)
    :param rd: направление в сторону каждого пикселя на экране (он идёт дальше, пока не пересечёт какой-то объект)
    :return: нормаль к поверхности
    """
    n = dist(p) - vec3(dist(p - e_x), dist(p - e_y), dist(p - e_z))
    return normalize(n - max(0., dot(n, rd)) * rd)


@ti.func  # блик
def phong(n, rd, ld, sh):
    """
    Рассчёт коэффициентов для блика от свещение на поверхности фигуры
    :param n: нормаль к поверхности
    :param rd: направление в сторону каждого пикселя на экране (он идёт дальше, пока не пересечёт какой-то объект)
    :param ld: направление луча от лампы
    :param sh: коэффициент
    :return: коэффициенты для блика
    """
    diff = max(dot(n, ld), 0.)  # ld - direction of light from lamp
    r = reflect(-ld, n)
    v = -rd
    spec = max(dot(r, v), 0.)**sh
    return diff, spec


@ti.func
def soft_shadow(ro, rd, k=2.):
    """
    Рассчёт мягких теней
    :param ro: где расположена камера
    :param rd: направление в сторону каждого пикселя на экране (он идёт дальше, пока не пересечёт какой-то объект)
    :param k: коэффициент
    :return: вклад тени в цвет
    """
    d = EPS * 20
    res = 1.
    for i in range(MAX_STEPS):
        ds = dist(ro + d * rd)
        d += ds
        if d > MAX_DIST:
            break
        if ds < EPS:
            res = 0.
            break
        res = min(res, k*ds/d)
    return res


@ti.func
def sharp_shadow(ro, rd):
    """
    Рассчёт резких теней
    :param ro: где расположена камера
    :param rd: направление в сторону каждого пикселя на экране (он идёт дальше, пока не пересечёт какой-то объект)
    :return: вклад тени в цвет
    """
    sh = 1.
    d = 0.
    for i in range(MAX_STEPS):
        ds = dist(ro + d * rd)
        d += ds
        if ds < EPS:
            sh = 0.
            break
        if d > MAX_DIST:
            break
    return sh


@ti.func
def render_custom(ro, rd, pr_mat):  # ro: vec3, rd: vec3, t: ti.f32
    """
    Определение цвета каждого пикселя
    :param ro: где расположена камера
    :param rd: направление в сторону каждого пикселя на экране (он идёт дальше, пока не пересечёт какой-то объект)
    :param pr_mat: предыдущий материал
    :return: цвет пикселя, точка падения луча на объект, отражённый луч, материал
    """
    # d, mat_i, p = raymarch(ro, rd)
    d, mat_i, p = raymarch_outline(ro, rd, 0.05)
    n = normal(p, rd)
    r = reflect(rd, n)
    occ = ambient_occlusion(p, n)
    col = vec3(0.)
    lp = vec3(5., 5., -5.)  # lamp position
    ld = normalize(lp - p)
    mat_n = materials.shape[0]
    background = materials[mat_n - 1] - abs(rd.y)
    mate = materials[mat_i]
    coeff_of_reflect = 1.

    if pr_mat == 2 and mat_i != 2 or pr_mat == 2 and mat_i == 2:
        col = vec3(0., 0., 0.)
    elif pr_mat == 4 and mat_i != 4 or pr_mat == 4 and mat_i == 4:
        col = vec3(0., 0., 0.)
    elif pr_mat == 5 and mat_i != 5 or pr_mat == 5 and mat_i == 5:
        col = vec3(0., 0., 0.)
    else:

        if mat_i >= mat_n - 2:
            col = mate  # background, outline
        else:
            diff, spec = phong(n, rd, ld, 16)

            if mat_i == 0:
                mate = boxmap_texture(translate_cube(rotate_cube(p)), rotate_cube(n), 60, 32.)
                diff = ti.ceil(diff*2.)/2.
            if mat_i == 2:
                diff = ti.ceil(diff * 2.) / 2.
                pass

            shad = sharp_shadow(p + n * EPS, ld)
            if flag[None] != 0.:
                shad = soft_shadow(p + n * EPS, ld)
            k_a = 0.3
            k_d = 1.0
            k_s = 1.5  # 1.5
            amb = mate
            dif = diff * mate
            spe = spec * vec3(1.)
            col = coeff_of_reflect * (k_a * amb * occ + (k_d * dif + k_s * spe * occ) * shad)
        #fog
        col = mix(col, background, smoothstep(20., 50., d))

    ro = p + n*0.1
    rd = r
    return col, ro, rd, mat_i


@ti.kernel
def main_image():
    """
    Рендер картинки
    :return: цвет пикселя после анти-алиасинга
    """
    t = global_time[None]
    background = materials[-1]
    mp = ti.static(mouse_pos)
    muv = 2 * np.pi * (mp[None] - 0.5)

    m = rot_y(muv.x)
    ro = m @ vec3(0., 2., -10. + 10*muv.y)  # 1 и 3 координата (отвечают за позицию в плоскости пола) вместе с s влияют на удаление камеры от точки вращения
    la = vec3(0., -1., 0.)  # 2 координата вместе с 2 координатой из ro влияет одновременно на наклон и положение камеры по оси Oz (в 3D сцене)
    up = vec3(0., 1., 0.)  # направление вверх (в 3D сцене)
    c, r, u = lookat(ro, la, up, 0.5)

    for fragCoord in ti.grouped(pixels):
        col = vec3(0.)
        for i in range(AA):
            for j in range(AA):
                uv = (fragCoord + vec2(i, j) / AA - 0.5 * vec2(res)) / res[1]
                rd = normalize(c + uv.x * r + uv.y * u)
                pr_mat = -10
                col1, ro1, rd1, pr_mat = render_custom(ro, rd, pr_mat)
                col2, ro2, rd2, pr_mat = render_custom(ro1, rd1, pr_mat)
                if all(col1 <= vec3(0.07, 0.07, 0.07)):
                    col = col1
                else:
                    col += (col1 + col2) / 2.
        col /= AA**2
        # gamma correction, clamp, write to pixel
        pixels[fragCoord] = clamp(col ** (1 / 2.2), 0., 1.)


fr = 0
video_manager = ti.tools.VideoManager(output_dir="./results", framerate=30, automatic_build=False)

gui = ti.GUI("Taichi ray marching shader", res=res, fast_gui=True)
start = time.time()

while gui.running:
    if gui.get_event(ti.GUI.PRESS):
        if gui.event.key == ti.GUI.ESCAPE:
            break

    mpos = gui.get_cursor_pos()  # [0..1], [0..1]
    mouse_pos[None] = [np.float32(mpos[0]), np.float32(mpos[1])]

    if gui.is_pressed(ti.ui.RMB):
        flag[None] = 1.
    else:
        flag[None] = 0.

    global_time[None] = time.time() - start

    # с записью видео

    if fr < 600:
        main_image()
        pixels_img = pixels.to_numpy()
        video_manager.write_frame(pixels_img)
        gui.set_image(pixels)
        gui.show()
        fr += 1
    else:
        video_manager.make_video(gif=False, mp4=True)
        exit()

    # без записи видео

    # main_image()
    # gui.set_image(pixels)
    # gui.show()

gui.close()