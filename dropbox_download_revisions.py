#!/usr/bin/env python
# Copyright 2009-2018 Ram Rachum.
# This program is distributed under the MIT license.

import os
import itertools
import concurrent.futures
import json
import pathlib

import click
import dropbox


home_path = pathlib.Path(os.environ['HOME'])
config_path = home_path / '.dropbox_download_revisions'


def get_cached_api_key():
    try:
        data = json.loads(config_path.read_text())
    except FileNotFoundError:
        return None
    else:
        return data['api_key']


def save_api_key_to_cache(api_key):
    data = config_path.write_text(json.dumps({'api_key': api_key}))


@click.command()
@click.argument('path', type=click.Path(exists=True, dir_okay=False,
                                        resolve_path=True))
@click.option('-n', '--n-revisions', default=100)
@click.option('--api-key', type=str, prompt='Dropbox API key',
              default=get_cached_api_key)
@click.option('--save-api-key', is_flag=True)
@click.option('--dropbox-root', prompt=True, 
              default=lambda: home_path / 'Dropbox',
              envvar='DROPBOX')
def dropbox_download_revisions(path, n_revisions, api_key, save_api_key,
                               dropbox_root):
    '''
    Download up to 100 revisions of a Dropbox file to a folder.
    '''
    path = pathlib.Path(path)
    revisions_folder = pathlib.Path(f'{path}.revisions')
    if revisions_folder.exists():
        raise click.ClickException(f'{revisions_folder} already exists')
    dropbox_root = pathlib.Path(dropbox_root)
    relative_path = path.relative_to(dropbox_root)
    
    path_string = ''.join(f'/{part}' for part in relative_path.parts)
    d = dropbox.Dropbox(api_key)
    revisions_folder.mkdir()
    print('Getting list of revisions...')
    entries = d.files_list_revisions(path_string, limit=n_revisions).entries
    if save_api_key:
        print('Saving API key to cache...')
        save_api_key_to_cache(api_key)
    
    def shush(entry):
        file_name = (
            f'{entry.server_modified.isoformat().replace("T", "-").replace(":", "-")}'
            f'---{entry.rev}.{path.suffix}'
        )
        d.files_download_to_file(str(revisions_folder / file_name),
                                 path_string, entry.rev)
        
    with concurrent.futures.ThreadPoolExecutor(20) as executor:
        print('Downloading revisions...')
        list(executor.map(shush, entries))
    print(f'Downloaded {len(entries)} revisions to {revisions_folder}')
        

if __name__ == '__main__':
    dropbox_download_revisions()