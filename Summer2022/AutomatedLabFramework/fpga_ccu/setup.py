import setuptools as st

st.setup(
    name='fpga_ccu',
    version='0.0.0',
    url='https://github.com/kwshi/lynnlab-summer2018',
    author='Kye W. Shi',
    author_email='kwshi@hmc.edu',
    packages=st.find_packages(),
    entry_points={
        'console_scripts': [
            'fpga-ccu = fpga_ccu.__main__:main',
        ],
    },

)
