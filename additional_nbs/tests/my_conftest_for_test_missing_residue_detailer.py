#!/usr/bin/env python
# this goes in same folder with `conftest.py` that will be for 
# `test_missing_residue_detailer.py` 
# `conftest.py` is a special file that pytest automatically finds and uses, but 
# I don't won't poorly named file so putting most of actual content dictating
# what `conftest.py` should do & generate in here and directing `conftest.py` to
# utilize this.
# Note that because it isn't part of the HTML table, I don't bother testing the 
# top line of the report because I focus on table HTML that is easy to 
# specifically collect. I ned to set things up so that will be thee case and it
# is easist to do using conftest step where I am making the output to test.

import pytest
import os
import fnmatch
import urllib3
import certifi
import filecmp
from bs4 import BeautifulSoup
from shutil import move
from shutil import copyfile


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
suffix_4_results = "_missing_residue_details.html" # Has to match what 
# `missing_residue_detailer.py` has for this.
file_input_suffix = "_header4missing.txt" # Has to match what 
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

# Follow convention of variable name with PDB code between `fgij_` and `_main_table_html` to add new ones. Use Chrome DEveloper Tools to get Element where table starts with `'<table cellpadding="2">`
fgij_4dqo_main_table_html = '''<table cellpadding="2"><tbody><tr><td>Chain(s)</td><td>Missing<br>Residues</td><td>Missing<br>Charges*</td><td>Segment Ranges</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>246</b> residues of Protein including 2 <a href="javascript: showLigNSRHelp()">non-standard residue(s)</a> (no <a href="http://proteopedia.org/wiki/index.php/Selenomethionine" target="_blank">selenomethonine</a> [MSE]):</center></td></tr><tr><td> H</td><td><center>6</center></td><td><font color="red">1-</font>, 0+</td><td>217-222</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>216</b> residues of Protein:</center></td></tr><tr><td> L</td><td><center>2</center></td><td>0</td><td>211-212</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>124</b> residues of Protein:</center></td></tr><tr><td> C</td><td><center>36</center></td><td><font color="red">7-</font>, 0+</td><td>118-118, 143-152, 178-178P, 239-246</td></tr></tbody></table>'''
fgij_6w6v_main_table_html = '''<table cellpadding="2"><tbody><tr><td>Chain(s)</td><td>Missing<br>Residues</td><td>Missing<br>Charges*</td><td>Segment Ranges</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>340</b> residues of RNA:</center></td></tr><tr><td> A</td><td><center>46</center></td><td>&nbsp;</td><td>1-1, 53-56, 132-143, 170-173, 203-207, 220-224, 242-246, 285-289, 336-340</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>875</b> residues of Protein:</center></td></tr><tr><td> B</td><td><center>95</center></td><td><font color="red">7-</font>, <font color="blue">16+</font></td><td>1-70, 125-137, 692-694, 741-749</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>279</b> residues of Protein:</center></td></tr><tr><td> D</td><td><center>67</center></td><td><font color="red">10-</font>, <font color="blue">11+</font></td><td>1-67</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>173</b> residues of Protein:</center></td></tr><tr><td> E</td><td><center>4</center></td><td><font color="red">3-</font>, 0+</td><td>1-1, 171-173</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>158</b> residues of Protein:</center></td></tr><tr><td> F</td><td><center>0</center></td><td>&nbsp;</td><td>&nbsp;</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>140</b> residues of Protein:</center></td></tr><tr><td> G</td><td><center>14</center></td><td><font color="red">3-</font>, <font color="blue">2+</font></td><td>1-5, 107-115</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>133</b> residues of Protein:</center></td></tr><tr><td> H</td><td><center>8</center></td><td><font color="red">1-</font>, <font color="blue">2+</font></td><td>1-3, 129-133</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>293</b> residues of Protein:</center></td></tr><tr><td> J</td><td><center>0</center></td><td>&nbsp;</td><td>&nbsp;</td></tr><tr><td> I</td><td><center>50</center></td><td><font color="red">7-</font>, <font color="blue">7+</font></td><td>244-293</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>198</b> residues of Protein:</center></td></tr><tr><td> K</td><td><center>119</center></td><td><font color="red">14-</font>, <font color="blue">24+</font></td><td>1-2, 82-198</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>201</b> residues of Protein:</center></td></tr><tr><td> L</td><td><center>80</center></td><td><font color="red">11-</font>, <font color="blue">19+</font></td><td>54-60, 129-201</td></tr></tbody></table>'''

