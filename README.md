##### Steps to setup a reproducible and dockerized python environment in Windows


1. Use Docker Desktop 
    a. Forces you to work with WSL.
2. Use Docker Development Environment.
    a. Currently this is setup using a git repo.
3. The default docker development environment had python 3.9 installed.
    a. But no pip.
    b. Got distutil error while trying to install pip.
    c. Solution: Do apt-get update && upgrade first.
    d. Install pip 
4. Install Poetry as the dependency manager.
    a. Set local folder to contain the environment.
    b. Use this video as reference: https://www.youtube.com/watch?v=0f3moPe_bhk
    c. You can use poetry to package and publish apps in pypi too.
=======
1. Use github codespaces.
2. The compose-dev.yaml file will automatically setup the environment with the necessary dependencies.
3. Follow the notebooks for starting out with langchain.
4. Follow https://python.langchain.com/en/latest/ecosystem/google_search.html and https://python.langchain.com/en/latest/modules/agents/tools/examples/google_search.html for setting up google api key, enabling custom search api and creating Google custom search engine (CSE_ID) ID.

