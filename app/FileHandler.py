


class FileHandler():

	test_folder = "test-data/"
	training_folder = "training/"
	validation_folder = "validation/"
	users_file = "users.txt"
	users_list = []

	def __init__(self):
		# Load the users list into memory for reading
		file = read(users_file)
		while (line = file.read()):
			users_list.add(line)

	# Should we keep a text file with all names? or search the folders on runtime?
	# Will implemenent with text file now, until i can decide what to do

	def write(self, name, image):
		if name not in users_list:
			# New user, make a new folder for them.
		else:
			# Existing user, add the images to that folder 
			pass
		