fgij_4hix_main_table_html = '''<table cellpadding="2"><tbody><tr><td>Chain(s)</td><td>Missing<br>Residues</td><td>Missing<br>Charges*</td><td>Segment Ranges</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>227</b> residues of Protein:</center></td></tr><tr><td> H</td><td><center>8</center></td><td>0</td><td>215-222</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>220</b> residues of Protein:</center></td></tr><tr><td> L</td><td><center>1</center></td><td><font color="red">1-</font>, 0+</td><td>0-0</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>28</b> residues of Protein:</center></td></tr><tr><td> A</td><td><center>22</center></td><td><font color="red">4-</font>, <font color="blue">2+</font></td><td>7-28</td></tr></tbody></table>'''

fgij_1d66_main_table_html = '''<table cellpadding="2"><tbody><tr><td>Chain(s)</td><td>Missing<br>Residues</td><td>Missing<br>Charges*</td><td>Segment Ranges</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>19</b> residues of DNA:</center></td></tr><tr><td> D</td><td><center>0</center></td><td>&nbsp;</td><td>&nbsp;</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>19</b> residues of DNA:</center></td></tr><tr><td> E</td><td><center>0</center></td><td>&nbsp;</td><td>&nbsp;</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>66</b> residues of Protein:</center></td></tr><tr><td> A, B</td><td><center>9</center></td><td><font color="red">1-</font>, <font color="blue">1+</font></td><td>1-7, 65-66</td></tr></tbody></table>'''

fgij_4ifd_main_table_html = '''<table cellpadding="2"><tbody><tr><td>Chain(s)</td><td>Missing<br>Residues</td><td>Missing<br>Charges*</td><td>Segment Ranges</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>304</b> residues of Protein:</center></td></tr><tr><td> A</td><td><center>4</center></td><td><font color="red">1-</font>, <font color="blue">1+</font></td><td>302-305</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>248</b> residues of Protein:</center></td></tr><tr><td> B</td><td><center>6</center></td><td>0-, <font color="blue">1+</font></td><td>(-1)-0, 243-246</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>393</b> residues of Protein:</center></td></tr><tr><td> C</td><td><center>55</center></td><td><font color="red">21-</font>, <font color="blue">4+</font></td><td>2-6, 100-120, 194-205, 310-326</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>245</b> residues of Protein:</center></td></tr><tr><td> D</td><td><center>22</center></td><td><font color="red">3-</font>, <font color="blue">7+</font></td><td>(-21)-0</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>267</b> residues of Protein:</center></td></tr><tr><td> E</td><td><center>0</center></td><td>&nbsp;</td><td>&nbsp;</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>250</b> residues of Protein:</center></td></tr><tr><td> F</td><td><center>37</center></td><td><font color="red">7-</font>, <font color="blue">4+</font></td><td>1-3, 23-41, 150-162, 249-250</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>242</b> residues of Protein:</center></td></tr><tr><td> G</td><td><center>6</center></td><td><font color="red">2-</font>, <font color="blue">1+</font></td><td>(-1)-0, 237-240</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>361</b> residues of Protein:</center></td></tr><tr><td> H</td><td><center>66</center></td><td><font color="red">11-</font>, <font color="blue">4+</font></td><td>(-1)-1, 18-49, 246-274, 358-359</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>301</b> residues of Protein:</center></td></tr><tr><td> I</td><td><center>71</center></td><td><font color="red">13-</font>, <font color="blue">7+</font></td><td>(-8)-0, 72-98, 114-125, 163-184, 292-292</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>1003</b> residues of Protein:</center></td></tr><tr><td> J</td><td><center>55</center></td><td><font color="red">16-</font>, <font color="blue">2+</font></td><td>(-1)-8, 238-248, 330-363</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>179</b> residues of Protein:</center></td></tr><tr><td> K</td><td><center>98</center></td><td><font color="red">15-</font>, <font color="blue">18+</font></td><td>515-531, 558-564, 620-693</td></tr><tr><td colspan="4" bgcolor="#d8d8d8"><center><b>45</b> residues of RNA:</center></td></tr><tr><td> R</td><td><center>15</center></td><td>&nbsp;</td><td>(-45)-(-45), (-29)-(-16)</td></tr></tbody></table>'''

