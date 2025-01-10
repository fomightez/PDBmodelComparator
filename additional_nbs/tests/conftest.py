#!/usr/bin/env python
# this goes with `test_no_changes_introduced_to_results.py` 
# `conftest.py` is a special file that pytest automatically 
# discovers and uses and so you can use that to set up things and tear down (if
# desired/needed) the environment before tests run.
import pytest
import sys
import os
import fnmatch
import uuid
from shutil import move



#*******************************************************************************
##################################
#  FILE PATHS       #

##################################
#

# So far only two used here. Rest set in 
# `test_no_changes_introduced_to_results.py`. The two set here will hopefully be
# propagated  to there. (works so far with only `dir_with_new_results`)
dir_with_new_results = "tests/new_results"
example_datasets_location = "Example_data/Datasets"
# Create fixture to make the `dir_with_new_results`variable available to tests 
#, special handling needed with `example_datasets_location` (see below)
@pytest.fixture(scope="session")
def dir_with_new_results_set_inCONFTEST():
    return dir_with_new_results
# I also wanted to pass `example_datasets_location` but fixture couldn't be 
# used with `@pytest.mark.parametrize()` so passed result via importing 
# function below. THAT WAS SUPER TRICKY TO WORK OUT.
#(sort of wish I had realized how to pass `example_datasets_location` earlier
# because I ended up needing an intermediate to pass `dir_with_new_results` 
# because it was at the module level and kept confusing function 
# `dir_with_new_results` with string and intermediate was way I went aroudn that
# but could have used import the funciton that returned it and been consistent.
# In a way I guess it is okay because this file illustrates three ways to pass
# variables in between `conftest.py` and the pytest test document and that will
# be handy to know)
#
#*******************************************************************************
#*****************************END FILE PATHS************************************







#*******************************************************************************
##################################
#  USER ADJUSTABLE VALUES        #

##################################
#

import datetime
now = datetime.datetime.now()
log_tests_prefix = "tests_results_log"
tests_log = f"{log_tests_prefix}{now.strftime('%b%d%Y%H%M')}.txt" #log 
# wtih a date/timestamp

#
#*******************************************************************************
#**********************END USER ADJUSTABLE VARIABLES****************************








#*******************************************************************************
#*******************************************************************************
###DO NOT EDIT BELOW HERE - ENTER VALUES ABOVE###



###---------------------------HELPER FUNCTIONS-------------------------------###

def _(row):
    '''
    takes the row and .... PLACEHOLDER FOR NOW
    '''
    return _

def generate_output_file_name_AS_IMPROVED_DOES(file_name):
    '''
    Need to make output name when process single path as `improved_Fasta2Structure.py`
    does. THIS DOES THAT LIKE THE SCRIPT WOULD, so get actual name.
    Takes a file name as an argument and returns string for the name of the
    output file. The generated name is based on the original file
    name.

    Specific example
    ================
    Calling function with
        ("ITS.fas")
    returns
        "ITS_Structure.str"
    '''
    main_part_of_name, file_extension = os.path.splitext(
        file_name) #from http://stackoverflow.com/questions/541390/extracting-extension-from-filename-in-python
    if '.' in file_name:  #I don't know if this is needed with the os.path.splitext method but I had it before so left it
        return main_part_of_name + "_Structure" + ".str"
    else:
        return file_name + ".str"
def get_example_datasets_location():
    return example_datasets_location

def make_temp_base_filename(filename_prefix):
    '''
    Takes a string and makes a base file name that nothing should match 
    based on the provided prefix and uuid use.
    '''
    return "tmp_{}_{}_{}".format(filename_prefix,uuid.uuid4().time,now.strftime('%b%d%Y%H%M'))


def write_string_to_file(s, fn):
    '''
    Takes a string, `s`, and a name for a file & writes the string to the file.
    '''
    with open(fn, 'w') as output_file:
        output_file.write(s)




###--------------------------END OF HELPER FUNCTIONS--------------------------###
###--------------------------END OF HELPER FUNCTIONS--------------------------###



def pytest_configure(config):
    '''
    Prepare for tests to be run by seting up situation.

    Repo will already have results made by with Fasta2Structure.py via GUI. So
    now also need what current (possibly new) version of 
    `improved_Fasta2Structure.py` script makes. That sets up things so that then
    can check via running the test how new versions compare to old stored versions.
    '''
    #global dir_with_new_results # need this here to bring this in?
    print("To set up for tests, run `improved_Fasta2Structure.py` with the example datasets...")
    os.makedirs(dir_with_new_results, exist_ok=True)
    #make the results for the individual files in the `Example_data/Datasets`
    # Iterate on names in `Example_data/Datasets/` & process each one separate
    # fasta_fps = glob.glob(f'{example_datasets_location}/*.fas')
    ind_results_noms = [] # while making collect the names
    ind_log_noms = []
    for filename in os.listdir(example_datasets_location):
        if fnmatch.fnmatch(filename, '*.fas'):
            unique_namePrefix_for_new = make_temp_base_filename(filename)
            full_path2match = os.path.join(example_datasets_location, filename)
            #make each result, moving to `dir_with_new_results` with better name
            os.system(f'python improved_Fasta2Structure.py {full_path2match}')
            result_str = generate_output_file_name_AS_IMPROVED_DOES(filename)
            unique_result_nom = f"{unique_namePrefix_for_new}_Structure.str"
            unique_log_nom = f"{unique_namePrefix_for_new}_log.log"
            move(result_str, f"{dir_with_new_results}/{unique_result_nom}")
            ind_results_noms.append(unique_result_nom)
            move("log.log", f"{dir_with_new_results}/{unique_log_nom}")
            ind_log_noms.append(unique_log_nom)
    

    # make the result for all three genes targeted at once
    three_nom_prefix = "from_all_three_at_once"
    unique_prefix_for_with_three = make_temp_base_filename(three_nom_prefix)
    os.system('python improved_Fasta2Structure.py Example_data/Datasets/ITS.fas Example_data/Datasets/trnD-trnT.fas Example_data/Datasets/trnH-trnK.fas')
    # move the results to `dir_with_new_results` & give better name
    move("Structure.str", f"{dir_with_new_results}/{unique_prefix_for_with_three}_Structure.str")
    move("log.log", f"{dir_with_new_results}/{unique_prefix_for_with_three}_log.log")

    # To set up for making fixtures to pass information to the tests store the 
    # data in pytest cache. (Need to use pytest cache because "it's important to note that pytest_configure runs before any fixtures are created, so you can't directly use fixtures to pass data from this function.")
    config.cache.set('ind_results_noms', ind_results_noms)
    config.cache.set('ind_log_noms', ind_log_noms)
    config.cache.set('three_nom_prefix', three_nom_prefix)
    config.cache.set('unique_prefix_for_with_three', unique_prefix_for_with_three)



# Create fixtures to access the cached data to make `ind_results_noms` & 
# `ind_log_noms`, `three_nom_prefix` & `unique_prefix_for_with_three` variables 
# available to tests
@pytest.fixture(scope="session")
def ind_results_noms(pytestconfig):
    return pytestconfig.cache.get('ind_results_noms', [])

@pytest.fixture(scope="session")
def ind_log_noms(pytestconfig):
    return pytestconfig.cache.get('ind_log_noms', [])

@pytest.fixture(scope="session")
def three_nom_prefix(pytestconfig):
    return pytestconfig.cache.get('three_nom_prefix', [])

@pytest.fixture(scope="session")
def unique_prefix_for_with_three(pytestconfig):
    return pytestconfig.cache.get('unique_prefix_for_with_three', [])
