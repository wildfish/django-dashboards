from setuptools import find_packages, setup


VERSION = "0.0.1"

setup(
    name="django-datorum",
    version=VERSION,
    author="Wildfish",
    author_email="developers@wildfish.com",
    description="Tools for building data dashboards and pipelines with Django",
    license="BSD",
    keywords="django dashboard pipeline htmx graphql",
    url="http://wildfish.com",
    long_description="Tools for building data dashboards and pipelines with Django",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
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
        "django>=3.2",
        "django-cors-headers",
        "django-extensions",
        "pydantic",
        "strawberry-graphql[debug-server]",
    ],
    zip_safe=True,
    packages=find_packages(exclude=("docs", "tests*")),
    include_package_data=True,
)
