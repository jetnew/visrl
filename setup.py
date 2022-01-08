from setuptools import setup

setup(
    name='visrl',
    version='0.1.0',
    description="A simple wrapper to analyse and visualise reinforcement learning agents' behaviour in the environment.",
    url='https://github.com/jetnew/rl-debugger',
    author='Jet New',
    author_email='notesjet@gmail.com',
    license='MIT',
    packages=['visrl'],
    install_requires=['pysimplegui',
                      'numpy',
                      'opencv-python',
                      'imageio',
                      'gym',
                      'stable-baselines3'
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