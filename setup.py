from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

## edit below variables as per your requirements -
REPO_NAME = "Big-Mart-Sales-Prediction-MLFlow"
AUTHOR_USER_NAME = "siddmodi"
SRC_REPO = "src"
LIST_OF_REQUIREMENTS = []


setup(
    name=SRC_REPO,
    version="0.0.1",
    author='Siddharth',
    description="Big mart sales prediction",

    long_description='''
                        Fill the following details and get the sales of your described items
                        on your described outlet in Rs :

                        Item_Weight,
                        Item_Fat_Content,
                        Item_Visibility,	
                        Item_Type,
                        Item_MRP,
                        Outlet_Size	Outlet_Location_Type,	
                    ''',

    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    author_email="siddharthmodi39101@gmail.com",
    packages=[SRC_REPO],
    license="",
    python_requires=">=3.6",
    install_requires=LIST_OF_REQUIREMENTS
    )
