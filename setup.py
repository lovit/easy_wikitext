import easy_wikitext
from setuptools import setup, find_packages


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="easy_wikitext",
    version=easy_wikitext.__version__,
    author=easy_wikitext.__author__,
    author_email='soy.lovit@gmail.com',
    url='https://github.com/lovit/easy_wikitext',
    description='Wikitext handler',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords = ['wikitext'],
    packages=find_packages()
)
