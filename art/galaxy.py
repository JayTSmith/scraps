import os.path
import random
from math import cos, pi

from PIL import Image, ImageDraw, ImageFilter, ImageFont


class Fader(object):
    @staticmethod
    def percent_float(percent):
        return percent / 100

    @staticmethod
    def fade_linear(alpha: int, step: int):
        return round(alpha * Fader.percent_float(step))

    @staticmethod
    def fade_cubic_root(alpha: int, step: int, a=None, b=None, c=None, d=None):
        a = a or 1
        b = b or 1
        c = c or 0
        d = d or 0

        # This is done in order to reduce the chance of complex roots
        # This is fully dependent on the function not doing that tho.
        bc = (b * (step - c))

        if bc:
            inside = (abs(bc) ** (1 / 3)) * abs(bc) / bc
        else:
            inside = 0
        raw = inside * a + d
        return round(alpha * Fader.percent_float(raw))

    @staticmethod
    def fade_square_root(alpha: int, step: int, a=None, b=None, c=None, d=None):
        a = a or 1
        b = b or 1
        c = c or 0
        d = d or 0

        bc = (b * (step - c))
        if bc < 0:
            return 0

        raw = a * (bc ** (1 / 2)) + d
        return round(alpha * Fader.percent_float(raw))

    @staticmethod
    def fade_parabola(alpha: int, step: int):
        return round(alpha * Fader.percent_float(step) ** 2)

    @staticmethod
    def fade_random(alpha: int, step: int):
        return round(alpha * random.random())

    @staticmethod
    def fade_abs_sin(alpha: int, step: int):
        return round(alpha * cos(Fader.percent_float(step) * pi))


def draw_faded_circle(img: Image, xy: tuple, radius, fill: tuple, fader: callable = None):
    if fader is None:
        fader = Fader.fade_linear

    new_layer = Image.new('RGBA', img.size)
    cir_drawer = ImageDraw.Draw(new_layer)

    print('Drawing a circle at {0}, {1} with a radius of {2} using fader {3}'.format(*xy, radius, fader.__name__))

    for i in range(100, 0, -1):
        work_alpha = fader(fill[3], 100 - i)
        work_radius = fader(radius, i)
        if not work_radius:
            break
        pos = (xy[0] - work_radius, xy[1] - work_radius, xy[0] + work_radius, xy[1] + work_radius)
        # print('{0}-th step| Alpha: {1} Size: {2}'.format(i, work_alpha, pos[2] - pos[0]))
        _fill = (fill[0], fill[1], fill[2], work_alpha)
        cir_drawer.ellipse(pos, fill=_fill)

    return Image.alpha_composite(img, new_layer)
    # drawer.ellipse(xy, fill=fill)


# Circles are the amount of circles to draw in the blob area.
def draw_blob(img, xy: tuple, circles: int, radius, fill: tuple, fader: callable = None, variance: int = None):
    if variance is None:
        variance = 0
    cur_img = img
    for i in range(circles):  # May be an arg.
        work_xy = (
            xy[0] + random.randint(-variance, variance),
            xy[1] + random.randint(-variance, variance)
        )
        cur_img = draw_faded_circle(cur_img, work_xy, radius + random.randint(-variance, variance), fill, fader=fader)

    return cur_img


def draw_stars(img, fill: tuple, fader: callable = None, frequency: int = None,
               max_radius: int = None, min_radius: int = None, variance: int = None):
    cur_img = img
    fader = fader or Fader.fade_linear
    min_radius = min_radius or min(img.height, img.width) * .05
    max_radius = max_radius or min_radius * 2
    frequency = frequency or 50
    variance = variance or min_radius

    cur_pos = (min_radius, min_radius)
    while cur_pos[0] <= img.width:
        while cur_pos[1] <= img.height:
            used_radius = random.randint(min_radius, max_radius)  # Set the size of the circle beforehand.
            if random.randint(1, 100) <= frequency:
                work_pos = (
                    cur_pos[0] + random.randint(-variance, variance),
                    cur_pos[1] + random.randint(-variance, variance)
                )  # Adds some varied positions so it doesn't look grid based.
                cur_img = draw_faded_circle(cur_img, work_pos, used_radius, fill, fader=fader)
            cur_pos = (cur_pos[0], cur_pos[1] + used_radius + max_radius)  # Go to the next row
        cur_pos = (cur_pos[0] + max_radius, min_radius)  # Go to the next column

    return cur_img


