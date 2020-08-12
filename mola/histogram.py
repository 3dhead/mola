import matplotlib.pyplot as plt
from PIL import Image
from colour import Color

from skimage import data, io
from skimage import exposure
from skimage.exposure import match_histograms

image = io.imread('/home/maroslaw/Downloads/gontran-isnard-q6NvmanzdrU-unsplash.jpg')

img = Image.open('/home/maroslaw/Downloads/gontran-isnard-q6NvmanzdrU-unsplash.jpg').convert("L")

histogram = img.histogram()
index = histogram.index(max(histogram))


# Color("black").range_to(Color(46, 52, 64), index)

def darkness(color: Color) -> int:
    return int(round(255 * (0.299 * color.get_red() + 0.587 * color.get_green() + 0.114 * color.get_blue())))


palette = [Color('#2e3440'),
           Color('#3b4252'),
           Color('#434c5e'),
           Color('#4c566a'),
           Color('#d8dee9'),
           Color('#e5e9f0'),
           Color('#eceff4'),
           Color('#8fbcbb'),
           Color('#88c0d0'),
           Color('#81a1c1'),
           Color('#5e81ac'),
           Color('#bf616a'),
           Color('#d08770'),
           Color('#ebcb8b'),
           Color('#a3be8c'),
           Color('#b48ead')]
palette.sort(key=lambda c: darkness(c))
white = palette.pop()
p_i = 0

i_cols = [palette.pop(0)]
i_last = 0

for i in range(len(histogram)):
    if darkness(palette[p_i]) == i:
        tmp = []
        tmp.extend(i_cols[i_last].range_to(palette[p_i], i - i_last))
        i_cols.extend(tmp[1:])
        i_last = len(i_cols) - 1

tmp = []
tmp.extend(palette[p_i].range_to(white, len(histogram) - i_last))
i_cols.extend(tmp[1:])
for i in range(len(i_cols)):
    print(str(i_cols[i]) + " " + str(darkness(i_cols[i])))

print(len(i_cols))
width = img.size[0]
height = int(sum(histogram) / width)
reference = Image.new("RGB", (width, height), (255, 255, 255))
offsetx = 0
offsety = 0
for i in range(len(i_cols)):
    lwidth = max(1, histogram[i])

    while lwidth > 0:
        cwidth = lwidth
        wrap = False
        if cwidth > width - offsetx:
            wrap = True
            cwidth = width - offsetx
        if cwidth == 0:
            break
        reference.paste(
            Image.new("RGB", (cwidth, 1), (
                int(round(i_cols[i].get_red() * 255)), int(round(i_cols[i].get_green() * 255)),
                int(round(i_cols[i].get_blue() * 255)))),
            (offsetx, offsety))
        if wrap:
            offsetx = 0
            offsety += 1
        else:
            offsetx = offsetx + cwidth
        lwidth -= cwidth

reference.save('/home/maroslaw/tmp/ref.jpg', format="JPEG")

reference = io.imread('/home/maroslaw/tmp/ref.jpg')

matched = match_histograms(image, reference, multichannel=True)

fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, sharex=True, sharey=True, figsize=(8, 3))
for aa in (ax1, ax2, ax3):
    aa.set_axis_off()

ax1.imshow(image)
ax1.set_title('Source')
ax2.imshow(reference)
ax2.set_title('Reference')
ax3.imshow(matched)
ax3.set_title('Matched')

plt.tight_layout()
plt.show()

io.imsave('/home/maroslaw/tmp/out.jpg', matched)
