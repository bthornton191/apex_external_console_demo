# MSC Apex Scripting - External Console Demo

One exciting feature of MSC Apex is the powerful python API.  I wanted learn how to launch Apex from an external console.  There are several reasons for using an external console.  The two big ones for mre

1. You can use integrated development environmnents (IDE) like vscode or pycharm and make use of powerful tools like autocompletion, linting, and debugging.
2. You can integrate your Apex scripts into a larger code base that runs outside of the Apex environment

The Apex documentation lays out a method for using 3rd party modules/packages in Apex scripts.  There were several reasons that I was not satisfied with this method (not the lease of which is that I couldn't get it to work with pandas).  After some trial and error I came up with the method presented here using a virtual environment.  My hope is that the code in this repo can help you get a jump start on apex scripting in external consoles.

## Requirements
You must have MSC Apex installed.  I currently have Iberian Lynx, but the script will *probably* work on any version.

## Usage

### Step 1: Create A Virtual Environment
Create a virutal environment from the python installation shipped with apex by running the following command in the terminal of your IDE:

`"<path-to-apex-python>\python.exe" -m venv env --system-site-packages`

For reference, my apex python path is *C:\Program Files\MSC.Software\MSC Apex\2019-652722\python3\\*

If your IDE doesn't automatically activate the new env environment, you can do so with the command:

`env\Scripts\**activate`**

### Step 2: Install 3rd Party Modules/Packages
This you can install all the 3rd party dependencies required by this script to the env environment with the following command:

`pip install -r requirements.txt`

> **TIP**: You can create your own requirements.txt document using `pip freeze>requirements.txt`

### Step 3: Run the script
Run the main.py file via `python main.py` or through your IDE.

## Contributing
Please don't hesitate to message/email me if you have any suggestions that might improve this repo.