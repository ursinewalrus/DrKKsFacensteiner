from PIL import Image
import json
import stitch
import feature_chop
import pprint as pp

face_data = json.load(open('output.json'))
face_image = Image.open('5people.jpg')

faces = []
for feature_set in face_data:
	faces.append(feature_chop.get_face_image_parts_boxes(feature_set,face_image))

left_eyebrow = feature_chop.get_feature_from_random_face(faces,"left_eyebrow")
right_eyebrow = feature_chop.get_feature_from_random_face(faces,"right_eyebrow")

left_eye = feature_chop.get_feature_from_random_face(faces,"left_eye")
right_eye = feature_chop.get_feature_from_random_face(faces,"right_eye")

nose = feature_chop.get_feature_from_random_face(faces,"nose")
brow = stitch.combine_ims(left_eyebrow,right_eyebrow,"hort")
eyes = stitch.combine_ims(left_eye,right_eye,"hort")

eye_area = stitch.combine_ims(brow,eyes,"vert")
eye_and_nose = stitch.combine_ims(eye_area,nose,"vert")

mouth = feature_chop.get_feature_from_random_face(faces,"bottom_lip")

basic_face = stitch.combine_ims(eye_and_nose,mouth,"vert")

basic_face.save("franken.jpg")
# stitch.combine_ims()
# pp.pprint(faces)
# lets say a face is 
#	left_eyebrow | vert | right_eybrow  
# 				 | hort |
#   left_eye     | vert | right eye
# 			nose
# 			|maybe hort, or new func for dif scaling| 
#           bottom_lip
