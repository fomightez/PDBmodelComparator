#!/usr/bin/env python
# `test_missing_residue_detailer.py` by Wayne Decatur
# this goes in same folder with
# `my_conftest_for_test_missing_residue_detailer.py` & `conftest.py` that will 
# be for  testing `missing_residue_detailer.py`, which needs to be in root 
import pytest
import os
import fnmatch
import glob
import filecmp
from bs4 import BeautifulSoup

# Run this file while working diretory is at root,
# like `pytest -v additional_nbs/tests/test_missing_residue_detailer.py` 

# Compares the results of my `missing_residue_detailer.py` with collected 
# results from Eric Martz's FirstGlance in Jmol. I had to hand collect the 
# results from Eric Martz's FirstGlance in Jmol because I thought easier and 
# more portable to script detailing missing residues myself than use slenium or
# something along those lines to handle getting missing residue information from
# Eric Martz's FirstGlance in Jmol.


#*******************************************************************************
##################################
#  USER ADJUSTABLE VALUES        #

##################################
#
aMMMMMMMM_prefix = "fgij_html_" # Used here?????
 

#
#*******************************************************************************
#**********************END USER ADJUSTABLE VARIABLES****************************



#*******************************************************************************
##################################
#  FILE PATHS       #

##################################
#

current_provided_exampleMMMMMMM = "???????????????" # USED HERE??????
 
#
#*******************************************************************************
#*****************************END FILE PATHS************************************







###---------------------------HELPER FUNCTIONS-------------------------------###

def generate_filename_from_prefix_andPDBid(prefix,pdb_id):
    '''
    Takes a string that will be prefix and PDB id and generates file name with 
    correct extenstion.
    Specific examples
    =================
    Calling function with
        (firstglanceinjmol_hmtl_file_prefix,'6w6v')
    returns
        "fgij_html_6w6v.html"

    Calling function with
        (firstglanceinjmol_text_file_prefix,'6w6v')
    returns
        "fgij_text_6w6v.txt"

    '''
    extension = prefix.split("_",2)[1]
    if extension == "text":
        extension = "txt"
    return f"{prefix}{pdb_id}.{extension}"

def write_string_to_file(s, fn):
    '''
    Takes a string, `s`, and a name for a file & writes the string to the file.
    '''
    with open(fn, 'w') as output_file:
        output_file.write(s)



def make_corresponding_GUIobtained_filename(file_name):
    '''
    Takes a filename and makes it match pattern I used to name things in `results_observed_from_original_with_Example_data` based on names in `Example_data/Datasets`
    Specific example
    ================
    Calling function with
        ("ITS.fas")
    returns
        "from_ITS.fas_Structure.str"
    '''
    return "from_{}_Structure.str".format(file_name)

def make_corresponding_GUIobtained_logname(file_name):
    '''
    Takes a filename and makes it match pattern I used to name things in `results_observed_from_original_with_Example_data` based on names in `Example_data/Datasets`
    Specific example
    ================
    Calling function with
        ("ITS.fas")
    returns
        "from_ITS.fas_log.log"
    '''
    return "from_{}_log.log".format(file_name)

def read_and_process_file4content_check(file_path):
    '''
    read file for content check
    '''
    processed_data = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = [part for part in line.split() if part]
            if parts:
                processed_data.append(parts)
    return processed_data

def compare_files_content(file1_path, file2_path):
    '''
    Compare content ignoring whitespace differences
    '''
    data1 = read_and_process_file4content_check(file1_path)
    data2 = read_and_process_file4content_check(file2_path)

    assert len(data1) == len(data2), f"Files have different number of lines: {len(data1)} vs {len(data2)}"

    for i, (line1, line2) in enumerate(zip(data1, data2), 1):
        assert line1 == line2, f"Difference found at line {i}:\nFile 1: {' '.join(line1)}\nFile 2: {' '.join(line2)}"

    return True  # If we get here, the files are identical in content

