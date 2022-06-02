import taichi as ti
import math

vec1 = ti.types.vector(1, ti.f32)
vec2 = ti.types.vector(2, ti.f32)
vec3 = ti.types.vector(3, ti.f32)
vec4 = ti.types.vector(4, ti.f32)
vec5 = ti.types.vector(5, ti.f32)
vec6 = ti.types.vector(6, ti.f32)
vec7 = ti.types.vector(7, ti.f32)
vec8 = ti.types.vector(8, ti.f32)
vec9 = ti.types.vector(9, ti.f32)
vec10 = ti.types.vector(10, ti.f32)
vec11 = ti.types.vector(11, ti.f32)
vec12 = ti.types.vector(12, ti.f32)
vec13 = ti.types.vector(13, ti.f32)
vec14 = ti.types.vector(14, ti.f32)
vec15 = ti.types.vector(15, ti.f32)
vec16 = ti.types.vector(16, ti.f32)

mat2 = ti.types.matrix(2, 2, ti.f32)
mat3 = ti.types.matrix(3, 3, ti.f32)
mat4 = ti.types.matrix(4, 4, ti.f32)

tmpl = ti.template()

twopi = 2 * math.pi
pi180 = math.pi / 180.


@ti.func
def length(p):
    """
    Длина вектора
    :param p: точка на луче rd  (на поверхности какой-то фигуры)
    :return: длина вектора
    """
    return ti.sqrt(p.dot(p))


@ti.func
def normalize(p):
    """
    Норма вектора
    :param p: точка на луче rd (на поверхности какой-то фигуры)
    :return: длина вектора
    """
    n = p.norm()
    return p / (n if n != 0. else 1.)


@ti.func
def mix(x, y, a):
    """
    Смешение цветов в заданной пропорции
    :param x: первый вектра
    :param y: второй вектор
    :param a: пропорция
    :return: новый цвет
    """
    return x * (1. - a) + y * a


@ti.func
def dot(p, q):
    """
    Скалярное произведение двух векторов
    :param p: первый вектор
    :param q: второй вектор
    :return: число, равное скалярному произведению
    """
    return p.dot(q)


@ti.func
def dot2(p):
    """
    Квадрат модуля вектора
    :param p: сам вектор
    :return: число, равное квадрату модуля
    """
    return p.dot(p)


@ti.func
def cross(x, y):
    """
    Векторное произведение
    :param x: первый вектор
    :param y: второй вектор
    :return: вектор, равный вектороному произведению
    """
    return vec3(x[1] * y[2] - y[1] * x[2],
                x[2] * y[0] - y[2] * x[0],
                x[0] * y[1] - y[0] * x[1])


@ti.func
def reflect(rd, n):  # rd: vec3, n: vec3
    """
    Отражает вектор света при попадании на поверхность
    :param rd: вектор направления луча
    :param n: нормаль к поверхности
    :return: отражённый вектор
    """
    return rd - 2.0 * dot(n, rd) * n


@ti.func
def deg2rad(a):
    """
    Перевод градусов в радианы
    :param a: угол в градусах
    :return: угол в радианах
    """
    return a * pi180


@ti.func
def rot(a):
    """
    Матрица поворота в плоскости
    :param a: радианы
    :return: матрица поворота
    """
    c = ti.cos(a)
    s = ti.sin(a)
    return mat2([[c, -s], [s, c]])


@ti.func
def rot_y(a):
    """
    Матрица поворота по оси Oy
    :param a: радианы
    :return: матрица поворота
    """
    c = ti.cos(a)
    s = ti.sin(a)
    return mat3([[c, 0, -s],
                 [0, 1,  0],
                 [s, 0,  c]])


@ti.func
def rot_x(a):
    """
    Матрица поворота по оис Ox
    :param a: радианы
    :return: матрица поворота
    """
    c = ti.cos(a)
    s = ti.sin(a)
    return mat3([[1, 0,  0],
                 [0, c, -s],
                 [0, s,  c]])


@ti.func
def rot_z(a):
    """
    Матрица поворота по оис Oz
    :param a: радианы
    :return: матрица поворота
    """
    c = ti.cos(a)
    s = ti.sin(a)
    return mat3([[c, -s, 0],
                 [s,  c, 0],
                 [0,  0, 1]])

@ti.func
def sign(x: ti.f32):
    """
    sign-функция
    :param x: аргумент
    :return: значение sign-функции при аргументе x
    """
    return 1. if x > 0. else -1. if x < 0. else 0.


@ti.func
def signv(x: tmpl):
    """
    sign-функция для каждого элемента в векторе
    :param x: входной вектор
    :return: вектор, к которому была применена sign-функция
    """
    r = ti.Vector(x.shape[0], x.dtype)
    for i in ti.static(range(x.shape[0])):
        r[i] = sign(x[i])
    return r


@ti.func
def clamp(x, low, high):
    """
    Получение наиболее близкого значения в заданном диапазоне
    :param x: исходное значение
    :param low: нижняя граница
    :param high: верзняя граница
    :return: новое значение в границах low и high
    """
    return ti.max(ti.min(x, high), low)


