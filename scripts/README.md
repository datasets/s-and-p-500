These scripts run with [github-actions](https://github.com/features/actions)

# Run the scripts yourself

## Install the dependencies
The scripts work with some python and shell scripts glued together with a Makefile.

Install the required python libraries :

    cd scripts
    pip install -r requirements.txt

You can also work on a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) .

## Make the package and publish it
The purpose of the project is to compute the datapackage, to test it and to publish it to a git repository :

	make

## Only make the package locally and test it
If you work on the code, you might want to skip to publish step :

	make valid.txt