def compare_file_content_equality(file1_path, file2_path, msg="Files are not identical in content, ignoring whitespace differences."):
    '''
    Compare two files content ignoring whitespace differences

    Has a default assertion message, but you can pass your own string as third
    argument in call or only pass the two paths and use the default.
    '''
    assert compare_files_content(file1_path, file2_path), msg

def parse_number_FASTA_selected(file_path):
    '''
    parse out number of files selected
    '''
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        log_content=file.read()
        return log_content.split("FASTA files selected.",1)[0].split()[-1].strip()

def extract_tag(file_path, process_number):
    '''
    from the content that will be in a log file of runs of the fasta2structure 
    example data get the 'tag' from the file base name I can use to match the 
    corresponding input data. The process number is the step number for logs
    made with more than one input file as part of the input.
    For example, for `Example_data/Datasets/ITS.fas`,
    the tag is `ITS.fas`.

    Except thete is an issue with the `log.log` that Adam Bessa provides
    in `Example_data/Results/`.
    These are the corresponding tags/names of FASTA file there and so I'll add 
    special handling for those since they don't conform to all the others.
    Avicennia-ITS_Phase.fas', 'Avicennia-trnD-trnT_ediphase.fas', 'Avicennia-trnH-trnK_editphase.fas
    '''
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        log_content=file.read()
        if 'Avicennia-' in log_content:
            return log_content.split(".fas",process_number)[process_number-1].split("Avicennia-")[1].split("_",1)[0]+".fas"
        else:
            return log_content.split(".fas",process_number)[process_number-1].split("/")[-1]+".fas"

def parse_variable_sites_info(file_path,process_number):
    '''
    parse out the variable sites string corresponding to the step number 
    (process_number) of such data in the log text content for where there is 
    more than one input file when the script is called.
    '''
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        log_content=file.read()
        return "["+log_content.split("[",process_number)[process_number].split("]")[0]+"]"

def compare_log_info(file1_path, file2_path):
    '''
    Compare number of number of FASTA files selected and variable sites info in 
    two specified log files
    '''
    # parse out number of files selected
    sel1 = parse_number_FASTA_selected(file1_path)
    sel2 = parse_number_FASTA_selected(file2_path)

    assert sel1 == sel2, f"Files have different number of FASTA files selected: {sel1} vs {sel2}"

    # There will be a number of variable sites information to compare equal to the number of files selected
    # make a dictionary to relate the names/tag for each one so matching the same
    # parse out variable sites information. One for file1 and one for file2.
    # Note that the dictonary is made with the 'tag' from the name of the input
    # file as key so the actual order of occurence/listing in the log file 
    # content won't matter for the comparison.
    tag_and_variable_sites_f1 = {}
    tag_and_variable_sites_f2 = {}
    for i in range(int(sel1)):
        tag1 = extract_tag(file1_path,i+1)
        tag_and_variable_sites_f1[tag1] = parse_variable_sites_info(file1_path, i+1)
        tag2 = extract_tag(file2_path,i+1)
        tag_and_variable_sites_f2[tag2] = parse_variable_sites_info(file2_path, i+1)

    # sanity check: the number of keys should match sel1 and keys in the 
    # dictionary should be same.
    assert len(tag_and_variable_sites_f1) == int(sel1), f"The length of the dictionary keys old example logs, {len(tag_and_variable_sites_f1)}, for the file name tags should be the same as the number of FASTA files input into the log, {sel1}."
    assert len(tag_and_variable_sites_f2) == int(sel1), f"The length of the dictionary keys for current example logs, {len(tag_and_variable_sites_f2)}, for the file name tags should be the same as the number of FASTA files input into the log, {sel1}."
    assert len(tag_and_variable_sites_f1) == len(tag_and_variable_sites_f2), f"The number of the dictionary keys for current example logs, {len(tag_and_variable_sites_f2)}, for the file name tags should be the same as the value for length of the dictionary keys for current example logs, {len(tag_and_variable_sites_f2)}."
    assert tag_and_variable_sites_f1.keys() == tag_and_variable_sites_f2.keys(), f"The keys in the two dictionaries should match."


    # Now iterate on the dictionary and compare the variable sites for each tag.
    # Because the tags were used for the dictionary the actual order of the 
    # content appearing in the logs is moot. It is just checking the associated
    # data from the same input file matches.
    for fastafile,vs1 in tag_and_variable_sites_f1.items():
        vs2 = tag_and_variable_sites_f2[fastafile]

        assert vs1 == vs2, f"Files have different details for variable sites concerning the `{fastafile}` pair: {sel1} vs {sel2}"

    return True  # If we get here, the files have same FASTA file number and variable sites info



