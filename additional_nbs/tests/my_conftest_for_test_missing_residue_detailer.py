#!/usr/bin/env python
# this goes in same folder with `conftest.py` that will be for 
# `test_missing_residue_detailer.py` 
# `conftest.py` is a special file that pytest automatically finds and uses, but 
# I don't won't poorly named file so putting most of actual content dictating
# what `conftest.py` should do & generate in here and directing `conftest.py` to
# utilize this.

import pytest
import os
import fnmatch
import filecmp
from bs4 import BeautifulSoup
from shutil import move


#*******************************************************************************
##################################
#  USER ADJUSTABLE VALUES        #

##################################
#
firstglanceinjmol_hmtl_file_prefix = "fgij_html_"
missingresiduedetailer_hmtl_prefix = "fmrd_html_"
#
firstglanceinjmol_text_file_prefix = "fgij_text_"
missingresiduedetailer_text_prefix = "fmrd_text_"
suffix_4_results = "_missing_residue_details.txt" # Has to match what 
# `missing_residue_detailer.py` has for this.


#
#*******************************************************************************
#**********************END USER ADJUSTABLE VARIABLES****************************



#*******************************************************************************
##################################
#  FILE PATHS       #

##################################
#

TEST_FILES_DIR = "additional_nbs/tests/" 

#
#*******************************************************************************
#*****************************END FILE PATHS************************************








#*******************************************************************************
#########################################################
#  MISSING RESIDUE DATA FROM FIRST GLANCE IN JMOL       #

#########################################################
#

fgij_4dqo_main_table_html = '''<table cellpadding="2"><tbody><tr><td>Chain(s)</td><td>Missing<br>Residues</td><td>Missing<br>Charges*</td><td>Segment Ranges</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>246</b> residues of Protein including 2 <a href="javascript: showLigNSRHelp()">non-standard residue(s)</a> (no <a href="http://proteopedia.org/wiki/index.php/Selenomethionine" target="_blank">selenomethonine</a> [MSE]):</center></td></tr><tr><td> H</td><td><center>6</center></td><td><font color="red">1-</font>, 0+</td><td>217-222</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>216</b> residues of Protein:</center></td></tr><tr><td> L</td><td><center>2</center></td><td>0</td><td>211-212</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>124</b> residues of Protein:</center></td></tr><tr><td> C</td><td><center>36</center></td><td><font color="red">7-</font>, 0+</td><td>118-118, 143-152, 178-178P, 239-246</td></tr></tbody></table>'''
fgij_6w6v_main_table_html = '''<table cellpadding="2"><tbody><tr><td>Chain(s)</td><td>Missing<br>Residues</td><td>Missing<br>Charges*</td><td>Segment Ranges</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>340</b> residues of RNA:</center></td></tr><tr><td> A</td><td><center>46</center></td><td>&nbsp;</td><td>1-1, 53-56, 132-143, 170-173, 203-207, 220-224, 242-246, 285-289, 336-340</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>875</b> residues of Protein:</center></td></tr><tr><td> B</td><td><center>95</center></td><td><font color="red">7-</font>, <font color="blue">16+</font></td><td>1-70, 125-137, 692-694, 741-749</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>279</b> residues of Protein:</center></td></tr><tr><td> D</td><td><center>67</center></td><td><font color="red">10-</font>, <font color="blue">11+</font></td><td>1-67</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>173</b> residues of Protein:</center></td></tr><tr><td> E</td><td><center>4</center></td><td><font color="red">3-</font>, 0+</td><td>1-1, 171-173</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>158</b> residues of Protein:</center></td></tr><tr><td> F</td><td><center>0</center></td><td>&nbsp;</td><td>&nbsp;</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>140</b> residues of Protein:</center></td></tr><tr><td> G</td><td><center>14</center></td><td><font color="red">3-</font>, <font color="blue">2+</font></td><td>1-5, 107-115</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>133</b> residues of Protein:</center></td></tr><tr><td> H</td><td><center>8</center></td><td><font color="red">1-</font>, <font color="blue">2+</font></td><td>1-3, 129-133</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>293</b> residues of Protein:</center></td></tr><tr><td> J</td><td><center>0</center></td><td>&nbsp;</td><td>&nbsp;</td></tr><tr><td> I</td><td><center>50</center></td><td><font color="red">7-</font>, <font color="blue">7+</font></td><td>244-293</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>198</b> residues of Protein:</center></td></tr><tr><td> K</td><td><center>119</center></td><td><font color="red">14-</font>, <font color="blue">24+</font></td><td>1-2, 82-198</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>201</b> residues of Protein:</center></td></tr><tr><td> L</td><td><center>80</center></td><td><font color="red">11-</font>, <font color="blue">19+</font></td><td>54-60, 129-201</td></tr></tbody></table>'''

# make a dicitonary to match the content to the PDB id. Key is PDB accession
# code and the values are the string the HTML stored in
fgij_correspondences_dict = {
                            '6w6v':fgij_6w6v_main_table_html, 
                            '4dqo':fgij_4dqo_main_table_html
                            }

