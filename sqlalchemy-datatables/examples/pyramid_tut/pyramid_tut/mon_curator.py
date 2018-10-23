#!/usr/bin/env python

from datetime import datetime, timedelta


from models import Job, File, Recipient, TimeSlot, RecipientTimeSlot, init


def gen_avail_stats(time_slot_duration):

    #datetime.datetime(year, month, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]])
    start_time = datetime(2018, 9, 24, 06, 0, 0)
    end_time = start_time + timedelta(seconds=time_slot_duration)

    session = init()

    jobs = session.query(Job).join(File).join(Recipient).\
        filter(File.type == 1).\
        filter(File.time_stamp > start_time).\
        filter(File.time_stamp <= end_time).all()

    time_slot_dict = {'duration': time_slot_duration,
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
                    recip_files_dict = {'sent_nr_of_bytes': 0,
                                        'sent_nr_of_files': 0,
                                        'received_nr_of_bytes': 0,
                                        'received_nr_of_files': 0,
                                        'name': name}
                    recip_reports[name] = recip_files_dict

                recip_reports[name]['sent_nr_of_bytes'] += a_file.size
                recip_reports[name]['sent_nr_of_files'] += 1

                if recipient.complete:
                    recip_reports[name]['received_nr_of_bytes'] += a_file.size
                    recip_reports[name]['received_nr_of_files'] += 1

    # Persist time slots in database
    new_time_slot = TimeSlot(time_slot_dict)
    old_time_slot = session.query(TimeSlot).filter(TimeSlot.id == new_time_slot.id).first()
    old_time_slot = new_time_slot
    session.commit()

    #session.add(a_time_slot)
    for key, value in recip_reports.iteritems():
        a_recip_report = RecipientTimeSlot(value)
        session.add(a_recip_report)

    session.commit()


if __name__ == '__main__':

    time_slot_duration = int(100)
    gen_avail_stats(time_slot_duration)

