from setuptools import setup, find_packages
from typing import List

HYPEN = '-e .'

def get_requirements(file_path: str) -> List[str]:
    """
    This function reads a requirements file and returns a list of packages.
    """
    with open(file_path,) as file_obj:

        requirements = file_obj.readlines()
        requirements = [req.replace("\n", "") for req in requirements]
        if HYPEN in requirements:
            requirements.remove(HYPEN)
    return requirements
                                    

    




setup(
    name='mlendtoend',
    version='0.1',
    author='Sahil Maniyar',
    author_email='sahilmaniyar1602@gmail.com',
    packages=find_packages(),
    install_requires= get_requirements('requirements.txt')


)