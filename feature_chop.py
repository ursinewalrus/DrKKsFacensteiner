import json
from PIL import Image
import sys
import pprint as pp
import random
import sys

def get_face_image_parts_boxes(face_parameters,image):
	chopped_face = {};
	# for nose, combine nose_tip max Y and its X cords with min Y for bridge
	# below notes might not be true for if you dont grab the whole box, face lib seems to possibly trace
	# bottom_lip seems to get whole mouth
	# chin gets basically the whole face
	full_nose_cords = [0,0,0,0]
	for feature in face_parameters:
		feature_params = face_parameters[feature]

		feature_params.sort(key=lambda x: x[0])
		minX = feature_params[0][0]
		maxX = feature_params[len(feature_params)-1][0]

		feature_params.sort(key=lambda x: x[1])
		minY = feature_params[0][1]
		maxY = feature_params[len(feature_params)-1][1]
		face_feature_image = image.crop((minX,minY,maxX,maxY))
		chopped_face[feature] = {"image": face_feature_image, "cords": (minX,minY,maxX,maxY)}

		if feature == 'nose_bridge':
			full_nose_cords[1] = minY
		if feature == 'nose_tip':
			full_nose_cords[0] = minX
			full_nose_cords[2] = maxX
			full_nose_cords[3] = maxY

	chopped_face['nose'] = {"image": image.crop(tuple(full_nose_cords)), "cords":tuple(full_nose_cords)}
	chopped_face = pad_face_image_parts(chopped_face,image)
	return chopped_face

# padd each feature with skin around it
# parts of face might need generate / intuit
	# forehead
	# cheeks
	# chin? -> maybe get bottom middle of current chin
	# for eyes/brows->maybe snag a little extra on the sides
	# eyes -> maybe snag out to chin??
	# brows also maybe extra above
	# for mouth -> little extra above and below
	# for nose -> little extra sides
def pad_face_image_parts(face_parts,image):
	for (l,r) in [("left_eye","right_eye"),("left_eyebrow","right_eyebrow")]:
		x_eye_distance = (face_parts[r]["cords"][0] - face_parts[l]["cords"][2])/2
		
		old_left_eye_cords = face_parts[l]["cords"]
		new_left_eye_cords = (old_left_eye_cords[0],old_left_eye_cords[1],old_left_eye_cords[2] + x_eye_distance,old_left_eye_cords[3])
		face_parts[l]["padded"] = image.crop(new_left_eye_cords) 

		old_right_eye_cords = face_parts[r]["cords"]
		new_right_eye_cords = (old_right_eye_cords[0] - x_eye_distance,old_right_eye_cords[1],old_right_eye_cords[2],old_right_eye_cords[3])
		face_parts[r]["padded"] = image.crop(new_right_eye_cords) 

	# face_parts["right_eye"]["image"].show()
	# face_parts["right_eye"]["padded"].show()


	return face_parts


def get_feature_from_random_face(faces,feature):
	face = faces[random.randint(0,len(faces)-1)]
	if "padded" in face[feature]:
		return face[feature]["padded"]
	return face[feature]['image']


# get all faces
# face_parts = get_face_image_parts_boxes(face_data[3],face_image)
# selection = ''

# pp.pprint(face_parts)


# while selection != 'done':
# 	selection = raw_input()
# 	face_parts[selection].show()
# 	pp.pprint(face_parts)



