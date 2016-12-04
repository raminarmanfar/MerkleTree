# Readme

# Good practices

 - before adding latex files to the git, run latexmk -C to clean the repo (by this you will not add log and other latex generated temporary files)
 - add the pdf to a separate place because when I compile locally the tex file the generated pdf will replace git version, therefore when I pull your version there is always a conflict. For now we could use ./reports directly for different versions of pdf.

# ToDO

 - [ ] Ramin, as you've used tex -> PDF, upload the Tex file in a separate folder, it could be useful to merge and track changes [Prabha]
 
# Tests

 - [ ] Runs smoothly on Ubuntu + Python3 [Prabha]
  
# Issues

- [ ] issues with windows + msys2 + python3
	```
	$ python mainModule.py
	*****************************************************
	>>> Merkle Tree (Ver 1.1)
	>>> By Ramin Armanfar
	>>> Date: Oct 19, 2016
	Email: ramin.armanfar@gmail.com
	*****************************************************
	*************** Merkle-Tree Main Menu ***************
	1) Create Merkle-Tree
	2) Add new data block(s)
	3) Show a path
	4) Show all paths
	5) Proof of a path
	6) About Us
	0) Exit
	Traceback (most recent call last):
File "mainModule.py", line 276, in <module>
    main(sys.argv)
  File "mainModule.py", line 138, in main
    menuItem = raw_input(bcolors.OKGREEN + 'Choose an item (0 - 6): ' + bcolors.ENDC)
NameError: name 'raw_input' is not defined
    ```
