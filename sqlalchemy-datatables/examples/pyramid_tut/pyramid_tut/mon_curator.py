#!/usr/bin/env python

from datetime import datetime, timedelta
from models import Job, File, Recipient, TimeSlot, RecipientTimeSlot, init
from sqlalchemy import and_


def gen_avail_stats(start_time, time_slot_duration):

    end_time = start_time + timedelta(seconds=time_slot_duration)

    session = init()

    # Query DB for files within the time_slot.
    # Take only regular files, i.e. of type = 1, and do not consider file list files.
    jobs = session.query(Job).join(File).join(Recipient).\
        filter(File.type == 1).\
        filter(File.time_stamp > start_time).\
        filter(File.time_stamp <= end_time).all()

    time_slot_dict = {'id': start_time.strftime("%s")+'+'+str(time_slot_duration),
                      'duration': time_slot_duration,
                      'total_nr_of_bytes': 0,
                      'total_nr_of_files': 0,
                      'start_time': start_time,
                      'end_time': end_time}

    # TODO: It can probably be done with less for nesting
    recip_reports = {}
    for job in jobs:
        for a_file in job.files:

            time_slot_dict['total_nr_of_files'] += 1
            time_slot_dict['total_nr_of_bytes'] += a_file.size

            for recipient in job.recipients:
                name = recipient.name
                if name not in recip_reports.keys():
                    recip_files_dict = {'name': name,
                                        'time_slot_id': time_slot_dict['id'],
                                        'sent_nr_of_bytes': 0,
                                        'sent_nr_of_files': 0,
                                        'received_nr_of_bytes': 0,
                                        'received_nr_of_files': 0}
                    recip_reports[name] = recip_files_dict

                recip_reports[name]['sent_nr_of_bytes'] += a_file.size
                recip_reports[name]['sent_nr_of_files'] += 1

                if recipient.complete:
                    recip_reports[name]['received_nr_of_bytes'] += a_file.size
                    recip_reports[name]['received_nr_of_files'] += 1

    # Persist time slots in database
    time_slot_query = session.query(TimeSlot).filter(TimeSlot.id == time_slot_dict['id']).first()
    if not time_slot_query:
        # Create a new time slot if none exists
        session.add(TimeSlot(time_slot_dict))
    else:
        # Update time_slot if it already exists
        time_slot_query.update(time_slot_dict)

    # Persist user time slots in database
    for recp, recp_dict in recip_reports.iteritems():

        recp_ts = session.query(RecipientTimeSlot).filter(and_(
            RecipientTimeSlot.time_slot_id == recp_dict['time_slot_id'],
            RecipientTimeSlot.name == recp_dict['name'])
        ).first()

        if not recp_ts:
            # Create a new entry
            session.add(RecipientTimeSlot(recp_dict))
        else:
            # Update entry
            recp_ts.update(recp_dict)

    session.commit()


if __name__ == '__main__':

    start_time = datetime(2018, 9, 24, 05, 15, 0)
    end_time = datetime(2018, 9, 24, 07, 15, 0)
    time_slot_duration = int(900)

    calc_time = start_time
    while calc_time < end_time:
        print("Calculating time slot: " + calc_time.isoformat())
        gen_avail_stats(calc_time, time_slot_duration)
        calc_time = calc_time + timedelta(seconds=time_slot_duration)

