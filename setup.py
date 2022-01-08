from setuptools import setup

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='visrl',
    version='0.1.5',
    description="A simple wrapper to analyse and visualise reinforcement learning agents' behaviour in the environment.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jetnew/visrl',
    author='Jet New',
    author_email='notesjet@gmail.com',
    license='MIT',
    packages=['visrl'],
    install_requires=['pysimplegui',
                      'numpy',
                      'opencv-python',
                      'imageio',
                      'gym',
                      'stable-baselines3',
                      'pyglet',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
)