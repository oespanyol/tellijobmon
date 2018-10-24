"""Pyramid tutorial models.

Basic example: a User has one or many Addresses.
"""
import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (backref, relationship, scoped_session, sessionmaker)
from sqlalchemy import engine_from_config
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    files_acknowledge_id = Column(String)
    files = relationship('File', backref=backref('Job'))
    recipients = relationship('Recipient', backref=backref('File'))
    files_source_directory = Column(String)
    files_target_directory = Column(String)
    files_state_files_directory = Column(String)
    files_integrity_check = Column(Boolean, unique=False, default=False)
    channel_name = Column(String)
    accounting_customer = Column(String)
    scheduling_allow_recipient_modifications = Column(String)
    scheduling_start_time = Column(DateTime)
    scheduling_priority = Column(Integer)
    scheduling_retransmission_interval = Column(Integer)
    scheduling_start_time_window = Column(Integer)
    scheduling_nr_of_transmissions = Column(Integer)
    scheduling_status_keep_time = Column(Integer)
    scheduling_expire_time = Column(DateTime)
    scheduling_retransmission_type = Column(String)
    scheduling_acknowledgement_interval = Column(Integer)
    scheduling_loss_rate_threshold = Column(Integer)
    scheduling_request_acknowledgements = Column(Integer)
    scheduling_atomicity = Column(Integer)
    scheduling_client_file_database_expire_time = Column(Integer)
    recipients_file = Column(String)
    system_is_complete = Column(Boolean, unique=False, default=True)
    system_nr_of_transmitted_bytes = Column(Integer)
    system_completion_percentage = Column(Float)
    system_next_start_time = Column(DateTime)
    system_transmissions_done = Column(Integer)
    system_packet_naks_allowed = Column(Boolean, unique=False, default=False)

    def __init__(self, jobdict):
        self.files_acknowledge_id = jobdict['files_acknowledge_id']
        self.files_source_directory = jobdict['files_source_directory']
        self.files_target_directory = jobdict['files_target_directory']
        self.files_state_files_directory = jobdict['files_state_files_directory']
        self.files_integrity_check = str2bool(jobdict['files_integrity_check'])
        self.channel_name = jobdict['channel_name']
        self.accounting_customer = jobdict['accounting_customer']
        self.scheduling_allow_recipient_modifications = str2bool(jobdict['scheduling_allow_recipient_modifications'])
        self.scheduling_start_time = datetime.datetime.strptime(jobdict['scheduling_start_time'],"%Y-%m-%d %H:%M:%S")
        self.scheduling_priority = int(jobdict['scheduling_priority'])
        self.scheduling_retransmission_interval = int(jobdict['scheduling_retransmission_interval'])
        self.scheduling_start_time_window = int(jobdict['scheduling_start_time_window'])
        self.scheduling_nr_of_transmissions = int(jobdict['scheduling_nr_of_transmissions'])
        self.scheduling_status_keep_time = int(jobdict['scheduling_status_keep_time'])
        self.scheduling_expire_time = datetime.datetime.strptime(jobdict['scheduling_expire_time'],
                                                                 "%Y-%m-%d %H:%M:%S")
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
        self.system_next_start_time = datetime.datetime.strptime(jobdict['system_next_start_time'],"%Y-%m-%d %H:%M:%S")
        self.system_transmissions_done = int(jobdict['system_transmissions_done'])
        self.system_packet_naks_allowed = str2bool(jobdict['system_packet_naks_allowed'])

    def to_json_table(self):

        job_copy = self.__dict__.copy()
        # Remove entry corresponding to SQLAlchemy: _sa_instance_state
        job_copy.pop('_sa_instance_state', None)

        output = {}
        job_data = []
        for key, value in job_copy.iteritems():
            columns = {}
            columns['0'] = str(key)
            columns['1'] = str(value)
            job_data.append(columns)

        output['draw'] = str(int("1"))
        output['recordsTotal'] = str(len(job_copy))
        output['recordsFiltered'] = str(len(job_copy))
        output['data'] = job_data

        return output

    def __repr__(self):
        return "<Job(" \
               "id = '%s'," \
               "files_acknowledge_id = '%s'," \
               "files_source_directory = '%s'," \
               "files_target_directory = '%s'," \
               "files_state_files_directory = '%s'," \
               "files_integrity_check = '%s'," \
               "channel_name = '%s', " \
               "accounting_customer = '%s'," \
               "scheduling_allow_recipient_modifications = '%s', " \
               "scheduling_start_time = '%s'," \
               "scheduling_priority = '%u', " \
               "scheduling_retransmission_interval = '%u', " \
               "scheduling_start_time_window = '%u', " \
               "scheduling_nr_of_transmissions = '%u', " \
               "scheduling_status_keep_time = '%u', " \
               "scheduling_expire_time = '%s'," \
               "scheduling_retransmission_type = '%s', " \
               "scheduling_acknowledgement_interval = '%u', " \
               "scheduling_loss_rate_threshold = '%u', " \
               "scheduling_request_acknowledgements = '%u', " \
               "scheduling_atomicity = '%u', " \
               "scheduling_client_file_database_expire_time = '%u', " \
               "recipients_file = '%s'," \
               "system_is_complete = '%s'," \
               "system_nr_of_transmitted_bytes = '%u'," \
               "system_completion_percentage = '%.2f'," \
               "system_next_start_time = '%s'," \
               "system_transmissions_done = '%u'," \
               "system_packet_naks_allowed = '%s'," \
               "')>" % (self.id,
                        self.files_acknowledge_id,
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
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(String)
    files_acknowledge_id = Column(String, ForeignKey('jobs.files_acknowledge_id'))
    done = Column(Boolean, unique=False, default=False)
    type = Column(Integer)
    relay_file = Column(Boolean, unique=False, default=False)
    path = Column(String)
    target_path = Column(String)
    state_file = Column(String)
    size = Column(Integer)
    sent_fragment = Column(String)
    time_stamp = Column(DateTime)
    last_send_time_stamp = Column(DateTime)

    def __init__(self, filedict):
        self.file_id = filedict['id']
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

    def to_json_table(self):

        file_copy = self.__dict__.copy()
        # Remove entry corresponding to SQLAlchemy: _sa_instance_state
        file_copy.pop('_sa_instance_state', None)

        output = {}
        job_data = []
        for key, value in file_copy.iteritems():
            columns = {}
            columns['0'] = str(key)
            columns['1'] = str(value)
            job_data.append(columns)

        output['draw'] = str(int("1"))
        output['recordsTotal'] = str(len(file_copy))
        output['recordsFiltered'] = str(len(file_copy))
        output['data'] = job_data

        return output

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
               "size = '%u', " \
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
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    ip = Column(String)
    files_acknowledge_id = Column(String, ForeignKey('jobs.files_acknowledge_id'))
    unconfirmed = Column(Boolean, unique=False, default=False)
    complete = Column(Boolean, unique=False, default=False)
    received = Column(Float)

    def __init__(self, recipientdict):
        # Mandatory fields
        self.name = recipientdict['name']
        self.files_acknowledge_id = recipientdict['files_acknowledge_id']
        # Optional fields
        if 'ip' in recipientdict:
            self.ip = recipientdict['ip']
        if 'unconfirmed' in recipientdict:
            self.unconfirmed = str2bool(recipientdict['unconfirmed'])
        if 'complete' in recipientdict:
            self.complete = str2bool(recipientdict['complete'])
        if 'received' in recipientdict:
            self.received = float(recipientdict['received'])

    def __repr__(self):
        return "<Recipient(" \
               "id='%s', " \
               "name='%s', " \
               "ip='%s', " \
               "files_acknowledge_id='%s', " \
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


class TimeSlot(Base):
    __tablename__ = 'time_slots'
    id = Column(String, primary_key=True)
    duration = Column(Integer)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    total_nr_of_bytes = Column(Integer)
    total_nr_of_files = Column(Integer)
    recipients = relationship('RecipientTimeSlot', backref=backref('TimeSlot'))

    def __init__(self, time_slot_dict):
        self.duration = int(time_slot_dict['duration'])
        self.start_time = time_slot_dict['start_time']
        self.end_time = time_slot_dict['end_time']
        self.total_nr_of_bytes = int(time_slot_dict['total_nr_of_bytes'])
        self.total_nr_of_files = int(time_slot_dict['total_nr_of_files'])
        self.id = self.start_time.strftime("%s") + '+' + str(self.duration)

    def update(self, a_dict):
        self.total_nr_of_bytes = a_dict['total_nr_of_bytes']
        self.total_nr_of_files = a_dict['total_nr_of_files']

    def __repr__(self):
        return "<TimeSlot(" \
               "id='%s', " \
               "duration='%s', " \
               "start_time='%s', " \
               "end_time='%s', " \
               "total_nr_of_bytes='%s', " \
               "total_nr_of_files='%s'" \
               ")>" % (self.id,
                       self.duration,
                       self.start_time,
                       self.end_time,
                       self.total_nr_of_bytes,
                       self.total_nr_of_files
                       )


class RecipientTimeSlot(Base):
    __tablename__ = 'recipients_time_slots'
    id = Column(Integer, primary_key=True, autoincrement=True)
    time_slot_id = Column(String, ForeignKey('time_slots.id'))
    name = Column(String)
    sent_nr_of_bytes = Column(Integer)
    sent_nr_of_files = Column(Integer)
    received_nr_of_bytes = Column(Integer)
    received_nr_of_files = Column(Integer)

    def __init__(self, rec_time_slot_dict):
        self.name = rec_time_slot_dict['name']
        self.time_slot_id = rec_time_slot_dict['time_slot_id']
        self.sent_nr_of_bytes = int(rec_time_slot_dict['sent_nr_of_bytes'])
        self.sent_nr_of_files = int(rec_time_slot_dict['sent_nr_of_files'])
        self.received_nr_of_bytes = int(rec_time_slot_dict['received_nr_of_bytes'])
        self.received_nr_of_files = int(rec_time_slot_dict['received_nr_of_files'])

    def update(self, a_dict):
        self.sent_nr_of_bytes = a_dict['sent_nr_of_bytes']
        self.sent_nr_of_files = a_dict['sent_nr_of_files']
        self.received_nr_of_bytes = a_dict['received_nr_of_bytes']
        self.received_nr_of_files = a_dict['received_nr_of_files']

    def __repr__(self):
        return "<RecipientTimeSlot(" \
               "id='%s', " \
               "time_slot_id='%s', " \
               "name='%s', " \
               "sent_nr_of_bytes='%s', " \
               "sent_nr_of_files='%s', " \
               "received_nr_of_bytes='%s', " \
               "received_nr_of_files='%s'" \
               ")>" % (self.id,
                       self.time_slot_id,
                       self.name,
                       self.sent_nr_of_bytes,
                       self.sent_nr_of_files,
                       self.received_nr_of_bytes,
                       self.received_nr_of_files
                       )


def str2bool(v):
    # TODO : handle the 'False' cases and return error if not found
    return v.lower() in ("yes", "true", "t", "1")


def serialize(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial

    return obj.__dict__


class _InitPersist:
    """
     Initiates the Persistence with SQLAlchemy
    """
    # TODO: Have all configuration read freom same
    config = {'sqlalchemy.url': 'sqlite:////home/espanyol/workspace/tellijobsparser/'
                        'sqlalchemy-datatables/examples/pyramid_tut/tellijobsparser.sqlite', 'sqlalchemy.echo': 'True'}

    _engine = engine_from_config(config, 'sqlalchemy.')
    #Base.metadata.drop_all(_engine)
    Base.metadata.create_all(_engine)
    _Session = sessionmaker(bind=_engine)

    def __init__(self):
        self.session = self._Session()


def init():
    session = _InitPersist().session
    return session