# make a dictionary to match the content to the PDB id. Key is PDB accession
# code and the values are the string the HTML stored in.
# Originally this was hardcoded like the docstring section below
'''
fgij_correspondences_dict = {
                            '6w6v':fgij_6w6v_main_table_html, 
                            '4dqo':fgij_4dqo_main_table_html
                            }
'''
# However, it would be better for making it easier to expand with addition of more main table html content if automated making this. This does that as long as the names of the docstrings follow the same convention like `fgij_4dqo_main_table_html` with PDB code after `fjig_`:
def create_fgij_dict():
    """
    Creates a dictionary mapping PDB IDs to their corresponding HTML table strings
    by finding all variables in the global scope that match the pattern
    'fgij_XXXX_main_table_html' where XXXX is the PDB ID.
    
    Returns:
        dict: Dictionary with PDB IDs as keys and HTML strings as values

    THIS MAKES IT MUCH EASIER TO ADD MORE EXAMPLES OF `fgih_XXXX_main_table_html` 
    like fgij_4dqo_main_table_html` docstrings because just have to add them and 
    then everything else to test what the script will make from the same PDB id
    will be done automatically.  
    """
    # Get variables from global scope
    all_vars = list(globals().items())
    
    # Find variables matching our pattern
    fgij_dict = {}
    for var_name, value in all_vars:
        if var_name.startswith('fgij_') and var_name.endswith('_main_table_html'):
            pdb_id = var_name.replace('fgij_', '').replace('_main_table_html', '')
            if len(pdb_id) == 4:
                fgij_dict[pdb_id] = value
    
    return fgij_dict
fgij_correspondences_dict = create_fgij_dict()
# Note original hardcoded way I define `fgij_correspondences_dict` early on is just above this.

# from Eric Martz's FirstGlance in Jmol moltab.js, the section from there that is below could be used to expand the tests to be more representative:
'''
// missingPerChainInfo 2D array format
// 2D array format: chain name, missing count, missneg, misspos,
// Each missing sequence range segment has 4 values:
//   firstseq, firstseq-insertion-code, lastseq, lastseq-insertion-code
//
// Test cases:
// 2jqo none missing (NMR).
// 1nzp 1nzp: A 1 241 241 (single residue missing)
// 1o9a 1o9a: B 12 1 12 (CHAIN A, SEQDIFF FROM B, HAS NONE MISSING)
// EXAMPLE NEEDED: CHAIN WITH NONE MISSING SEQID TO CHAIN WITH SOME MISSING.
// 4asw 4asw: ["A", 13, 1, 13] ["B", 13, 1, 13]  ["C", 4, 16, 19]
//    total all chains: 30
// ABOVE EXAMPLES HAVE ONLY ONE MISSING SEGMENT PER CHAIN
// BELOW HAVE >ONE MISSING SEGMENT PER CHAIN
// 2ace 2ace: A 10 1 3 485 489 536 537 ONE CHAIN
// 1d66 1d66: A 9 1 7 65 66, B 9 1 7 5 66 TWO CHAINS
//
// 1tzn: 28 chains, 140 missing residues in 14 chains.
// 3fic: 27 chains, 27 missing residues in 1 chain.
// 3jqo=3JQO: 42 chains (3 distinct), 635 missing residues (32, 5, 8 per chain).
//   VARIABLE MISSING IN 2 OF 3 CHAINS.
// 3lo3: 28 chains (1 distinct), 0 missing residues. TWO CHAIN LINES.
//
// 4hix has 1 residue numbered 0 missing in chain L.
// 4en3 has missing with neg seq nums and 0.
// 2lex has missing DNA (2-letter residue names).
// 4ifd has missing RNA (1-letter residue names) among 435 missing residues
//   in 12 distinct chains <====== good xmpl of table simplifying.
// 4dqo has missing amino acids with INSERTION CODES.
// 1ucy has missing amino acids with INSERTION CODES in REVERSE alpha order!
//   also has a missing residue in just 1 of 3 seqID chains!
// 3nn8 has 2 sets of seqID chains, each set has some missing, some not.
// 4gxu has 926 missing AA - good xmpl of table simplifying! <==========
// 4dep has 174 missing AA, many negs, good xmpl of table simplifying! <==========
// 3omz has chain G length 259 with 156 missing (more than half!)
'''

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

