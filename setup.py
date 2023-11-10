from setuptools import setup, find_packages

setup(
    name="RanBALL",
    version="1.0.0",
    description="Identifying B-cell acute lymphoblastic leukemia subtypes based on an ensemble random projection model",
    url="https://github.com/wan-mlab/RanBALL",
    author="Lusheng Li, Hanyu Xiao, Shibiao Wan",
    author_email="lli@unmc.edu",
    license="MIT",
    packages=find_packages(where='./RanBALL'),
    package_dir={
        '': 'RanBALL'
    },
    include_package_data=True,
    install_requires=[
        "scikit-learn==1.2.1",
        "scipy==1.7.3"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6"
)
