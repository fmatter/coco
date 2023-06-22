from setuptools import find_packages, setup

setup(
    name="coco",
    version="0.0",
    description="coco",
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author="",
    author_email="",
    url="",
    keywords="web pyramid pylons",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "clld",
        "clld_document_plugin",
        "clld_markdown_plugin",
        "clld_morphology_plugin",
        "clld_corpus_plugin",
        "tqdm",
        "waitress"
    ],
    extras_require={
        "dev": ["flake8", "waitress"],
        "test": [
            "mock",
            "pytest>=5.4",
            "pytest-clld",
            "pytest-mock",
            "pytest-cov",
            "coverage>=4.2",
            "selenium",
            "zope.component>=3.11.0",
        ],
    },
    test_suite="coco",
    entry_points="""\
    [paste.app_factory]
    main = coco:main
""",
)
