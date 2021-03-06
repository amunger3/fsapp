import os
import json
import configparser


def read_from_package_json(write=False):

    package_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'package.json'))

    with open(package_file) as f:
        package = json.load(f)

    package_info = dict(
        name=package['name'].replace(' ', '_').replace('-', '_'),
        version=package['version'],
        author=package['author']
    )

    if write:
        package_info_file = os.path.abspath(os.path.join(
            os.path.dirname(__file__), os.path.join(
                'version-info.json'
            )
        ))

        with open(package_info_file, 'w') as f:
            f.write(json.dumps(package_info, indent=4))

    return package_info


def read_from_setup_cfg():

    config = configparser.ConfigParser()
    config.read('setup.cfg')

    config_info = dict(
        name=config['metadata']['name'],
        version=config['metadata']['version'],
        author=dict(
            name=config['metadata']['author'],
            email=config['metadata']['author-email'],
            url=config['metadata']['author-url']
        )
    )

    return config_info


def ver_up(level='patch'):

    pkg = read_from_package_json(write=False)
    cfg = read_from_setup_cfg()
    if pkg['version'] == cfg['version']:
        major, minor, patch = pkg['version'].split('.')
        ver_dict = {
            'major': int(major),
            'minor': int(minor),
            'patch': int(patch)
        }
        ver_dict[level] += 1
        upd_vstr = '.'.join([str(val) for val in ver_dict.values()])
        print(upd_vstr)

        return


if __name__ == '__main__':
    package_info = read_from_package_json(write=True)
    config_info = read_from_setup_cfg()
    if package_info == config_info:
        print("Package version configurations synced!")
        print("Current version: {0}".format(package_info['version']))
    else:
        print("Package version configurations are inconsistent.")
        print("package.json names version: {0}".format(package_info['version']))
        print("setup.cfg names version: {0}".format(config_info['version']))