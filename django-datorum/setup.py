from setuptools import find_packages, setup


VERSION = "0.0.1"

setup(
    name="django-datorum",
    version=VERSION,
    author="Wildfish",
    author_email="developers@wildfish.com",
    description="...",
    license="BSD",
    keywords="django dashboard datorum",
    url="http://wildfish.com",
    long_description="todo",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
    ],
    install_requires=[
        "django-cors-headers",
        "django_htmx",
        "strawberry-graphql[debug-server]",
    ],
    zip_safe=True,
    packages=find_packages(exclude=("docs", "tests*")),
    include_package_data=True,
)