def get_using_curl(script_needed):
    '''
    Use curl which will work on MyBinder sessions where I plan to do the testing
    for now.
    Might not work if I shift to JupyterLite and so having this modularized in
    this way will make it easier to shift later
    '''
    if not os.path.isfile(script_needed):
        os.system("curl -OL https://raw.githubusercontent.com/"\
            "fomightez/structurework/refs/heads/master/"\
            f"PDBmodelComparator-utilities/{script_needed}")

def get_content_atURL_with_URLLIB3(url, chunk_size=64):
    '''
    Get content with the urllib3 library, which offers more advanced retry and 
    streaming capabilities than Requests.
    And works in JupyterLite.
    '''
    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where(),
        retries=urllib3.Retry(
            total=3,
            backoff_factor=0.1,
            status_forcelist=[500, 502, 503, 504]
        )
    )
    try:
        response = http.request('GET', url, preload_content=False)
        collected = ''
        chunk_count = 0
        while True:
            chunk = response.read(chunk_size)
            if not chunk:
                break
            chunk_count += 1
            collected += chunk.decode(errors='ignore')
        response.release_conn()
        return collected, chunk_count
    except urllib3.exceptions.ChunkedEncodingError as ex:
        print(f"Specific ChunkedEncodingError: {ex}")
        return collected, chunk_count
    except Exception as ex:
        print(f"General error: {ex}")
        return None, 0
def get_script_using_URLLIB3(script_needed):
    '''
    Get script using the urllib3 library, which offers more advanced retry and 
    streaming capabilities than Requests.
    And works in JupyterLite.
    '''
    if not os.path.isfile(script_needed):
        url = ("https://raw.githubusercontent.com/fomightez/structurework/master"
        "/PDBmodelComparator-utilities/"+script_needed)
        r_text, _ = get_content_atURL_with_URLLIB3(url)
        with open(script_needed, 'w') as filehandler:
            filehandler.write(r_text)

def get_script_if_needed(script_needed):
    '''
    fetch script if needed

    `curl` may not work and so by having a generic function I can use in 
    multiple places in the same script, I only need to change this script to
    handle the change to another method in multiple places.
    '''
    #get_using_curl(script_needed)
    get_script_using_URLLIB3(script_needed)

def write_string_to_file(s, fn):
    '''
    Takes a string, `s`, and a name for a file & writes the string to the file.
    '''
    with open(fn, 'w') as output_file:
        output_file.write(s)

def remove_text_up_to_string(file_path, target_string):
    '''
    self-explanatory function to remove everything before the supplied string
    '''
    with open(file_path, 'r') as file:
        content = file.read()
    index = content.find(target_string)
    if index != -1:
        # Just use index, not index + len(target_string)
        new_content = content[index:]
        with open(file_path, 'w') as file:
            file.write(new_content)