def compare_file_number_and_variable_sites_in_log(file1_path, file2_path, msg="Files are not identical in content, ignoring whitespace differences."):
    '''
    Compare number of number of FASTA files selected and variable sites info in 
    two specified log files

    Has a default assertion message, but you can pass your own string as third
    argument in call or only pass the two paths and use the default.
    '''
    assert compare_log_info(file1_path, file2_path), msg



#import the shared helper function from `conftest.py`
#from conftest import make_corresponding_GUIobtained_filename

# import the function that gives string `example_datasets_location` because cannot
# use a pytest fixture to pass this one since used in `@pytest.mark.parametrize()`
# that seemed incompatible with fixtures
'''
from conftest import get_example_datasets_location
example_datasets_location = get_example_datasets_location()
'''
###--------------------------END OF HELPER FUNCTIONS--------------------------###
###--------------------------END OF HELPER FUNCTIONS--------------------------###







# Check the FGIJ-source generated files match the corresponding script files
#--------------------------------------------------------------------------#
# Maybe start with just seeing if content okay and then up level to check if
# entire HTML matches
#`html_pairs_to_process` comes from conftest (which gets it from `my_conftest_for_test_missing_residue_detailer.py`), passing into here via pytest fixture
#`text_pairs_to_process` comes from conftest (which gets it from `my_conftest_for_test_missing_residue_detailer.py`), passing into here via pytest fixture

''' Need anything like this here?????
def test_current_result_matches_results_in_my_fork():
    assert filecmp.cmp(current_provided_example, provided_example_as_of_when_I_forked), "The current results Adam Bessa provides don't match what was there when I forked."
test_current_result_matches_results_in_my_fork()
'''

# most basic test of set-up of things for pytest. (Doesn't test processing of data though.) Tests that what I set up to pass variables in `my_conftest_for_test_missing_residue_detailer.py` and `conftest.py` passes a variable. 
def test_pytest_working_and_can_pass_fixtures_from_conftest_to_test_file(html_pairs_to_process, text_pairs_to_process, dir_2_put_test_files):  # Add the fixtures as parameters
    assert dir_2_put_test_files == "additional_nbs/tests/" 
    assert isinstance(html_pairs_to_process, list) 
    assert isinstance(text_pairs_to_process, list) 

# Get & Iterate on each pair and check if the text without HTML matches. Because
# if that fails, surely the more detailed HTML will fail.
def get_text_pairs_and_ids(directory):
    # Print what files we find to debug
    print(f"Looking in directory: {os.path.abspath(directory)}")
    fgij_files = glob.glob(os.path.join(directory, "fgij_text_*.txt"))
    print(f"Found fgij files: {fgij_files}")
    
    pairs_and_ids = []
    for fgij_file in fgij_files:
        # Extract ID from filename
        id_part = os.path.basename(fgij_file).split('_')[-1].split('.')[0]
        # Find matching fmrd file
        fmrd_file = os.path.join(directory, f"fmrd_text_{id_part}.txt")
        print(f"Looking for matching file: {fmrd_file}")
        if os.path.exists(fmrd_file):
            pairs_and_ids.append(((os.path.basename(fgij_file), 
                                 os.path.basename(fmrd_file)), 
                                id_part))
    return pairs_and_ids


# Get pairs and IDs from the correct directory
#test_dir = "additional_nbs/tests" # I had hoped to avoid having this in multiple places, so let's see if this works: (IT does and so I don't know why cannot use those not fixtures to pass things. Maybe only fixtures allowed in tests?)
from my_conftest_for_test_missing_residue_detailer import TEST_FILES_DIR
test_dir = TEST_FILES_DIR
pairs_and_ids = get_text_pairs_and_ids(test_dir)
pairs, ids = zip(*pairs_and_ids)