#
#*******************************************************************************
#*******END MISSING RESIDUE DATA FROM FIRST GLANCE IN JMOL**********************




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









# Set up
#--------------------------------------------------------------------------#
# Set-up for the tests that will be done below
# First make the text files needed for the First Glance in Jmol content that I 
# have.
# Then make the corresponding files for those with the results from  
# `missing_residue_detailer.py`
#
# THIS NEEDS TO BE moved to `conftest.py`, like used for 
# https://github.com/fomightez/Fasta2Structure-cli 

html_pairs_to_process_list = [] # this will be a list of the two element tuples 
# the HTML files to compare for the tests
text_pairs_to_process_list = [] # this will be a list of the two element tuples 
# the text files to compare for the tests

# Make the text files needed for the First Glance in Jmol content
# Can use keys in `fgij_correspondences_dict` to iterate on because the keys for 
# that are the PDBids I have content for
for pdb_id, corr_html_string in fgij_correspondences_dict.items():
    current_fgij_html_fn = generate_filename_from_prefix_andPDBid(
        firstglanceinjmol_hmtl_file_prefix,pdb_id)
    current_fgij_text_fn = generate_filename_from_prefix_andPDBid(
        firstglanceinjmol_text_file_prefix,pdb_id)
    file_needed = current_fgij_html_fn
    if not os.path.isfile(TEST_FILES_DIR + file_needed): #only make the 
        # file if haven't already
        write_string_to_file(corr_html_string, TEST_FILES_DIR + file_needed)
    # make text from HTML then save that as file
    corr_text_string = BeautifulSoup(corr_html_string,"html.parser").get_text() # based on 
    # https://stackoverflow.com/a/14694669/8508004 & warning I got without `"html.parser"`
    file_needed = current_fgij_text_fn
    if not os.path.isfile(TEST_FILES_DIR + file_needed): #only make the 
        # file if haven't already
        write_string_to_file(
            corr_text_string, TEST_FILES_DIR + file_needed)

    # Now while iterating on the same PDB id use `missing_residue_detailer.py` to 
    # make the corresponding content, both html and text as files
    current_script_html_fn = generate_filename_from_prefix_andPDBid(
        missingresiduedetailer_hmtl_prefix,pdb_id)
    current_script_text_fn = generate_filename_from_prefix_andPDBid(
        missingresiduedetailer_text_prefix,pdb_id)
    script_needed = "missing_residue_detailer.py"
    if not os.path.isfile(script_needed):
        os.system("curl -OL https://raw.githubusercontent.com/"\
            "fomightez/structurework/refs/heads/master/"\
            f"PDBmodelComparator-utilities/{script_needed}")
    #make each result, and then move both to `TEST_FILES_DIR`
    file_needed = current_script_html_fn
    if not os.path.isfile(TEST_FILES_DIR + file_needed): #only make the 
        # file if haven't already
        os.system(f'python missing_residue_detailer.py {pdb_id}')
        move(pdb_id + suffix_4_results, current_script_html_fn) # rename to what is needed for tests
    
        # Convert html from script to in-memory text. BEFORE MOVING HTML FILE. (And this won't work if made and moved file above already so place it under control of that conditional)
        with open(current_script_html_fn, 'r', encoding='utf-8') as file:
            html_content = file.read()
        text_from_script_html = BeautifulSoup(html_content,"html.parser").get_text() # based on 
        # https://stackoverflow.com/a/14694669/8508004 & warning I got without `"html.parser"`
        # Now that used to convert, can move HTML file to location of test files
        move(file_needed, TEST_FILES_DIR + file_needed)

    # save the in-memory text form from the html the script made, if needed.
    file_needed = current_script_text_fn
    if not os.path.isfile(TEST_FILES_DIR + file_needed): #only make the 
        # file if haven't already
        write_string_to_file(
            text_from_script_html, TEST_FILES_DIR + file_needed)
    
    html_pairs_to_process_list.append((current_fgij_html_fn,current_script_html_fn))
    text_pairs_to_process_list.append((current_fgij_text_fn,current_script_text_fn))





# Create fixtures to pass objects to be available to tests
#--------------------------------------------------------------------------#
# Create fixtures to access the cached data to make `html_pairs_to_process_list` & 
# `text_pairs_to_process_list`, & `TEST_FILES_DIR`/dir_2_put_test_files` variables available to tests
# Note that it is very important the variable used here and what will get passed 
# have different name (as annoying as that is) because if you have both a variable and a fixture with the same name, because otherwise when you use it in your test, you're getting the fixture function itself, not its return value. (Because you just defined it on the above line to now be the function.)
@pytest.fixture(scope="session")
def html_pairs_to_process():
    return html_pairs_to_process_list

@pytest.fixture(scope="session")
def text_pairs_to_process():
    return text_pairs_to_process_list

@pytest.fixture(scope="session")
def dir_2_put_test_files():
    return TEST_FILES_DIR