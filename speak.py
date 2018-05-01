from PIL import Image, ImageDraw
import cv2 as cv

edge_get = cv.imread("10blended.jpg")
edges = cv.Canny(edge_get,100,200)
im = Image.open("10blended.jpg")
dot = ImageDraw.Draw(im)

for w in range(len(edges)):
	for h in range(len(edges[0])):
		if edges[w][h] == 255:
			dot.point((h,w),"red")
del dot
im.save('face_with_edges.jpg')
im.show()
# dot.point(zip())


# PIL.ImageDraw.Draw.point(xy, fill=None)
# cv.imshow('image',img)
# cv.waitKey(0)
# cv.destroyAllWindows()