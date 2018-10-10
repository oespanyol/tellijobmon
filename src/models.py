#!/usr/bin/env python

import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean


__author__    = "Oriol Espanyol"
__copyright__ = "Copyright 2018, EUMETCast Terrestrial Pathfinder-II"
__license__   = "GPL"
__version__   = "1.0.1"
__email__     = "oriol.espanyol@eumetsat.int"
__status__    = "Development"

Base = declarative_base()


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
    received             = Column(Float)

    def __init__(self, recipientdict):
        # Mandatory fields
        self.name                 = recipientdict['name']
        self.files_acknowledge_id = recipientdict['files_acknowledge_id']
        # Optional fields
        if 'ip' in recipientdict:
            self.ip                   = recipientdict['ip']
        if 'unconfirmed' in recipientdict:
            self.unconfirmed          = str2bool(recipientdict['unconfirmed'])
        if 'complete' in recipientdict:
            self.complete             = str2bool(recipientdict['complete'])
        if 'received' in recipientdict:
            self.received             = float(recipientdict['received'])

    def __repr__(self):
        return "<Recipient(" \
               "id='%s', " \
               "name='%s', " \
               "ip='%s', " \
               "files_acknowledge_id='%s', "\
               "unconfirmed='%s', " \
               "complete='%s', " \
               "received='%.6f'" \
               ")>" % (self.id,
                       self.name,
                       self.ip,
                       self.files_acknowledge_id,
                       self.unconfirmed,
                       self.complete,
                       self.received
                       )


def str2bool(v):
    # TODO : handle the 'False' cases and return error if not found
    return v.lower() in ("yes", "true", "t", "1")


class _InitPersist:
    """
     Initiates the Persistence with SQLAlchemy
    """
    _engine = create_engine('sqlite:////home/espanyol/workspace/tellijobsparser/db/tellijobsparser.db', echo=False)
    Base.metadata.drop_all(_engine)
    Base.metadata.create_all(_engine)
    _Session = sessionmaker(bind=_engine)

    def __init__(self):
        self.session = self._Session()


def init():
    session = _InitPersist().session
    return session


