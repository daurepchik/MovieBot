from setuptools import setup

setup(
    name='MovieBot',
    version='1.0',
    packages=['database', 'database.utils', 'site_API', 'site_API.utils', 'telegram_API', 'telegram_API.utils',
              'telegram_API.handlers', 'telegram_API.handlers.custom_handlers',
              'telegram_API.handlers.default_handlers', 'telegram_API.keyboards'],
    url='',
    license='',
    author='Daurepchik',
    author_email='daurenblin5@gmail.com',
    description='Bot to provide information about the rating of films and show their beautiful photos',
    python_requires=">=3.9",
    install_requires=[
        'peewee',
        'pydantic',
        'python-dotenv',
        'python-telegram-bot',
        'requests'
    ]
)
