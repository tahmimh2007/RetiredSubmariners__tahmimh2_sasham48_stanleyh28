# Submarine Charts By RetiredSubmariners
Roster: Tahmim Hassan (frontend), Stanley Hoo (backend), Sasha Murokh (backend)


Overview:
Our site will allow users to display their data from csv/json files on charts or to create ML models based on their data. The format is as follows:
- User uploads dataset, either csv or json
- User selects either automatic or manual headings (auto will try to detect headings in csv/json files and use those, manual users will enter name for each field)
- User selects bar graph, line graph, or scatter plot, then an independent variable, then a numerical dependent variable to display a graph
- User selects non-numerical classifying variable, then the variables to train the model to return a machine learning model graph


## Install Guide

**Prerequisites**

Ensure that **Git** is installed on your machine. For help, refer to the following documentation: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

### How to clone/install
1. In terminal, clone the repository to your droplet:

HTTPS METHOD:

```
git clone https://github.com/tahmimh2007/RetiredSubmariners__tahmimh2_sasham48_stanleyh28.git    
```

SSH METHOD (requires the SSH key):

```
git clone git@github.com:tahmimh2007/RetiredSubmariners__tahmimh2_sasham48_stanleyh28.git
```
2. Navigate to project directory:

```
cd PATH/TO/RetiredSubmariners__tahmim2_sasham48_stanleyh28
```
3. Install dependencies

```
pip install -r requirements.txt
```

## Launch Codes

**Prerequisites**

Ensure that **Git**, **Python** and **Ubuntu** are installed on your machine. It is recommended that you use a virtual machine when running this project to avoid any possible conflicts. For help, refer to the following documentation:
   1. Installing Git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
   2. Installing Python: https://www.python.org/downloads/
   3. Installing Ubuntu onto your droplet: https://www.digitalocean.com/community/tutorials/how-to-set-up-an-ubuntu-server-on-a-digitalocean-droplet

### How to run


1. Create Python virtual environment:

```
python3 -m PATH/TO/venv_name
```

2. Activate virtual environment

   - Linux: `. PATH/TO/venv_name/bin/activate`
   - Windows (PowerShell): `. .\PATH\TO\venv_name\Scripts\activate`
   - Windows (Command Prompt): `>PATH\TO\venv_name\Scripts\activate`
   - macOS: `source PATH/TO/venv_name/bin/activate`

   *Notes*

   - If successful, command line will display name of virtual environment: `(venv_name) `

   - Type `deactivate` in the terminal to close a virtual environment

3. Navigate to project app directory

```
cd PATH/TO/RetiredSubmariners__tahmim2_sasham48_stanleyh28/app/
```

4. Run App

```
 python3 __init__.py
```
5. Open the link that appears in the terminal to be brought to the website
    - You can visit the link via several methods:
        - Control + Clicking on the link
        - Typing/Pasting http://127.0.0.1:5000 in any browser
    - To close the app, press control + C when in the terminal

```    
* Running on http://127.0.0.1:5000
```
Accurate as of (last update): 
4-2-2025
