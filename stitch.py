from PIL import Image

def scale_to_smallerW(f1,f2):
	f1W,f1H = f1.size
	f2W,f2H = f2.size

	newW = min(f1W,f2W)
	wpercent = newW / float(max(f1W, f2W))
	newH = int(max(f1H,f2H) * wpercent)	
	f1 = f1.resize((newW,f1H if f1H<newH else newH))
	f2 = f2.resize((newW,f2H if f2H<newH else newH))

	return f1, f2

def scale_to_smallerH(f1,f2):
	f1W,f1H = f1.size
	f2W,f2H = f2.size

	newH = min(f1H,f2H)
	Hpercent = newH / float(max(f1H, f2H))
	newW = int(max(f1W,f2W) * Hpercent)	
	f1 = f1.resize((f1W if f1W<newW else newW,newH))
	f2 = f2.resize((f2W if f2W<newW else newW,newH))

	return f1, f2

# scale_priority = 'vert' or 'hort'
# hort for things in a row
# vert for things stacked
def combine_ims(im1,im2,scale_priority):

	if scale_priority == 'hort':
		f1,f2 = scale_to_smallerH(im1,im2)
		f1W, f1H = f1.size
		f2W, f2H = f2.size
		newW = f1W + f2W;
		newH  = max(f1H,f2H)
		new_im = Image.new('RGB', (newW,newH))
		new_im.paste(f1,(0,0));		
		new_im.paste(f2,(f1W,0))
	else:
		f1,f2 = scale_to_smallerW(im1,im2)
		f1W, f1H = f1.size
		f2W, f2H = f2.size
		newH = f1H + f2H;
		newW  = max(f1W,f2W)
		new_im = Image.new('RGB', (newW,newH))
		new_im.paste(f1,(0,0));		
		new_im.paste(f2,(0,f1H))

	return new_im

# def rotate_im(im,degrees):


# im1 = Image.open("me.jpg")
# im2 = Image.open("cat.jpg")
# # im1.show()
# # f1.show()
# new_im = combine_ims(im1,im2,'hort')

# new_im.transpose(45).show()