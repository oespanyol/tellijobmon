#!/usr/bin/env python

import re
import datetime
# SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


__author__    = "Oriol Espanyol"
__copyright__ = "Copyright 2018, EUMETCast Terrestrial Pathfinder-II"
__license__   = "GPL"
__version__   = "1.0.1"
__email__     = "oriol.espanyol@eumetsat.int"
__status__    = "Development"

Base = declarative_base()


def parse(pfilepath):
    """
    Parse text at given filepath

    Parameters : TODO

    Returns : TODO

    """

    with open(pfilepath, 'r') as pfile:
        text = pfile.read()
        pfile.close()

        reg_match = _RegExLib(text)

        # TODO: Can be streamlined to match for the names of the sections and iterate
        #       Code is compacter and more extandable but, it might be less readable
        channel_content    = ['channel',    reg_match.channel   .group('channel_content'   )]
        accounting_content = ['accounting', reg_match.accounting.group('accounting_content')]
        scheduling_content = ['scheduling', reg_match.scheduling.group('scheduling_content')]
        recipients_content = ['recipients', reg_match.recipients.group('recipients_content')]
        files_content      = ['files',      reg_match.files     .group('files_content'     )]
        system_content     = ['system',     reg_match.system    .group('system_content'    )]

        # Put all contents together in one list
        job_contents = [channel_content, accounting_content, scheduling_content,
                        recipients_content, files_content, system_content]

        # Instantiate a the job dictionary to keep all the keys and values
        job_dict = {}
        # Iterate through the list of contents to prepend the name of the section
        for content in job_contents:
            prefix = content[0]
            lines  = content[1]
            for line in lines.splitlines():
                if line.strip():
                    # Prepend the name of the section
                    section_line = prefix + '_' + line
                    # Split line on "=" separator to generate the key value pair
                    print(section_line)
                    job_kvp = section_line.split("=", 2)
                    job_dict[job_kvp[0]] = job_kvp[1]

        print(job_dict)
        session = _InitPersist().session

        job = Job(job_dict)

        session.add(job)
        my_job = session.query(Job).filter_by(channel_name='T01-EPS-A-11').first()
        print(my_job)

#        for filel in reg_match.filel:
#            filel_content = filel.group('filel_content')
#            print(filel_content)
    return text


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
    _reg_system     = re.compile(r'''^\[system\]        (?P<system_content>[\s\S]+?)        (?=^\[|\Z|^\#)''', re.MULTILINE | re.VERBOSE)

    def __init__(self, text):
        self.channel    = self._reg_channel    .search(text)
        self.accounting = self._reg_accounting .search(text)
        self.scheduling = self._reg_scheduling .search(text)
        self.recipients = self._reg_recipients .search(text)
        self.files      = self._reg_files      .search(text)
        self.filel      = self._reg_filel      .finditer(text)
        self.system     = self._reg_system     .search(text)


