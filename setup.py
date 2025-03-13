from setuptools import setup, find_packages

setup(
    name='mcp',
    version='0.1.0',
    description='Model Context Protocol Implementation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/mcp',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pydantic>=2.0.0',
        'fastapi>=0.68.0',
        'uvicorn>=0.15.0',
        'requests>=2.26.0',
        'python-dotenv>=0.19.0',
        'marshmallow>=3.15.0',
    ],
    extras_require={
        'dev': [
            'pytest>=6.2.0',
            'pytest-asyncio>=0.15.0',
        ],
        'ml': [
            'scikit-learn>=0.24.0',
            'torch>=1.9.0',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    keywords='model context protocol ai machine-learning',
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'mcp-api=mcp.api.context_api:run_server',
        ],
    }
)
