#!/usr/bin/env python

import os
import re
from models import Job, File, Recipient, init

'''
 Environment prerequisites
 SQLAlchemy       $> pip install --user SQLAlchemy==1.2.12
 Datatables       $> pip install --user datatables
 Jinja            $> pip install --user Jinja2
 Flask            $> pip install --user Flask
'''

__author__    = "Oriol Espanyol"
__copyright__ = "Copyright 2018, EUMETCast Terrestrial Pathfinder-II"
__license__   = "GPL"
__version__   = "1.0.1"
__email__     = "oriol.espanyol@eumetsat.int"
__status__    = "Development"


def get_files_in_dir(dirpath, ending):

    files = []
    for filename in os.listdir(dirpath):
        if filename.endswith(ending):
            files.append(os.path.join(dirpath, filename))
            continue
        else:
            continue

    return files


def parse_job(pfilepath):
    """
    Parse text at given filepath

    Parameters : TODO

    Returns : TODO

    """
    with open(pfilepath, 'r') as jfile:
        text = jfile.read()
        jfile.close()

        reg_match = _RegExLib(text)

        channel_content     = ['channel',     reg_match.channel     .group('channel'    )]
        accounting_content  = ['accounting',  reg_match.accounting  .group('accounting' )]
        scheduling_content  = ['scheduling',  reg_match.scheduling  .group('scheduling' )]
        recipients_content  = ['recipients',  reg_match.recipients  .group('recipients' )]
        files_content       = ['files',       reg_match.files       .group('files'      )]
        system_content      = ['system',      reg_match.system      .group('system'     )]
        ip_content          = ['ip',          reg_match.ip          .group('ip'         )]
        unconfirmed_content = ['unconfirmed', reg_match.unconfirmed .group('unconfirmed')]
        complete_content    = ['complete',    reg_match.complete    .group('complete'   )]
        received_content    = ['received',    reg_match.received    .group('received'   )]

        # Put all contents together in one list
        job_contents = [channel_content, accounting_content, scheduling_content,
                        recipients_content, files_content, system_content]

        # Instantiate a the job dictionary to keep all the keys and values
        job_dict = {}
        # Iterate through the list of contents to prepend the name of the section
        for content in job_contents:
            prefix = content[0]
            lines = content[1]
            for line in lines.splitlines():
                if line.strip():
                    # Prepend the name of the section
                    section_line = prefix + '_' + line
                    # Split line on "=" separator to generate the key value pair
                    job_kvp = section_line.split("=", 2)
                    job_dict[job_kvp[0]] = job_kvp[1]

        session = init()

        job = Job(job_dict)

        session.add(job)

#        myjob = session.query(Job).filter_by(channel_name='T01-EPS-A-11').first()
#        print(myjob)

        # Iterate through the list of files, parse the information and persist it into table
        for filel in reg_match.filel:
            filel_lines = filel.group('filel')

            # Instantiate a the file dictionary to keep all the keys and values
            # and add the job id as link to jobs table
            filel_dict = {'files_acknowledge_id': job.files_acknowledge_id}
            # Iterate through the list of contents to prepend the name of the section
            for line in filel_lines.splitlines():
                if line.strip():
                    # Split line on "=" separator to generate the key value pair
                    filel_kvp = line.split("=", 2)
                    filel_dict[filel_kvp[0]] = filel_kvp[1]
                    # TODO: Consider handling duplicates, like in [files] file=

            afile = File(filel_dict)
            session.add(afile)

#        myfile = session.query(File).filter_by(file_id='5ba88d2e0012de5a').first()
#        print(myfile)

        # Put all contents together in one list
        recipient_contents = [ip_content, unconfirmed_content, complete_content, received_content]

        # Instantiate a recipient dictionary to keep all the keys and values
        recipient_dict = {}
        # Iterate through the list of contents to prepend the name of the section
        for content in recipient_contents:
            prefix = content[0]
            lines = content[1]
            for line in lines.splitlines():
                if line.strip():
                    recipient_kvp = line.split("=", 2)
                    # Assign key and value depending on the type of content
                    if recipient_kvp[0] == 'name':
                        key = recipient_kvp[1]
                        value = 'True'
                    else:
                        key = recipient_kvp[0]
                        value = recipient_kvp[1]

                    # Create new entry or if it already exists, get instance and fill details of existing entry
                    if key in recipient_dict:
                        rec = recipient_dict[key]
                        rec[prefix] = value
                        recipient_dict[key] = rec
                    else:
                        rec = {prefix: value,
                               'name': key,
                               'files_acknowledge_id': job.files_acknowledge_id}
                        recipient_dict[key] = rec

        for key, values in recipient_dict.items():
            arecipient = Recipient(values)
            session.add(arecipient)

