from setuptools import find_packages, setup

setup(
    name='mcp',
    packages=find_packages(),
    version='0.1.0',
    description='Model Context Portal - A comprehensive platform for managing model contexts',
    author='Your Name',
    license='MIT',
    install_requires=[
        'numpy>=1.21.0',
        'pandas>=1.3.0',
        'scikit-learn>=0.24.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
