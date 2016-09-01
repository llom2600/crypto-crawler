## crypto-crawler
crypto currency data parser thing

##yo! set up / install:

set up virtual environment (these are unix/linux instructions, but they should be similar)
  1. pip install virtualenv
  2. virtualenv -p /path/to/python/interpreter/ venv-crawler
  3. source /venv-crawler/bin/activate (i think in a windows environment, you just put the path, e.g. /venv-crawler/bin/activate)
  
then go to cloned project directory and run:
  4. pip install -r requirements.txt (in / of project)
  
before working each time, you gotta run (3) to ensure you're working in the proper virtual environment. i encapsulated this in a 
venv because i have so much shit installed in my normal python environment that it gets cluttered and confusing. sorry about that.
we can write some shell scripts if it gets annoying. i made a shell scripts folder for those. 
  