def generate_test_name(val):
    """Generates a custom test ID for each test case.
    Args:
        int: interger for index position.
    Returns:
        A string representing the custom test ID.
    """
    return f"From {ids[val]}"

#@pytest.mark.parametrize("pair_index", range(len(pairs)), ids=ids) # works to give PDB id code in brackets for end of name of function but I wanted to customize a bit further & so see next line
@pytest.mark.parametrize("pair_index", range(len(pairs)), ids=generate_test_name)

def test_text_files_match(pair_index, dir_2_put_test_files):
    """Test that each pair of text files have identical content."""
    file1, file2 = pairs[pair_index]
    assert filecmp.cmp(dir_2_put_test_files + file1, dir_2_put_test_files + file2, shallow=False), \
        f"Files {dir_2_put_test_files + file1} and {dir_2_put_test_files + file2} do not have identical content"
'''
# THIS EARLIER FORM WORKS BUT...
# Note that it appears it cannot be simpler because I am using 
# `text_pairs_to_process` from `conftest.py` and so cannot use in `@pytest.mark.parametrize()` direct because not yet define. This gets around that.
#BUT DOESN'T REALLY WORK With `ids` to name the tests  by the PDB id and if I use something like `request.node.name = f"test_text_files_match[{ids[pair_index]}]"` in the test, I am still hard coding in number and order with `"pair_index", [0, 1]`. SO THIS 
# IS FINE FOR TESTING SET UP INITIALLY BUT WILL LIMIT ME AS I HOPE TO ADD MORE
# details from more PDB diles to test.
@pytest.mark.parametrize("pair_index", [0, 1])
def test_text_files_match(text_pairs_to_process, pair_index, dir_2_put_test_files):
    """Test that each pair of text files have identical content."""
    file1, file2 = text_pairs_to_process[pair_index]
    assert filecmp.cmp(dir_2_put_test_files + file1, dir_2_put_test_files + file2, shallow=False), \
        f"Files {dir_2_put_test_files + file1} and {dir_2_put_test_files + file2} do not have identical content"
'''





# Now up the level to checking if the HTML matches. Get & Iterate on each pair .
def get_html_pairs_and_ids(directory):
    # Print what files we find to debug
    print(f"Looking in directory: {os.path.abspath(directory)}")
    fgij_files = glob.glob(os.path.join(directory, "fgij_html_*.html"))
    print(f"Found fgij files: {fgij_files}")
    
    pairs_and_ids = []
    for fgij_file in fgij_files:
        # Extract ID from filename
        id_part = os.path.basename(fgij_file).split('_')[-1].split('.')[0]
        # Find matching fmrd file
        fmrd_file = os.path.join(directory, f"fmrd_html_{id_part}.html")
        print(f"Looking for matching file: {fmrd_file}")
        if os.path.exists(fmrd_file):
            pairs_and_ids.append(((os.path.basename(fgij_file), 
                                 os.path.basename(fmrd_file)), 
                                id_part))
    return pairs_and_ids

# Get pairs and IDs from the correct directory
hpairs_and_ids = get_html_pairs_and_ids(test_dir)
hpairs, hids = zip(*hpairs_and_ids)

#@pytest.mark.parametrize("pair_index", range(len(pairs)), ids=hids) # works to give PDB id code in brackets for end of name of function but I wanted to customize a bit further & so see next line
@pytest.mark.parametrize("pair_index", range(len(pairs)), ids=generate_test_name)
def test_html_files_match(pair_index, dir_2_put_test_files):
    """Test that each pair of text files have identical content."""
    file1, file2 = pairs[pair_index]
    assert filecmp.cmp(dir_2_put_test_files + file1, dir_2_put_test_files + file2, shallow=False), \
        f"Files {dir_2_put_test_files + file1} and {dir_2_put_test_files + file2} do not have identical content"

