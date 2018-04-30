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
	left_cheek_cords = [0,0,0,0]
	right_cheek_cords = [0,0,0,0]
	# (minx, miny, maxx, maxy)
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

		# making full nose
		if feature == 'nose_bridge':
			full_nose_cords[1] = minY
		if feature == 'nose_tip':
			full_nose_cords[0] = minX
			full_nose_cords[2] = maxX
			full_nose_cords[3] = maxY
		
		# making cheeks
		# they art catching some nose, push out from nose, need eye and nose
		if feature == 'left_eye':
			left_cheek_cords[0] = minX
			left_cheek_cords[1] = maxY
		if feature == 'right_eye':
			right_cheek_cords[1] = maxY
			right_cheek_cords[2] = maxX
		if feature == 'nose_tip':
			left_cheek_cords[2] = minX
			right_cheek_cords[0] = maxX
		if feature == 'top_lip':
			left_cheek_cords[3] = minY
			right_cheek_cords[3] = minY



	chopped_face['nose'] = {"image": image.crop(tuple(full_nose_cords)), "cords":tuple(full_nose_cords)}
	chopped_face['left_cheek'] = {"image": image.crop(tuple(left_cheek_cords)), "cords":tuple(left_cheek_cords)}
	chopped_face['right_cheek'] = {"image": image.crop(tuple(right_cheek_cords)), "cords":tuple(right_cheek_cords)}
	# chopped_face["left_cheek"]["image"].show()
	# chopped_face["right_cheek"]["image"].show()
	# sys.exit(0)
	chopped_face = pad_face_image_parts(chopped_face,image)

	return chopped_face

# padd each feature with skin around it
# parts of face might need generate / intuit
	# forehead
	# cheeks
	# chin? -> maybe get bottom middle of current chin
	# for eyes/brows->maybe snag a little extra on the sides
	# eyes -> maybe snag out to chin??, get extra below
	# for nose -> little extra sides->out to x's of eyes, cut a little on top
	# brows also maybe extra above
	# for mouth -> little extra above and below
def pad_face_image_parts(face_parts,image):
	# maybe abs() all the x cord additions
	# adds padding between eyes
	for (l,r) in [("left_eye","right_eye"),("left_eyebrow","right_eyebrow")]:
		x_eye_distance = (face_parts[r]["cords"][0] - face_parts[l]["cords"][2])/2
		
		old_left_eye_cords = face_parts[l]["cords"]
		new_left_eye_cords = (old_left_eye_cords[0],old_left_eye_cords[1],old_left_eye_cords[2] + x_eye_distance,old_left_eye_cords[3])
		face_parts[l]["padded"] = image.crop(new_left_eye_cords) 

		old_right_eye_cords = face_parts[r]["cords"]
		new_right_eye_cords = (old_right_eye_cords[0] - x_eye_distance,old_right_eye_cords[1],old_right_eye_cords[2],old_right_eye_cords[3])
		face_parts[r]["padded"] = image.crop(new_right_eye_cords) 
	# adds padding above mouth
	upper_lip_height = (face_parts['top_lip']['cords'][1] - face_parts['nose_tip']['cords'][3])
	old_mouth_cords = face_parts["bottom_lip"]["cords"]
	new_mouth_cords = (old_mouth_cords[0],old_mouth_cords[1] - upper_lip_height,old_mouth_cords[2],old_mouth_cords[3])
	# face_parts["bottom_lip"]["padded"] = image.crop(new_mouth_cords)
	# adds padding to sides of the mouth
	center_left_eye = face_parts["left_eye"]["cords"][2] - (face_parts["left_eye"]["cords"][2] - face_parts["left_eye"]["cords"][0])
	center_right_eye = face_parts["right_eye"]["cords"][2] + (face_parts["right_eye"]["cords"][2] - face_parts["right_eye"]["cords"][0])
	# old_mouth_cords = face_parts["bottom_lip"]["padded"]
	new_mouth_cords = (center_left_eye,old_mouth_cords[1] - upper_lip_height,center_right_eye,old_mouth_cords[3])
	face_parts["bottom_lip"]["padded"] = image.crop(new_mouth_cords)
	# adds cheeks around the nose
	# nose_left_extension = face_parts["nose"]["cords"][0] - face_parts["left_eye"]["cords"][0]
	# nose_right_extension = face_parts["nose"]["cords"][3] - face_parts["right_eye"]["cords"][3] 
	# old_nose_cords = face_parts["nose"]["cords"]
	# nose_off_top = old_nose_cords[1] - max(face_parts["left_eye"]["cords"][3],face_parts["right_eye"]["cords"][3])
	# new_nose_cords  = (old_nose_cords[0] - nose_left_extension, old_nose_cords[1] - nose_off_top, old_nose_cords[2] + nose_right_extension, old_nose_cords[3])
	#face_parts["nose"]["padded"] = image.crop(new_nose_cords)
	return face_parts


def get_feature_from_random_face(faces,feature):
	face = faces[random.randint(0,len(faces)-1)]
	if "padded" in face[feature]:
		return face[feature]["padded"]
	return face[feature]['image']


# get all faces
# face_parts = get_face_image_parts_boxes(face_data[3],face_image)




