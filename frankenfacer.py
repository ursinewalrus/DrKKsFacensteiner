from PIL import Image
import json
import stitch
import feature_chop
import pprint as pp
import smoothing



def frankenify(face_file):
	face_image = Image.open(face_file)
	face_data = json.load(open('output.json'))
	faces = []
	for feature_set in face_data:
		faces.append(feature_chop.get_face_image_parts_boxes(feature_set,face_image))

	left_eyebrow = feature_chop.get_feature_from_random_face(faces,"left_eyebrow")
	right_eyebrow = feature_chop.get_feature_from_random_face(faces,"right_eyebrow")

	left_eye = feature_chop.get_feature_from_random_face(faces,"left_eye")
	right_eye = feature_chop.get_feature_from_random_face(faces,"right_eye")

	nose = feature_chop.get_feature_from_random_face(faces,"nose")
	nose_colors = smoothing.get_mean_pixel_color(nose)

	left_cheek = feature_chop.get_feature_from_random_face(faces,"left_cheek")
	right_cheek = feature_chop.get_feature_from_random_face(faces,"right_cheek")

	mouth = feature_chop.get_feature_from_random_face(faces,"bottom_lip")


	brow = stitch.combine_ims(left_eyebrow,right_eyebrow,"hort")
	eyes = stitch.combine_ims(left_eye,right_eye,"hort",1.5)
	cheeks_and_nose = stitch.combine_ims(stitch.combine_ims(left_cheek,nose,"hort"),right_cheek,"hort")

	eye_area = stitch.combine_ims(brow,eyes,"vert")
	eye_and_nose = stitch.combine_ims(eye_area,cheeks_and_nose,"vert")


	basic_face = stitch.combine_ims(eye_and_nose,mouth,"vert")

	# basic_face = smoothing.set_pixels_to_average_color(basic_face,nose_colors,False)

	return basic_face
	# basic_face.save("franken.jpg")
	# basic_face.show()

def feature_replace(face_file):
	face_image = Image.open(face_file)
	# oh wait i dont actually have full face cords, will hold off on this
	# 4 point chin actually gets everything so could work...

f1 = frankenify('5people.jpg')
for i in range(10):
	f2 = frankenify('5people.jpg')
	f1_size = f1.size
	f2_size = f2.size
	im_size = min(f1_size[0],f2_size[0]),min(f1_size[1],f2_size[1])
	f1 = f1.resize(im_size)
	f2 = f2.resize(im_size)
	f1 = Image.blend(f1,f2,0.5)
f1.show()
f1.save("10blended.jpg")

# while selection != 'done':
# 	selection = raw_input()
# 	if selection == 'frankenify':
# 		file = raw_input('File Name')
# 		frankenify(file)
# 	elif selection == "mask":
# 		file = raw_input('File Name')
# 		feature_replace(file)
# 	pp.pprint(face_parts)

# stitch.combine_ims()
# pp.pprint(faces)
# lets say a face is 
#	left_eyebrow | vert | right_eybrow  
# 				 | hort |
#   left_eye     | vert | right eye
# 			nose
# 			|maybe hort, or new func for dif scaling| 
#           bottom_lip