def trim_to_HTML_table(fn_made_by_script):
    '''
    takes a string with the name of the html file made by the script `missing_residue_detailer.py` and takes off everything in front of the first
    occurence of the text `<table ` to leave just the missing residues HTML file that
    is easy to collect and check against.

    Though this means the line like at the start of output for 6w6v that is `
    483 Missing Residues` won't get checked, it isn't a big deal and that data 
    that number is composed of gets checked in HTML table.
    '''
    remove_text_up_to_string(fn_made_by_script, "<table ")


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
# Set-up for the tests that will be done in the corresponding test file.
#**                                                                      **#
# First, get a header for a structure and save it as a file to be used in a test
# as to whether the script will recognize and use a text file supplied in the 
# expected way as the source of the information to be used. In this case the
# header to be used is from 1d66 but the PDB id code the file will have will be
# a non-existent one. So the only way the script will produce output is if it
# uses the supplied file. It cannot get the header from network because doesn't
# exist. Since using content corresponding to 1d66, output should look like 1d66
# PREP FOR `test_file_can_be_used_as_source`
source_data_for_file_read_test = '1d66_PDB_header_text_to_test_file_reading.txt'
PDB_code_for_file_read_test = "4tSt" # This PDB doesn't exist according to 
# https://proteopedia.org/wiki/index.php/Believe_It_or_Not#Notes & 
# https://proteopedia.org/wiki/index.php/4tst
# "4tst is a useful PDB id for a non-existing structure", even if
# account for case insensitivity. This dummy PDB id code seems better than using 
# zero in front of alphanumerics as initially did, see footnote to the statement 
# " This could be increased to 466,560 if the numeral "0" is allowed as the 
# first character[3]" at https://proteopedia.org/wiki/index.php/PDB_code#Limited_Number_of_4-Character_PDB_Codes.
# Because that one doesn't exist. The only data that will be valid is if use my
# supplied file as source.
file_needed = PDB_code_for_file_read_test + file_input_suffix
if not os.path.isfile(file_needed): #only supply the file if haven't already
    copyfile(TEST_FILES_DIR + source_data_for_file_read_test, file_needed)
output_expected = PDB_code_for_file_read_test.lower() + suffix_4_results
script_needed = "missing_residue_detailer.py"
get_script_if_needed(script_needed) # needed soon & so grab if not present yet
os.system(
    f'python missing_residue_detailer.py {PDB_code_for_file_read_test}')
#trim_to_HTML_table(output_expected) # see about trim_to_HTML_table below; may need here if I update related test to check content
move(output_expected,  TEST_FILES_DIR +output_expected) # move expected to 
# location of test files
# Now that used when run script, can move file used to test to BACK to
# the location of test files
move(file_needed, TEST_FILES_DIR + file_needed)

# Second, make the text files needed for the First Glance in Jmol content that I 
# have.
# PREP FOR `test_text_files_match` and `test_html_files_match`
# Then make the corresponding files for those with the results from  
# `missing_residue_detailer.py`
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
    get_script_if_needed(script_needed) # needed soon & so grab if not here yet
    #make each result, and then move both to `TEST_FILES_DIR`
    file_needed = current_script_html_fn
    if not os.path.isfile(TEST_FILES_DIR + file_needed): #only make the 
        # file if haven't already
        os.system(f'python missing_residue_detailer.py {pdb_id}')
        # Remove everything from the output that is prior to `<table `. This way
        # the test that will come are focused on the HTML table that is easy to 
        # collect and not the first part of the report, which is really just the
        # total of the missing residies and so is redundant with information
        # in the HTML table. As it probably be clearer with an example: 
        # basically, aside some boiler plate text, the only thing it gets rid 
        # of is the line `483 Missing Residues` ,for the case of 6w6v.
        trim_to_HTML_table(pdb_id + suffix_4_results)
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