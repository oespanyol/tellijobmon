#!/usr/bin/env python

from sqlalchemy import engine_from_config
from sqlalchemy.orm import (sessionmaker)

from models import Job, File, Recipient


def gen_avail_stats(time_slot):

    session = _Session()
    the_file = session.query(Job).join(File).join(Recipient).filter(File.type == 1).all()
    
    print(the_file)


if __name__ == '__main__':

    # TODO: Have all configuration read freom same
    config = {'sqlalchemy.url': 'sqlite:////home/espanyol/workspace/tellijobsparser/'
                        'sqlalchemy-datatables/examples/pyramid_tut/tellijobsparser.sqlite', 'sqlalchemy.echo': 'True'}

    _engine = engine_from_config(config, 'sqlalchemy.')
    _Session = sessionmaker(bind=_engine)

    time_slot = 300
    gen_avail_stats(time_slot)

