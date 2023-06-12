from setuptools import setup

setup(
    name='Tracker',
    version='0.1',
    packages=['firebase_notification','keyboard_model','main','mouse_model','tracker','user_list'],
    entry_points={
        'console_scripts': [
            'main=main:run'
        ]
    },
    url='',
    license='',
    author='Ziggy',
    author_email='ziggyliu06@gmail.com',
    description=''
)
