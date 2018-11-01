"""Pyramid_tut main views."""
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from datatables import ColumnDT, DataTables
from .models import DBSession, Job, File, Recipient, TimeSlot, RecipientTimeSlot
from datetime import datetime
from collections import defaultdict
import json
from sqlalchemy import or_

@view_config(route_name='home', renderer='templates/home.jinja2')
def home(request):
    """Try to connect to database, and list available examples."""
    try:
        DBSession.query(Job).first()
    except DBAPIError:
        return Response(
            conn_err_msg, content_type='text/plain', status_int=500)
    return {'project': 'pyramid_tut'}


@view_config(route_name='jobs',
             renderer='templates/jobs.jinja2')
def all_jobs(request):
    """Search with yadcf"""
    return {'project': 'jobs'}


@view_config(route_name='files',
             renderer='templates/files.jinja2')
def all_files(request):
    """Search with yadcf"""
    return {'project': 'files'}


@view_config(route_name='recipients',
             renderer='templates/recipients.jinja2')
def all_recipients(request):
    """Search with yadcf"""
    return {'project': 'recipients'}


@view_config(route_name='show_job',
             renderer='templates/show_job.jinja2')
def show_job(request):
    """Display a job"""
    return {'project': 'show_job'}


@view_config(route_name='monitor',
             renderer='templates/monitor.jinja2')
def monitor(request):
    """Display a job"""
    return {'project': 'monitor'}


@view_config(route_name='roll_mon',
             renderer='templates/roll_mon.jinja2')
def roll_mon(request):
    """Display a job"""
    return {'project': 'roll_mon'}


@view_config(route_name='job',
             request_method='GET',
             request_param='job_id',
             renderer='json')
def job(request):
    # Get the job ID from the request
    job_id = request.GET["job_id"]
    # Retrieve the corresponding job from the DB
    the_job = DBSession.query(Job).filter(Job.files_acknowledge_id == str(job_id)).first()
    job_json = the_job.to_json_table()
    return job_json


@view_config(route_name='show_file',
             renderer='templates/show_file.jinja2')
def show_file(request):
    """Display a file"""
    return {'project': 'show_file'}


@view_config(route_name='file',
             request_method='GET',
             request_param='file_id',
             renderer='json')
def file(request):
    # Get the job ID from the request
    file_id = request.GET["file_id"]
    # Retrieve the corresponding job from the DB
    the_file = DBSession.query(File).filter(File.file_id == str(file_id)).first()
    file_json = the_file.to_json_table()
    return file_json


@view_config(route_name='jobs_data', renderer='json_with_dates')
def jobs_data(request):
    """Return server side data."""
    # defining columns
    columns = [
        ColumnDT(Job.files_acknowledge_id),
        ColumnDT(Job.channel_name, search_method='yadcf_multi_select'),
        ColumnDT(Job.scheduling_start_time, search_method='yadcf_range_date'),
        ColumnDT(Job.scheduling_priority, search_method='yadcf_range_number'),
        ColumnDT(Job.scheduling_acknowledgement_interval, search_method='yadcf_range_number'),
        ColumnDT(Job.system_nr_of_transmitted_bytes, search_method='yadcf_range_number'),
        ColumnDT(Job.system_completion_percentage, search_method='yadcf_range_number'),
        ColumnDT(Job.system_transmissions_done, search_method='yadcf_range_number')
    ]

    # defining the initial query depending on your purpose
    query = DBSession.query().select_from(Job)

    # instantiating a DataTable for the query and table needed
    row_table = DataTables(request.GET, query, columns)

    # returns what is needed by DataTable
    return row_table.output_result()


@view_config(route_name='files_data', renderer='json_with_dates')
def files_data(request):
    """Return server side data."""
    # defining columns
    columns = [
        ColumnDT(File.file_id, search_method='text'),
        ColumnDT(Job.files_acknowledge_id, search_method='text'),
        ColumnDT(File.target_path, search_method='text'),
        ColumnDT(File.size, search_method='yadcf_range_number'),
        ColumnDT(File.time_stamp, search_method='yadcf_range_date')
    ]

    # defining the initial query depending on your purpose
    query = DBSession.query().select_from(Job).join(File).filter(File.type == 1)

    # instantiating a DataTable for the query and table needed
    row_table = DataTables(request.GET, query, columns)

    # returns what is needed by DataTable
    return row_table.output_result()


@view_config(route_name='recipients_data', renderer='json_with_dates')
def recipients_data(request):
    """Return server side data."""
    # defining columns
    columns = [
        ColumnDT(File.target_path),
        ColumnDT(Job.channel_name, search_method='yadcf_multi_select'),
        ColumnDT(Recipient.name, search_method='yadcf_multi_select'),
        ColumnDT(File.time_stamp, search_method='yadcf_range_date'),
        ColumnDT(Recipient.received, search_method='yadcf_range_number'),
        ColumnDT(Job.files_acknowledge_id),
        ColumnDT(File.size, search_method='yadcf_range_number')
    ]

    # defining the initial query depending on your purpose
    query = DBSession.query().select_from(Job).join(File).join(Recipient).filter(File.type == 1)

    # instantiating a DataTable for the query and table needed
    row_table = DataTables(request.GET, query, columns)

    # returns what is needed by DataTable
    return row_table.output_result()


