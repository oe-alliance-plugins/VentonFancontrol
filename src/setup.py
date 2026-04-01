from setuptools import setup
import setup_translate

pkg = 'SystemPlugins.VentonFancontrol'
setup(name='enigma2-plugin-systemplugins-fancontrol',
       version='3.0',
       description='Fancontrol Settings inStandby Mode',
       package_dir={pkg: 'VentonFancontrol'},
       packages=[pkg],
       package_data={pkg: ['images/*.png', '*.png', '*.xml', 'locale/*/LC_MESSAGES/*.mo']},
       cmdclass=setup_translate.cmdclass,  # for translation
      )
