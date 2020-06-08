from setuptools import setup, find_packages

setup(
    name='mock_cameras',
    version='0.0.1',
    description='Publishes images on IS architecture based on video files',
    url='http://github.com/luizcarloscf/mock-cameras',
    author='luizcarloscf',
    license='MIT',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': ['mock-cameras=mock_cameras.service:main',],
    },
    zip_safe=False,
    install_requires=[
        'numpy==1.18.1',
        'is-wire==1.2.0',
        'is-msgs==1.1.10',
    ],
)