@view_config(route_name='monitor_data', renderer='json_with_dates')
def monitor_data(request):
    """Return server side data."""
    # defining columns

    columns = [
        ColumnDT(TimeSlot.start_time, search_method='yadcf_range_date'),
        ColumnDT(TimeSlot.total_nr_of_files, search_method='yadcf_range_number'),
        ColumnDT(TimeSlot.total_nr_of_bytes, search_method='yadcf_range_number'),
        ColumnDT(RecipientTimeSlot.name, search_method='yadcf_multi_select'),
        ColumnDT(RecipientTimeSlot.sent_nr_of_files, search_method='yadcf_range_number'),
        ColumnDT(RecipientTimeSlot.received_nr_of_files, search_method='yadcf_range_number'),
        ColumnDT(RecipientTimeSlot.sent_nr_of_bytes, search_method='yadcf_range_number'),
        ColumnDT(RecipientTimeSlot.received_nr_of_bytes, search_method='yadcf_range_number')
    ]

    # defining the initial query depending on your purpose
    query = DBSession.query().select_from(TimeSlot).join(RecipientTimeSlot)

    # instantiating a DataTable for the query and table needed
    row_table = DataTables(request.GET, query, columns)

    # returns what is needed by DataTable
    return row_table.output_result()


@view_config(route_name='roll_mon_data', renderer='templates/rolling_monitoring.jinja2')
def roll_mon_data(request):

    start_time = datetime(2018, 9, 24, 05, 15, 0)
    end_time = datetime(2018, 9, 24, 07, 15, 0)
    duration = 900

    # TODO : time start/end and slot duration provided by user request
    recp_query = DBSession.query(RecipientTimeSlot.name).select_from(TimeSlot).join(RecipientTimeSlot)\
        .filter(TimeSlot.start_time > start_time) \
        .filter(TimeSlot.end_time < end_time) \
        .filter(TimeSlot.duration == duration) \
        .all()

    # List of unique recipients
    recipients = list(set(recp_query))

    tsu = defaultdict(list)
    for recipient in recipients:
        name = recipient[0]
        q_results = DBSession.query(TimeSlot.start_time,
                                    RecipientTimeSlot.name,
                                    RecipientTimeSlot.sent_nr_of_files,
                                    RecipientTimeSlot.received_nr_of_files)\
            .select_from(TimeSlot).join(RecipientTimeSlot) \
            .filter(TimeSlot.start_time > start_time) \
            .filter(TimeSlot.end_time < end_time) \
            .filter(TimeSlot.duration == duration) \
            .filter(RecipientTimeSlot.name == name) \
            .all()
       # Extract the key as the Start Time of each query
        for q_result in q_results:
            q_ts = q_result[0].isoformat()
            print(q_ts)
            # Add query results indexed by start time key
            tsu[q_ts].append(q_result[1:4])

    print(tsu)
    d = dict(tsu)
    print(d)

    return {'project': 'rolling_monitoring'}


@view_config(route_name='test', renderer='templates/test.jinja2')
def test(request):
    start_time = datetime(2018, 9, 24, 05, 15, 0)
    end_time = datetime(2018, 9, 24, 07, 15, 0)
    duration = 900

    # TODO : time start/end and slot duration provided by user request
    recp_query = DBSession.query(RecipientTimeSlot.name).select_from(TimeSlot).join(RecipientTimeSlot)\
        .filter(TimeSlot.start_time > start_time) \
        .filter(TimeSlot.end_time < end_time) \
        .filter(TimeSlot.duration == duration) \
        .all()

    # List of unique recipients
    recipients = list(set(recp_query))
    # Output is a list of lists of one element
    # Get only the first element of each list
    recipients = [item[0] for item in recipients]

    tsu = defaultdict(list)
    for recipient in recipients:
        q_results = DBSession.query(TimeSlot.start_time,
                                    RecipientTimeSlot.name,
                                    RecipientTimeSlot.sent_nr_of_files,
                                    RecipientTimeSlot.received_nr_of_files)\
            .select_from(TimeSlot).join(RecipientTimeSlot) \
            .filter(TimeSlot.start_time > start_time) \
            .filter(TimeSlot.end_time < end_time) \
            .filter(TimeSlot.duration == duration) \
            .filter(RecipientTimeSlot.name == recipient) \
            .all()
       # Extract the key as the Start Time of each query
        for q_result in q_results:
            q_ts = q_result[0].isoformat()
            data = {q_result[1]: {'sentf': q_result[2],
                                  'recvf': q_result[3]}}
            # Add query results indexed by start time key
            tsu[q_ts].append(data)

    roll_mon_dict = dict(tsu)
    print(roll_mon_dict)

    url_list = {'roll_mon_dict': roll_mon_dict, 'recipients': recipients}

    return url_list


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_pyramid_tut_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
