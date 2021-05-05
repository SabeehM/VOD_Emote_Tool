from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 3 - Alpha',
  'Intended Audience :: Other Audience',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name="VOD-Emote-Tool",
  version = '0.0.1',
  description="A simple tool to gather emote analytics from any twitch VOD.",
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Sabeeh Malik',
  author_email='sabeeh.malik@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='twitch', 
  packages=find_packages(),
  install_requires=['matplotlib','pyparsing','python-dateutil','twitch-python'] 
)