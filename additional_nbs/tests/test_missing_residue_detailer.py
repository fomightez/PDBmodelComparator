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
# Note that because it isn't part of the HTML table, I don't bother testing the 
# top line of the report because I focus on table HTML that is easy to 
# specifically collect. Handling of making it perform like this was done in `my_conftest_for_test_missing_residue_detailer.py`.

# To do yet:
# -possibly when more mature, update `test_file_can_be_used_as_source` to test
# it matches the HTML made by `missing_residue_detailer.py ` for 1d66 since that 
# header used. For now, `test_file_can_be_used_as_source` just makes sure there
# is output, which is mostly all that is needed for that test. Mostly.

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




def compare_file_content_equality(file1_path, file2_path, msg="Files are not identical in content, ignoring whitespace differences."):
    '''
    Compare two files content ignoring whitespace differences

    Has a default assertion message, but you can pass your own string as third
    argument in call or only pass the two paths and use the default.
    '''
    assert compare_files_content(file1_path, file2_path), msg



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

# This next test tests that a file with the proper name convention can be 
# supplied as souce of input data as instead of fetching PDB file header from 
# Protein Data Bank
def test_file_can_be_used_as_source(dir_2_put_test_files):  # Add the fixtures as parameters
    # I added later the ability to supply a file as the source the header. This 
    # should test that as it uses a PDB id code that does not exist and so the 
    # only way it will run to work and produce anything is if it uses the file
    # I supplied as source of header. (It cannot fall back to fetching & using 
    # something from Protein Data Bank.) Since using content corresponding to 
    # 1d66, output should look like what I expect for 1d66 output, which is 
    # among the PDB id codes tested below, but as written for now tests just 
    # makes sure output of some sort made by script.
    PDB_code_for_file_read_test = "4tSt" # "4tst is a useful PDB id for a non-existing structure"-https://proteopedia.org/wiki/index.php/Believe_It_or_Not
    suffix_4_results = "_missing_residue_details.html" # Has to match what 
    # `missing_residue_detailer.py` has for this.
    file_input_suffix = "_header4missing.txt" # Has to match what 
    # `missing_residue_detailer.py` has for this.
    file_used_as_input = PDB_code_for_file_read_test + file_input_suffix
    output_expected = PDB_code_for_file_read_test.lower() + suffix_4_results
    assert os.path.isfile(TEST_FILES_DIR + output_expected), \
        f"The expected file ouput {dir_2_put_test_files + output_expected} made using {file_used_as_input} as input does not exist"
    # the file used as input should also now be in the test files and have 1d66
    # header as content. Next assert test it at least the file is there.
    assert os.path.isfile(TEST_FILES_DIR + file_used_as_input), \
        f"The file {file_used_as_input} does not seem to have been moved back to the test location?"
    # FUTURE IMPROVEMENT: add when script more mature to see if content in `output_expected` matches HTML made by script for 1d66?


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
