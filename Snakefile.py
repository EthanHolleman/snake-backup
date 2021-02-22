import socket
from pathlib import Path
import os

def collect_local_sources():
    '''Collect all local directories that should be copied to remote machines.
    These are specified in the config.yaml file.

    Returns:
        list: List of directories on machine snakemake is running.
    '''

    return config['local_machines'][socket.gethostname()]['local_targets']

def intefer_rclone_remotes(targets):
    '''Using the local sources and the rclone remote targets specified in
    the config.yaml file return two lists containing local paths and the
    remote directory they should be copied to respectively.

    Args:
        targets ([type]): [description]
    '''
    all_targets = []
    all_remotes = []


#LOCAL_DIRS = config['local_machines'][socket.gethostname()]['local_targets']
#dir_dict = dict(zip(range(1, len(LOCAL_DIRS)+1), LOCAL_DIRS))
#hashes = dir_dict.keys()

rule collect_local_dirs:
    input:
       expand('temp/{hash_name}.confirm', hash_name=hashes)

# rule to download each individual file specified in sample_links
rule rclone_copy:
    output: 'temp/{hash_name}.confirm'
    params:
        # dynamically generate the download link directly from the dictionary
        download_path = LOCAL_DIRS
    shell: """
        {rclone.exe} copy --update --transfers {rclone.transfers} \
        --checkers {rclone.checkers} --retries {rclone.retries} \
        --low-level-retries {rclone.low_level_retries} \
        "{local_target}" "{remote_destination}"
        touch {output}
        """

rule rsync:
    pass
# use this rule for downloads via rsync
