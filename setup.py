import setuptools

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

with open('requirements.txt', "r", encoding="utf8") as f:
    required = f.read().splitlines()

setuptools.setup(
    name="collage",
    version="0.0.1",
    author="Alexandra Zhuravskaya, Satbek Turganbayev, Timur Kamalbekov",
    author_email="a.v.zhuravskaya@gmail.com, set.turg@mail.ru, onymoth@gmail.com",
    description="Simple Collage Creating application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/1alexandra/collage",
    packages=setuptools.find_packages(
        exclude=["*.test", "*.test.*", "test.*", "test"]
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=required,
    python_requires='>=3.7',
)
