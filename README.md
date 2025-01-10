# PDBmodelComparator
Tool to generate an overviews between models of related macromolecular structures available in the Protein Data Bank.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/fomightez/PDBmodelComparator/main?urlpath=%2Flab%2Ftree%2Findex.ipynb)


*tl;dr:*  
Click any `launch binder` badge on this page to use the series of notebooks inside your browser without need for installing or logging in.

------


***PDBmodelComparator:  A tool to generate an overviews between models of related macromolecular structures available in the Protein Data Bank with demonstrations here.***

A launchable, working Jupyter-based environment served via MyBinder.org that has a collection of demonstrations of tool to generate an overviews between models of related macromolecular structures available in the Protein Data Bank.

If you have two or more models of essentially the same structure and are wondering which one has the information you seek, this tool is for you. It allows you to update the summaries as more related structures are solved.
Compares things like missing residues per chain, missing segments, percent of the biological chain oberved in the structure, whether data for either or both chain termini is intact. Additionally, it makes a separate summary of which structure has the most of a each chain represented.
It allows you to quickly & programmatically update the summaries as more related structures are solved.
The information incorporated can be customized with addiitonal knowledge as part of the process to make more informative summaries. Meaning you can incorporate your own expert /domain-specific knowledge to make the summaries even more useful in your own research group.

Meant to be self-contained and ready-to-go. No installations or copying of notebooks is necessary if `launch binder` is clicked. Everything will just work. 

-----

#### Related

- My [PDBmodelComparator-utilities sub-repo](https://github.com/fomightez/structurework/tree/master/PDBmodelComparator-utilities) for the associated scripts.

- My [pdbsum-utilities sub-repo](https://github.com/fomightez/structurework/tree/master/pdbsum-utilities) has a number of scripts, although I note the interface handling ones only deal with chains of protein-protein interfaces. These scripts are demonstrated in sessions that can be launched by pressing the `launch binder` button at my repo [pdbsum-binder](https://github.com/fomightez/pdbsum-binder).

- My repo [pdbsum-binder](https://github.com/fomightez/pdbsum-binder) demonstrates scripts from my [pdbsum-utilities sub-repo](https://github.com/fomightez/structurework/tree/master/pdbsum-utilities) that enable handling data from the [PDBsum](http://www.ebi.ac.uk/thornton-srv/databases/cgi-bin/pdbsum/GetPage.pl?pdbcode=index.html) with Jupyter/Python. Importantly, data from that site will only summarize interface surface area between protein chains of a structure. It does detail protein and nucleic acid residue-residue contacts but only graphically, and so I haven't found/developed a way to extract the data from there into Pandas dataframes yet.

- My repo [pdbepisa-binder](https://github.com/fomightez/pdbepisa-binder) demonstrates scripts from my [pdbepisa-utilities sub-repo](https://github.com/fomightez/structurework/tree/master/pdbepisa-utilities) that enable handling data from [PDBePISA](https://www.ebi.ac.uk/pdbe/pisa/) with Jupyter/Python. Importantly, data from that site will summarize interface surface area between **ALL CHAINS** of a structure, even protein and nucleic acid chains, and may be additionally helpful if you are studying a deoxyribonucleic- or ribonucleic-complex.

- See [here](https://github.com/fomightez/structurework#related-binderized-utilities) for a listing of resources in a similar vein yet targeted to macromolecular structure data. In particular, see [cl_demo-binder](https://github.com/fomightez/cl_demo-binder) for the companion set to this one.

- See [here](https://github.com/fomightez/structurework#related-binderized-utilities) for a listing of resources in a similar vein yet targeted to macromolecular structure data. In particular, see [cl_demo-binder](https://github.com/fomightez/cl_demo-binder) for the companion set to this one.