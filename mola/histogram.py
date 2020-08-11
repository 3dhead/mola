import matplotlib.pyplot as plt
from PIL import Image
from colour import Color

from skimage import data, io
from skimage import exposure
from skimage.exposure import match_histograms

image = io.imread('/home/maroslaw/Downloads/ben-den-engelsen-lQFEdIBghv0-unsplash.jpg')

img = Image.open('/home/maroslaw/Downloads/ben-den-engelsen-lQFEdIBghv0-unsplash.jpg').convert("L")

histogram = img.histogram()
index = histogram.index(max(histogram))

# Color("black").range_to(Color(46, 52, 64), index)

palette = [Color('#2e3440'), Color('#5e81ac'), Color('#88c0d0'), Color('#8fbcbb'), Color('#d8dee9')]  # TODO order
p_i = 0

i_cols = [Color("black")]
i_last = 0

for i in range(len(histogram)):
    gray_scale = int(round(255 * (
            0.299 * palette[p_i].get_red() + 0.587 * palette[p_i].get_green() + 0.114 * palette[p_i].get_blue())))
    if gray_scale == i:
        tmp = []
        tmp.extend(i_cols[i_last].range_to(palette[p_i], i - i_last))
        i_cols.extend(tmp[1:])
        i_last = len(i_cols) - 1

tmp = []
tmp.extend(palette[p_i].range_to(Color("white"), len(histogram) - i_last))
i_cols.extend(tmp[1:])

print(len(i_cols))
width = 200
height = int(sum(histogram) / width)
reference = Image.new("RGB", (width, height), (255, 255, 255))
offsetx = 0
offsety = 0
for i in range(len(i_cols)):
    lwidth = max(1, histogram[i])
    print(str(i))

    while lwidth > 0:
        print("   " + str(lwidth))
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
