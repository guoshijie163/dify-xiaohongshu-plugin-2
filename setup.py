from setuptools import setup, find_packages

setup(
    name="dify-xiaohongshu-plugin",
    version="1.0.0",
    description="小红书笔记获取插件 for Dify",
    author="您的用户名",
    author_email="您的邮箱",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    python_requires=">=3.6",
) 