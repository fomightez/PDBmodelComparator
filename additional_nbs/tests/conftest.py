#!/usr/bin/env python
# this goes in same folder with `test_missing_residue_detailer.py`  and 
# `my_conftest_for_test_missing_residue_detailer.py`.
# `conftest.py` is a special file that pytest automatically 
# discovers and uses and so you can use that to set up things and tear down (if
# desired/needed) the environment before tests run. (When I was workiing on
# https://github.com/fomightez/Fasta2Structure-cli  I just used conftest.py
# filled with what I needed to set things up, but now that I am on my second one
# of thest I am worried about not following what I should be using where and so
# putting stuff this time in better-named one and importing to the nondescript, 
# named one pytest expects!!)
# Note that I don't need tp wrap anything in `pytest_configure(config)` hook 
# here because just defining fixtures or importing them. The code will execute 
# when it's imported into `conftest.py`. You only need 
# `pytest_configure(config)` if you need to: 1. Access or modify the pytest 
# configuration object itself. 2. Ensure code runs at a very specific point in 
# pytest's startup sequence. 3. Register custom markers or do other 
# pytest-specific configuration
# And about `config.cache.set()`:
'''
You only need config.cache.set() if you want to persist values between different pytest runs. The cache survives after your tests finish, so it's useful for storing expensive computation results that you want to reuse the next time you run the tests.
Regular variables and session fixtures reset each time you run pytest. They persist during a single test run (that's what the "session" scope means), but start fresh in the next run.
So it depends on your needs:
If you just need values to persist during one test run: use top-level variables and session fixtures like in my last example
If you need values to persist between different test runs: use config.cache.set()
For most test configuration needs, the simpler approach with top-level variables and session fixtures is sufficient. The cache is more of a special-case tool for optimization.
'''
import pytest
import sys
import os
from my_conftest_for_test_missing_residue_detailer import generate_filename_from_prefix_andPDBid, write_string_to_file, html_pairs_to_process, text_pairs_to_process, dir_2_put_test_files

#Note, that if need to print in `conftest.py`, need to use `def pytest_configure(config):` and wrap it in there or else no output.