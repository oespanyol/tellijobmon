#!/usr/bin/env python

__author__    = "Oriol Espanyol"
__copyright__ = "Copyright 2018, EUMETCast Terrestrial Pathfinder-II"
__license__   = "GPL"
__version__   = "1.0.1"
__email__     = "oriol.espanyol@eumetsat.int"
__status__    = "Development"

import re
import pandas as pd


def parse(filepath):
    """
    Parse text at given filepath

    Parameters : TODO

    Returns : TODO

    """

    with open(filepath, 'r') as file:
        text = file.read()
        file.close()


        reg_match = _RegExLib(text)

        channel_content    = reg_match.channel   .group('channel_content'   )
        accounting_content = reg_match.accounting.group('accounting_content')
        scheduling_content = reg_match.scheduling.group('scheduling_content')
        recipients_content = reg_match.recipients.group('recipients_content')
        files_content      = reg_match.files     .group('files_content'     )

        #print(channel_content)
        for line in channel_content.splitlines():
             if line.strip():
                 print(line)

        #print(accounting_content)
        for line in accounting_content.splitlines():
             if line.strip():
                 print(line)

        #print(scheduling_content)
        for line in scheduling_content.splitlines():
             if line.strip():
                 print(line)

        #print(recipients_content)
        for line in recipients_content.splitlines():
             if line.strip():
                 print(line)

        #print(files_content)
        for line in files_content.splitlines():
             if line.strip():
                 print(line)


        #for filel in reg_match.filel:
            #filel_content = filel.group('filel_content')
            #print(filel_content)


class _RegExLib:
    """
     Set up regular expressions - use https://regexper.com to visualise these if required
     The following sections exist in Job files:
             [channel] [accounting] [scheduling] [recipients] [files] [file] [recipient_ip_mappings]
             [system] [unconfirmed_recipients] [complete_recipients] [received_percentage]
    """

    _reg_channel    = re.compile(r'''^\[channel\]       (?P<channel_content>[\s\S]+?)       (?=^\[|\Z|^\#)''', re.MULTILINE | re.VERBOSE)
    _reg_accounting = re.compile(r'''^\[accounting\]    (?P<accounting_content>[\s\S]+?)    (?=^\[|\Z|^\#)''', re.MULTILINE | re.VERBOSE)
    _reg_scheduling = re.compile(r'''^\[scheduling\]    (?P<scheduling_content>[\s\S]+?)    (?=^\[|\Z|^\#)''', re.MULTILINE | re.VERBOSE)
    _reg_recipients = re.compile(r'''^\[recipients\]    (?P<recipients_content>[\s\S]+?)    (?=^\[|\Z|^\#)''', re.MULTILINE | re.VERBOSE)
    _reg_files      = re.compile(r'''^\[files\]         (?P<files_content>[\s\S]+?)         (?=^\[|\Z|^\#)''', re.MULTILINE | re.VERBOSE)
    _reg_filel      = re.compile(r'''^\[file\]          (?P<filel_content>[\s\S]+?)         (?=^\[|\Z|^\#)''', re.MULTILINE | re.VERBOSE)

    def __init__(self, text):
        self.channel    = self._reg_channel    .search(text)
        self.accounting = self._reg_accounting .search(text)
        self.scheduling = self._reg_scheduling .search(text)
        self.recipients = self._reg_recipients .search(text)
        self.files      = self._reg_files      .search(text)
        self.filel      = self._reg_filel      .finditer(text)


if __name__ == '__main__':
    filepath = 'sample.job'
    data = parse(filepath)
