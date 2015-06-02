import os
import glob
import sys

def main(frame_range, frame_padding, file_type):
	## FIND SEQUENCES
	# get cwd
	cwd = os.getcwd()
	# calculate the expected length of the sequence (# of files)
	seq_len = frame_range[1] - frame_range[0]
	seq_len += 1
	# Format frame padding value into glob-friendly string
	padding = ''.rjust(frame_padding, '?')
	# list all files in the cwd matching the expected pattern for image sequences
	img_seq = glob.glob('*.{0}.{1}'.format(padding, file_type))
	# parse that list for sequence names.  since there may be more than one 
	# in the folder we create a set() of the results to boil down the list
	sequences = [s.split('.')[0] for s in img_seq]
	sequences = set(sequences)

	## CHECK SEQUENCES
	# container list for missing files	
	missing = []
	# iterate over each sequence
	for seq in sequences:	
		# check the size of that array vs the expected input size
		# if the sizes match, there aren't any missing files
		if len(img_seq) == seq_len:
			continue
		else: pass
		# there is a difference in sizes, so there must be 
		# missing files. iterate over the array to identify them
		for i in range(seq_len):
			# offset counter to match frame numbering
			i = i + frame_range[0]
			# generate a name for the expected files
			frame_num = str(i).zfill(4)
			frame = '{0}.{1}.{2}'.format(seq, frame_num, file_type)
			print frame
			# check if that file exists
			if not os.path.exists(os.path.join(cwd, frame)):
				# if not, add it to the list
				missing.append(os.path.join(cwd, frame))

	## RECURSION
	# now that we've done all the files, check for subdirectories
	subdirs = [d[0] for d in os.walk(cwd)]
	# recurse through those folders
	for dir_ in subdirs:
		os.chdir(dir_)
		recurse_result = main(frame_range, frame_padding, file_type)

	missing.append(recurse_result)

	return missing
	

