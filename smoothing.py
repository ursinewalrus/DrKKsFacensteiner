from PIL import Image
allowed_color_deviation = 300


def get_mean_pixel_color(image):
    width,height = image.size
    size = width*height
    sum_r = 0
    sum_g = 0
    sum_b = 0
    for w in range(width):
    	for h in range(height):
            pix_vals = image.getpixel((w,h))
            sum_r += pix_vals[0]
            sum_g += pix_vals[2]
            sum_b += pix_vals[2]
    return (sum_r/size, sum_g/size, sum_b/size)  

def get_median_pixel_color(image):
    width,height = image.size
    size = width*height
    rs = []
    gs = []
    bs = []
# 
# if overwrite_average is false, will pull values a set distance from given average to the average
# if overwrite_average set to true, finds the current image average no matter what it is and overwrites it
# allowed_color_deviation shoudl be smaller if overwrite is set to true
def set_pixels_to_average_color(image,averages,overwrite_average=False):
    r,g,b = averages
    width,height = image.size
    # new_im = Image.new("RGB",(width,height))
    im_new = image.load()
    if overwrite_average:
        pix = get_mean_pixel_color(image)
    for w in range(width):
        for h in range(height):
            if not overwrite_average:
                pix = image.getpixel((w,h))
            if pix[0] in range(r-allowed_color_deviation,r+allowed_color_deviation) \
            and pix[1] in range(g-allowed_color_deviation,g+allowed_color_deviation) \
            and pix[2] in range(b-allowed_color_deviation,b+allowed_color_deviation):
                # im_new[w,h] = (r,g,b)#instead of flat set pull closer depending on how close already...
                new_r = r - ((r - pix[0]) / 2)
                new_g = g - ((g - pix[1]) / 2)
                new_b = b - ((b - pix[2]) / 2)
                im_new[w,h] = (new_r,new_g,new_b)

    return image

# def set_pixels_to_summed_average_color(image,average):
#     width,height = image.size
#     im_new = image.load()
#     for w in range(width):
#         for h in range(height):
#             pix = sum(image.getpixel((w,h)))
#             if pix in range(average-allowed_color_deviation,average+allowed_color_deviation):
#                 im_new[w,h] = ()

# def avg_color_with_map(image):
#     map_over_pixels(image,lambda x: )

# def map_over_pixels(image,func,*extra_args):
#     width,height = image.size
#     for w in range(width):
#         for h in range(height):
#             func_run = func()
#             func_run(image.getpixel((w,h)),extra_args)
#     return image

# def set_average_pixel_color(image,rgb_avgs):
#     return map_over_pixels(image,normalize_skin,rgb_avgs)

# def normalize_skin(pixel,avg_tones):


# im = Image.open('5people.jpg')
# # avgs = get_mean_pixel_color(im)
# avgs = get_mean_pixel_color(im)
# im = set_pixels_to_average_color(im,avgs)
# im.show()
'''
def get_average_color((x,y), n, image):
    """ Returns a 3-tuple containing the RGB value of the average color of the
    given square bounded area of length = n whose origin (top left corner) 
    is (x, y) in the given image"""
 
    r, g, b = 0, 0, 0
    count = 0
    for s in range(x, x+n+1):
        for t in range(y, y+n+1):
            pixlr, pixlg, pixlb = image[s, t]
            r += pixlr
            g += pixlg
            b += pixlb
            count += 1
    return ((r/count), (g/count), (b/count))
'''