def test_build():
    colors = {
        'text': (128, 128, 128, 255),
        'star-white': (150, 150, 150, 255),
        'purple': (20, 0, 90, 255),
        'pink': (120, 0, 90, 255)
    }

    if not os.path.isdir('./test'):
        os.mkdir('./test')

    faders = [getattr(Fader, fader) for fader in dir(Fader) if fader.startswith('fade_')]
    filters = [x for x in dir(ImageFilter) if x.isupper()]
    img_width = len(faders) * 150

    raw_img = Image.new('RGBA', (img_width, 100), color=(0, 0, 0, 255))

    # Drawing Guidelines at every 50 pixels
    raw_draw = ImageDraw.Draw(raw_img)
    for i in range(49, img_width, 50):
        start = (i, 0)
        end = (i, raw_img.height)
        raw_draw.line((start, end), fill=colors['pink'])

    # Drawing a 100px white circle with every fader available.
    for idx, fader in enumerate(faders):
        work_x = 49 + (100 * idx)
        raw_img = draw_faded_circle(raw_img, (work_x, 49), 50, colors['star-white'], fader=fader)

    # Apply every filter on the final image.
    for filt in filters:
        filt_path = os.path.join('test', filt + '.png')
        if os.path.exists(filt_path):
            os.remove(filt_path)
        raw_img.filter(getattr(ImageFilter, filt)).save(filt_path)

    raw_path = os.path.join('test', 'NO_FILTER.png')
    if os.path.exists(raw_path):
        os.remove(raw_path)
    raw_img.save(raw_path)

    if filters:
        stitch_height = (len(filters) + 1) * 100
        stitch_img = Image.new('RGBA', (img_width, stitch_height))
        filters.insert(0, 'NO_FILTER')

        stitch_img.paste(raw_img, (0, 0))

        for idx, filt in enumerate(filters):
            filt_img = Image.open(os.path.join('test', filt + '.png'), mode='r')
            filt_pos = (0, (99 * idx + idx))

            text_img = Image.new('RGBA', filt_img.size)
            # The most used color found in the filtered images
            max_color = sorted(filt_img.getcolors(maxcolors=65536), key=lambda e: e[0], reverse=True)[0][1]
            # Get the negative of the most used color so that the text will always show.
            text_color = (255 - max_color[0], 255 - max_color[1], 255 - max_color[2], 255)
            ImageDraw.Draw(text_img).text((5, 5), filt,
                                          font=ImageFont.truetype(font='LiberationMono-Regular.ttf', size=12),
                                          fill=text_color)

            out = Image.alpha_composite(filt_img, text_img)

            stitch_img.paste(out, filt_pos)
        stitch_img.save(os.path.join('test', 'stitch.png'))


def build_galaxy(path, img_size: int, overwrite=None):
    if os.path.exists(path) and not (overwrite or os.path.isfile(path)):
        return

    colors = {
        'star-white': (150, 150, 150, 255),
        'purple': (20, 0, 90, 255),
        'pink': (120, 0, 90, 255)
    }

    raw_img = Image.new('RGBA', (img_size, img_size), color=(0, 0, 0, 255))
    center = img_size // 2 - 1

    cube_root = lambda a, s: Fader.cubic_root(a, s, a=6, b=1, c=54, d=24)
    sq_root = lambda a, s: Fader.square_root(a, s)

    # raw_img = draw_faded_circle(raw_img, (199, 199), 100, colors['purple'], fader=Fader.parabola)
    # raw_img = draw_faded_circle(raw_img, (399, 199), 100, colors['purple'], fader=Fader.random)
    # raw_img = draw_faded_circle(raw_img, (799, 199), 100, colors['purple'])
    # raw_img = draw_faded_circle(raw_img, (499, 499), 100, colors['purple'], fader=cube_root)

    raw_img = draw_stars(raw_img, colors['star-white'], fader=Fader.ease_out, frequency=100)
    raw_img = draw_blob(raw_img, (center, center), 300, 10, colors['purple'], fader=cube_root, variance=100)
    raw_img = draw_blob(raw_img, (center, center), 100, 100, colors['pink'], fader=sq_root, variance=center + 1)
    os.remove(path)
    raw_img.save(path)


if __name__ == '__main__':
    test_build()