#        myrecipient = session.query(Recipient).order_by(desc(Recipient.id)).first()
#        print(myrecipient)

        session.commit()
        session.close()


class _RegExLib:
    """
     Set up regular expressions - use https://regexper.com to visualise these if required
     The following sections exist in Job files:
             [channel] [accounting] [scheduling] [recipients] [files] [file] [recipient_ip_mappings]
             [system] [unconfirmed_recipients] [complete_recipients] [received_percentage]
    """

    _reg_channel = re    .compile(r'''^\[channel\]                (?P<channel>[\s\S]+?)     (?=^\[|\Z|^\#)''', re.MULTILINE | re.VERBOSE)
    _reg_accounting = re .compile(r'''^\[accounting\]             (?P<accounting>[\s\S]+?)  (?=^\[|\Z|^\#)''', re.MULTILINE | re.VERBOSE)
    _reg_scheduling = re .compile(r'''^\[scheduling\]             (?P<scheduling>[\s\S]+?)  (?=^\[|\Z|^\#)''', re.MULTILINE | re.VERBOSE)
    _reg_recipients = re .compile(r'''^\[recipients\]             (?P<recipients>[\s\S]+?)  (?=^\[|\Z|^\#)''', re.MULTILINE | re.VERBOSE)
    _reg_files = re      .compile(r'''^\[files\]                  (?P<files>[\s\S]+?)       (?=^\[|\Z|^\#)''', re.MULTILINE | re.VERBOSE)
    _reg_filel = re      .compile(r'''^\[file\]                   (?P<filel>[\s\S]+?)       (?=^\[|\Z|^\#)''', re.MULTILINE | re.VERBOSE)
    _reg_system = re     .compile(r'''^\[system\]                 (?P<system>[\s\S]+?)      (?=^\[|\Z|^\#)''', re.MULTILINE | re.VERBOSE)
    _reg_ip = re         .compile(r'''^\[recipient_ip_mappings\]  (?P<ip>[\s\S]+?)          (?=^\[|\Z|^\#)''', re.MULTILINE | re.VERBOSE)
    _reg_unconfirmed = re.compile(r'''^\[unconfirmed_recipients\] (?P<unconfirmed>[\s\S]+?) (?=^\[|\Z|^\#)''', re.MULTILINE | re.VERBOSE)
    _reg_complete = re   .compile(r'''^\[complete_recipients\]    (?P<complete>[\s\S]+?)    (?=^\[|\Z|^\#)''', re.MULTILINE | re.VERBOSE)
    _reg_received = re   .compile(r'''^\[received_percentage\]    (?P<received>[\s\S]+?)    (?=^\[|\Z|^\#)''', re.MULTILINE | re.VERBOSE)

    def __init__(self, text):
        self.    channel = self._reg_channel    .search(text)
        self. accounting = self._reg_accounting .search(text)
        self. scheduling = self._reg_scheduling .search(text)
        self. recipients = self._reg_recipients .search(text)
        self.      files = self._reg_files      .search(text)
        self.      filel = self._reg_filel      .finditer(text)
        self.     system = self._reg_system     .search(text)
        self.         ip = self._reg_ip         .search(text)
        self.unconfirmed = self._reg_unconfirmed.search(text)
        self.   complete = self._reg_complete   .search(text)
        self.   received = self._reg_received   .search(text)


if __name__ == '__main__':

    jobs_path = '/home/espanyol/workspace/tellijobsparser/jobs'
    jobs_sufix = '.job'
    job_paths = get_files_in_dir(jobs_path, jobs_sufix)

    for job_path in job_paths:
        parse_job(job_path)