@ti.func
def fract(x):
    """
    Дробная часть числа
    :param x: значение
    :return: дробная часть
    """
    return x - ti.floor(x)


@ti.func
def smoothstep(edge0, edge1, x):
    """
    Сглаживание значениея в диапазоне
    :param edge0: нижняя граница
    :param edge1: верхняя граница
    :param x: само значение
    :return: сглаженное значение
    """
    n = (x - edge0) / (edge1 - edge0)
    t = clamp(n, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


@ti.func
def skewsin(x, t):
    """
    skewsin-функция
    :param x: радианы
    :param t: значение
    :return: значение skewsin-функции
    """
    return ti.atan2(t * ti.sin(x), (1. - t * ti.cos(x))) / t

#PRNG

@ti.func
def random2():
    """
    Возвращает случайное значение
    :return: случайное значение
    """
    return vec2(ti.random(ti.f32), ti.random(ti.f32))


@ti.func
def hash21(p):
    """
    Хеширование значение, используя функцию fract()
    :param p: значение
    :return: хешированное значение
    """
    q = fract(p * vec2(123.34, 345.56))
    q += dot(q, q + 34.23)
    return fract(q.x * q.y)


@ti.func
def sd_box(p, b):
    """
    Формула кубика
    :param p: точка на луче rd (на поверхности кубика)
    :param b: размер кубика
    :return: расстояние от точки на rd до границы кубика
    """
    d = abs(p) - b
    return max(d, 0.).norm() + min(d.max(), 0.0)


@ti.func
def sd_sphere(p, r):
    """
    Формула сферы
    :param p: точка на луче rd (на поверхности сферы)
    :param r: радиус сферы
    :return: расстояние от точки на rd до границы сферы
    """
    return length(p) - r


@ti.func
def sd_torus(p, r):
    """
    Формула торуса
    :param p: точка на луче rd (на поверхности торуса)
    :param r: радиус торуса
    :return: расстояние от точки на rd до границы торуса
    """
    q = vec2(length(vec2(p.x, p.z)) - r.x, p.y)
    return length(q) - r.y


@ti.func
def lookat(pos, look, up, s):
    """
    Куда и как смотрит камера
    :param pos: 1 и 3 координата (отвечают за позицию в плоскости пола) вместе с s влияют на удаление камеры от точки вращения
    :param look: 2 координата вместе с 2 координатой из ro влияет одновременно на наклон и положение камеры по оси Oz (в 3D сцене)
    :param up: направление вверх (в 3D сцене)
    :param s: зум
    :return:
    """
    f = normalize(look - pos)
    r = normalize(cross(up, f))
    u = cross(f, r)
    return f * s, r, u


@ti.func
def argmin(v):
    """
    Значение и индекс минимального элемента в v
    :param v: вектор
    :return: значение и индекс минимального элемента в v
    """
    m = v[0]
    j = 0
    for i in ti.static(range(1, len(v))):
        if v[i] < m:
            j = i
            m = v[i]
    return m, j


# New figures here

@ti.func
def sd_plane(p, n, h):
    """
    Формула плоскости
    :param p: точка на луче rd
    :param n: нормаль
    :param h: высота
    :return: расстояние от точки на rd до границы плоскости
    """
    return dot(p, n) + h


@ti.func
def sd_verticalCapsule(p, h, r):
    """
    Формула вертикальной капсулы
    :param p: точка на луче rd
    :param h: нормаль
    :param r: радиус
    :return: расстояние от точки на rd до границы вертикальной капсулы
    """
    p.y -= clamp(p.y, 0.0, h)[0]
    return length(p) - r


@ti.func
def sd_roundedCylinder(p, ra, rb, h):
    """
    Формула цилиндра со скруглёнными краями
    :param p: точка на луче rd
    :param ra: радиус цилиндра
    :param rb: радиус скругления
    :param h: высота
    :return: расстояние от точки на rd до границы цлиндра со скруглёнными краями
    """
    d = vec2(length(vec2(p.x, p.z)) - 2.0 * ra + rb, abs(p.y) - h)
    return min(max(d.x, d.y), 0.0) + length(max(d, 0.0)) - rb


@ti.func
def sd_Octahedron(p, s):
    """
    Формула октаэдра
    :param p: точка на луче rd
    :param s: размер
    :return: расстояние от точки на rd до границы октаэда
    """
    p = abs(p)
    return (p.x + p.y + p.z - s) * 0.57735027


@ti.func
def sd_Link(p, le, r1, r2):
    """
    Формула бублика
    :param p: точка на луче rd
    :param le: длина
    :param r1: радиус скругления
    :param r2: радиус
    :return: расстояние от точки на rd до границы бублика
    """
    q = vec3(p.x, max(abs(p.y) - le, 0.0), p.z)
    return length(vec2(length(vec2(q.x, q.y)) - r1, q.z)) - r2