class Job(Base):
    __tablename__ = 'jobs'
    files_acknowledge_id = Column(String, primary_key=True)
    files_source_directory                      = Column(String  )
    files_target_directory                      = Column(String  )
    files_state_files_directory                 = Column(String  )
    files_integrity_check                       = Column(Boolean )
    channel_name                                = Column(String  )
    accounting_customer                         = Column(String  )
    scheduling_allow_recipient_modifications    = Column(String  )
    scheduling_start_time                       = Column(Boolean )
    scheduling_priority                         = Column(Integer )
    scheduling_retransmission_interval          = Column(Integer )
    scheduling_start_time_window                = Column(Integer )
    scheduling_nr_of_transmissions              = Column(Integer )
    scheduling_status_keep_time                 = Column(Integer )
    scheduling_expire_time                      = Column(DateTime)
    scheduling_retransmission_type              = Column(String  )
    scheduling_acknowledgement_interval         = Column(Integer )
    scheduling_loss_rate_threshold              = Column(Integer )
    scheduling_request_acknowledgements         = Column(Integer )
    scheduling_atomicity                        = Column(Integer )
    scheduling_client_file_database_expire_time = Column(Integer )
    recipients_file                             = Column(String  )
    system_is_complete                          = Column(Boolean )
    system_nr_of_transmitted_bytes              = Column(Integer )
    system_completion_percentage                = Column(Float   )
    system_next_start_time                      = Column(DateTime)
    system_transmissions_done                   = Column(Integer )
    system_packet_naks_allowed                  = Column(Boolean )

    def __init__(self, jobdict):
        self.files_acknowledge_id = jobdict['files_acknowledge_id']
        self.files_source_directory = jobdict['files_source_directory']
        self.files_target_directory = jobdict['files_target_directory']
        self.files_state_files_directory = jobdict['files_state_files_directory']
        self.files_integrity_check = str2bool(jobdict['files_integrity_check'])
        self.channel_name = jobdict['channel_name']
        self.accounting_customer = jobdict['accounting_customer']
        self.scheduling_allow_recipient_modifications = str2bool(jobdict['scheduling_allow_recipient_modifications'])
        self.scheduling_start_time = datetime.datetime.strptime(jobdict['scheduling_start_time'], "%Y-%m-%d %H:%M:%S")
        self.scheduling_priority = int(jobdict['scheduling_priority'])
        self.scheduling_retransmission_interval = int(jobdict['scheduling_retransmission_interval'])
        self.scheduling_start_time_window = int(jobdict['scheduling_start_time_window'])
        self.scheduling_nr_of_transmissions = int(jobdict['scheduling_nr_of_transmissions'])
        self.scheduling_status_keep_time = int(jobdict['scheduling_status_keep_time'])
        self.scheduling_expire_time = datetime.datetime.strptime(jobdict['scheduling_expire_time'], "%Y-%m-%d %H:%M:%S")
        self.scheduling_retransmission_type = jobdict['scheduling_retransmission_type']
        self.scheduling_acknowledgement_interval = int(jobdict['scheduling_acknowledgement_interval'])
        self.scheduling_loss_rate_threshold = int(jobdict['scheduling_loss_rate_threshold'])
        self.scheduling_request_acknowledgements = int(jobdict['scheduling_request_acknowledgements'])
        self.scheduling_atomicity = int(jobdict['scheduling_atomicity'])
        self.scheduling_client_file_database_expire_time = int(jobdict['scheduling_client_file_database_expire_time'])
        self.recipients_file = jobdict['recipients_file']
        self.system_is_complete = str2bool(jobdict['system_is_complete'])
        self.system_nr_of_transmitted_bytes = int(jobdict['system_nr_of_transmitted_bytes'])
        self.system_completion_percentage = float(jobdict['system_completion_percentage'])
        self.system_next_start_time = datetime.datetime.strptime(jobdict['system_next_start_time'], "%Y-%m-%d %H:%M:%S")
        self.system_transmissions_done = int(jobdict['system_transmissions_done'])
        self.system_packet_naks_allowed = str2bool(jobdict['system_packet_naks_allowed'])

    def __repr__(self):
        return "<Job(" \
               "files_acknowledge_id = '%s'," \
               "files_source_directory = '%s'," \
               "files_target_directory = '%s'," \
               "files_state_files_directory = '%s'," \
               "files_integrity_check = '%s'," \
               "channel_name = '%s', " \
               "accounting_customer = '%s'," \
               "scheduling_allow_recipient_modifications = '%s', "\
               "scheduling_start_time = '%s'," \
               "scheduling_priority = '%u', "\
               "scheduling_retransmission_interval = '%u', "\
               "scheduling_start_time_window = '%u', "\
               "scheduling_nr_of_transmissions = '%u', "\
               "scheduling_status_keep_time = '%u', "\
               "scheduling_expire_time = '%s'," \
               "scheduling_retransmission_type = '%s', " \
               "scheduling_acknowledgement_interval = '%u', "\
               "scheduling_loss_rate_threshold = '%u', "\
               "scheduling_request_acknowledgements = '%u', "\
               "scheduling_atomicity = '%u', "\
               "scheduling_client_file_database_expire_time = '%u', "\
               "recipients_file = '%s'," \
               "system_is_complete = '%s'," \
               "system_nr_of_transmitted_bytes = '%u'," \
               "system_completion_percentage = '%.2f'," \
               "system_next_start_time = '%s'," \
               "system_transmissions_done = '%u'," \
               "system_packet_naks_allowed = '%s'," \
               "')>" % (self.files_acknowledge_id,
                        self.files_source_directory,
                        self.files_target_directory,
                        self.files_state_files_directory,
                        self.files_integrity_check,
                        self.channel_name,
                        self.accounting_customer,
                        self.scheduling_allow_recipient_modifications,
                        self.scheduling_start_time,
                        self.scheduling_priority,
                        self.scheduling_retransmission_interval,
                        self.scheduling_start_time_window,
                        self.scheduling_nr_of_transmissions,
                        self.scheduling_status_keep_time,
                        self.scheduling_expire_time,
                        self.scheduling_retransmission_type,
                        self.scheduling_acknowledgement_interval,
                        self.scheduling_loss_rate_threshold,
                        self.scheduling_request_acknowledgements,
                        self.scheduling_atomicity,
                        self.scheduling_client_file_database_expire_time,
                        self.recipients_file,
                        self.system_is_complete,
                        self.system_nr_of_transmitted_bytes,
                        self.system_completion_percentage,
                        self.system_next_start_time,
                        self.system_transmissions_done,
                        self.system_packet_naks_allowed
                        )


def str2bool(v):
    # TODO : handle the 'False' cases and return error if not found
    return v.lower() in ("yes", "true", "t", "1")


class _InitPersist:
    """
     Initiates the Persistence with SQLAlchemy
    """
    _engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.drop_all(_engine)
    Base.metadata.create_all(_engine)
    _Session = sessionmaker(bind=_engine)

    def __init__(self):
        self.session = self._Session()


if __name__ == '__main__':
    filepath = 'sample.job'
    data = parse(filepath)
