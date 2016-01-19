import os
import glob
import sys


def getFolders(root_dir):
    subfolders = []
    for root, subfolder, file_ in os.walk(root_dir):
        for s in subfolder:
            subfolders.append(os.path.join(root, s))
    return subfolders


def scan(frame_range, frame_padding, file_type):
    ## FIND SEQUENCES
    root_dir = os.getcwd()
    print root_dir
    # calculate the expected length of the sequence (# of files)
    num_frames = frame_range[1] - frame_range[0]
    num_frames += 1
    # Format frame padding value into glob-friendly string
    padding = ''.rjust(frame_padding, '?')

    try:
        # Iterate over all subfolders, looking for image sequences that match the params
        for folder in getFolders(root_dir):
            os.chdir(folder)
            # list all files in the cwd matching the expected pattern for image sequences
            img_seq = glob.glob('*.{0}.{1}'.format(padding, file_type))
            # parse that list for sequence names.  since there may be more than one 
            # in the folder we create a set() of the results to boil down the list
            sequences = [s.split('.')[0] for s in img_seq]
            sequences = set(sequences)

            if len(sequences) == 0:
                continue

            ## CHECK SEQUENCES
            # container list for missing files    
            missing = []
            # iterate over each sequence
            for s in sequences:    
                # s is just the name of the prefix, so we need to glob for
                # all the frames that match.
                seq = glob.glob('{0}.{1}.{2}'.format(s, padding, file_type))
                # check the size of that array vs the expected input size
                # if the sizes match, there aren't any missing files
                if len(seq) == num_frames:
                    continue
                else: pass
                # there is a difference in sizes, so there must be 
                # missing files. iterate over the array to identify them
                for i in range(num_frames):
                    # offset counter to match frame numbering
                    i = i + frame_range[0]
                    # generate a name for the expected files
                    frame_num = str(i).zfill(frame_padding)
                    frame = '{0}.{1}.{2}'.format(s, frame_num, file_type)
                    # check if that file exists
                    path = os.path.join(folder, frame)
                    #print path
                    if not os.path.exists(path):
                        # if not, add it to the list
                        print path + ' missing!'
                        missing.append(path)

    except: pass#print 'SEQCHK UNHANDLED ERROR'

    finally:
        os.chdir(root_dir)

    if len(missing) == 0: return None
    else: return missing
