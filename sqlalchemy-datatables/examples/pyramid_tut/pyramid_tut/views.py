"""Pyramid_tut main views."""
from pyramid.response import Response
from pyramid.view import view_config
from sqlalchemy.exc import DBAPIError
from sqlalchemy import func
from datatables import ColumnDT, DataTables

from .models import DBSession, Job, File, Recipient


@view_config(route_name='home', renderer='templates/home.jinja2')
def home(request):
    """Try to connect to database, and list available examples."""
    try:
        DBSession.query(Job).first()
    except DBAPIError:
        return Response(
            conn_err_msg, content_type='text/plain', status_int=500)
    return {'project': 'pyramid_tut'}


@view_config(route_name='dt_110x', renderer='templates/dt_110x.jinja2')
def dt_110x(request):
    """List users with DataTables >= 1.10.x."""
    return {'project': 'dt_110x'}


@view_config(route_name='dt_110x_custom_column',
             renderer='templates/dt_110x_custom_column.jinja2')
def dt_110x_custom_column(request):
    """Show a CRUD custom column"""
    return {'project': 'dt_110x_custom_column'}


@view_config(route_name='dt_110x_basic_column_search',
             renderer='templates/dt_110x_basic_column_search.jinja2')
def dt_110x_basic_column_search(request):
    """Text based per column search"""
    return {'project': 'dt_110x_basic_column_search'}


@view_config(route_name='dt_110x_advanced_column_search',
             renderer='templates/dt_110x_advanced_column_search.jinja2')
def dt_110x_advanced_column_search(request):
    """Advanced per column search"""
    return {'project': 'dt_110x_advanced_column_search'}


@view_config(route_name='dt_110x_yadcf',
             renderer='templates/dt_110x_yadcf.jinja2')
def dt_110x_yadcf(request):
    """Search with yadcf"""
    return {'project': 'dt_110x_yadcf'}


@view_config(route_name='data', renderer='json')
def data(request):
    """Return server side data."""
    # defining columns
    #  - explicitly cast date to string, so string searching the date
    #    will search a date formatted equal to how it is presented
    #    in the table
    columns = [
        #ColumnDT(Job.files_acknowledge_id),
        ColumnDT(Job.channel_name),
        #ColumnDT(Job.scheduling_priority),
        #ColumnDT(Job.scheduling_start_time),
        #ColumnDT(Job.system_nr_of_transmitted_bytes)
        ColumnDT(File.target_path),
        ColumnDT(File.size),
        ColumnDT(File.time_stamp),
        ColumnDT(Recipient.name)
        #ColumnDT(Recipient.received)
    ]

    # defining the initial query depending on your purpose
    #  - don't include any columns
    #  - if you need a join, also include a 'select_from'
    query = DBSession.query().select_from(Job).join(File).join(Recipient).filter(File.type == 1)
#        .filter(Address.id > 4)
#    query = DBSession.query().select_from(Job)

    # instantiating a DataTable for the query and table needed
    row_table = DataTables(request.GET, query, columns)

    # returns what is needed by DataTable
    return row_table.output_result()


@view_config(route_name='data_advanced', renderer='json_with_dates')
def data_advanced(request):
    """Return server side data."""
    # defining columns
    columns = [
        #ColumnDT(Job.scheduling_priority, search_method='numeric'),
        ColumnDT(Job.channel_name),
        ColumnDT(File.target_path),
        ColumnDT(File.size, search_method='numeric'),
        #ColumnDT(Job.accounting_customer),
        ColumnDT(File.time_stamp, search_method='date'),
        ColumnDT(Recipient.name)
        #ColumnDT(Recipient.received, search_method='numeric')
    ]

    # defining the initial query depending on your purpose
    query = DBSession.query().select_from(Job).join(File).join(Recipient).filter(File.type == 1)

    # instantiating a DataTable for the query and table needed
    row_table = DataTables(request.GET, query, columns)

    # returns what is needed by DataTable
    return row_table.output_result()


@view_config(route_name='data_yadcf', renderer='json_with_dates')
def data_yadcf(request):
    """Return server side data."""
    # defining columns
    columns = [
        ColumnDT(Job.channel_name, search_method='yadcf_multi_select'),
        ColumnDT(File.target_path, search_method='yadcf_autocomplete'),
        ColumnDT(File.size, search_method='yadcf_range_number'),
        ColumnDT(Recipient.name, search_method='yadcf_multi_select'),
        #ColumnDT(Recipient.received, search_method='yadcf_range_number_slider')
        ColumnDT(Job.system_next_start_time, search_method='yadcf_range_date')
    ]

    # defining the initial query depending on your purpose
    # defining the initial query depending on your purpose
    #    query = DBSession.query().\
    #            select_from(User).\
    #        join(Address).\
    #        filter(Address.id > 4)
    query = DBSession.query().select_from(Job).join(File).join(Recipient).filter(File.type == 1)

    # instantiating a DataTable for the query and table needed
    row_table = DataTables(request.GET, query, columns)

    # returns what is needed by DataTable
    return row_table.output_result()


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
