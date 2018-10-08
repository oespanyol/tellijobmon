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

        session = _InitPersist().session

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
                    # TODO: Handle duplicates, like in [files] file=

            afile = File(filel_dict)
            session.add(afile)

#        myfile = session.query(File).filter_by(file_id='5ba88d2e0012de5a').first()
#        print(myfile)

        # Iterate through the lists that contain recipients information, parse, compile and persist it into a table
        received_dict = {}

        # Put all contents together in one list
        recipient_contents = [ip_content, unconfirmed_content, complete_content, received_content]

        # Instantiate a recipient dictionary to keep all the keys and values
        recipient_dict = {}
        # Iterate through the list of contents to prepend the name of the section
        # TODO: To complex -> simplify
        for content in recipient_contents:
            prefix = content[0]
            lines = content[1]
            for line in lines.splitlines():
                if line.strip():
                    recipient_kvp = line.split("=", 2)
                    print(recipient_kvp)
                    if recipient_kvp[0] == 'name':
                        # Create one entry if it doesn't exist yet
                        key = recipient_kvp[1]
                        if key not in recipient_dict:
                            recipient = {prefix: 'True'}
                            recipient_dict[key] = recipient

                        # If it already exists, get instance and fill details of existing entry
                        if key in recipient_dict:
                            recipient = recipient_dict[key]
                            recipient[prefix] = 'True'
                            recipient_dict[key] = recipient

                    if recipient_kvp[0] != 'name':
                        # Create one entry if it doesn't exist yet
                        key = recipient_kvp[0]
                        value = recipient_kvp[1]
                        if key not in recipient_dict:
                            recipient = {prefix: value}
                            recipient_dict[key] = recipient

                        # If it already exists, get instance and fill details of existing entry
                        if key in recipient_dict:
                            recipient = recipient_dict[key]
                            recipient[prefix] = value
                            recipient_dict[key] = recipient

        print(recipient_dict)

    return text


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


class Job(Base):
    __tablename__ = 'jobs'
    files_acknowledge_id                        = Column(String, primary_key=True)
    files_source_directory                      = Column(String  )
    files_target_directory                      = Column(String  )
    files_state_files_directory                 = Column(String  )
    files_integrity_check                       = Column(Boolean, unique=False, default=False)
    channel_name                                = Column(String  )
    accounting_customer                         = Column(String  )
    scheduling_allow_recipient_modifications    = Column(String  )
    scheduling_start_time                       = Column(DateTime)
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
    system_is_complete                          = Column(Boolean, unique=False, default=True)
    system_nr_of_transmitted_bytes              = Column(Integer )
    system_completion_percentage                = Column(Float   )
    system_next_start_time                      = Column(DateTime)
    system_transmissions_done                   = Column(Integer )
    system_packet_naks_allowed                  = Column(Boolean, unique=False, default=False)

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


class File(Base):
    __tablename__ = 'files'
    id                   = Column(Integer, primary_key=True, autoincrement=True)
    file_id              = Column(String)
    files_acknowledge_id = Column(String)
    done                 = Column(Boolean, unique=False, default=False)
    type                 = Column(Integer)
    relay_file           = Column(Boolean, unique=False, default=False)
    path                 = Column(String)
    target_path          = Column(String)
    state_file           = Column(String)
    size                 = Column(Integer)
    sent_fragment        = Column(String)
    time_stamp           = Column(DateTime)
    last_send_time_stamp = Column(DateTime)

    def __init__(self, filedict):
        self.file_id              = filedict['id']
        if 'files_acknowledge_id' in filedict:
            self.files_acknowledge_id = filedict['files_acknowledge_id']
        if 'done' in filedict:
            self.done = str2bool(filedict['done'])
        if 'type' in filedict:
            self.type = int(filedict['type'])
        if 'relay_file' in filedict:
            self.relay_file = str2bool(filedict['relay_file'])
        if 'path' in filedict:
            self.path = filedict['path']
        if 'target_path' in filedict:
            self.target_path = filedict['target_path']
        if 'state_file' in filedict:
            self.state_file = filedict['state_file']
        if 'size' in filedict:
            self.size = int(filedict['size'])
        if 'sent_fragment' in filedict:
            self.sent_fragment = filedict['sent_fragment']
        if 'time_stamp' in filedict:
            self.time_stamp = datetime.datetime.strptime(filedict['time_stamp'][:26], "%Y-%m-%d %H:%M:%S.%f")
        if 'last_send_time_stamp' in filedict:
            self.last_send_time_stamp = \
                datetime.datetime.strptime(filedict['last_send_time_stamp'][:26], "%Y-%m-%d %H:%M:%S.%f")

    def __repr__(self):
        return "<File(" \
               "id = '%s'," \
               "file_id = '%s'," \
               "files_acknowledge_id = '%s'," \
               "done = '%s'," \
               "type = '%u'," \
               "relay_file = '%s'," \
               "path = '%s', " \
               "target_path = '%s'," \
               "state_file = '%s'," \
               "size = '%u', "\
               "sent_fragment = '%s'," \
               "time_stamp = '%s'," \
               "last_send_time_stamp = '%s'," \
               "')>" % (self.id,
                        self.file_id,
                        self.files_acknowledge_id,
                        self.done,
                        self.type,
                        self.relay_file,
                        self.path,
                        self.target_path,
                        self.state_file,
                        self.size,
                        self.sent_fragment,
                        self.time_stamp,
                        self.last_send_time_stamp
                        )


class Recipient(Base):
    __tablename__ = 'recipients'
    id                   = Column(Integer, primary_key=True, autoincrement=True)
    name                 = Column(String)
    ip                   = Column(String)
    files_acknowledge_id = Column(String)
    unconfirmed          = Column(Boolean, unique=False, default=False)
    complete             = Column(Boolean, unique=False, default=False)
    received_percentage  = Column(Float)

    def __init__(self, recipientdict):
        self.name                 = recipientdict['name']
        self.ip                   = recipientdict['ip']
        self.files_acknowledge_id = recipientdict['files_acknowledge_id']
        self.unconfirmed          = str2bool(recipientdict['unconfirmed'])
        self.complete             = str2bool(recipientdict['complete'])
        self.received_percentage  = float(recipientdict['received_percentage'])

    def __repr__(self):
        return "<Recipient(" \
               "id = '%s'," \
               "name = '%s'," \
               "ip = '%s'," \
               "files_acknowledge_id = '%u', "\
               "unconfirmed = '%s'," \
               "complete = '%s'," \
               "received_percentage = '%.6f'," \
               "')>" % (self.id,
                        self.name,
                        self.ip,
                        self.files_acknowledge_id,
                        self.unconfirmed,
                        self.complete,
                        self.received_percentage
                        )


def str2bool(v):
    # TODO : handle the 'False' cases and return error if not found
    return v.lower() in ("yes", "true", "t", "1")


class _InitPersist:
    """
     Initiates the Persistence with SQLAlchemy
    """
    _engine = create_engine('sqlite:///:memory:', echo=False)
    Base.metadata.drop_all(_engine)
    Base.metadata.create_all(_engine)
    _Session = sessionmaker(bind=_engine)

    def __init__(self):
        self.session = self._Session()


if __name__ == '__main__':
    filepath = 'sample.job'
    data = parse(filepath)
