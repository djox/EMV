def date_widget(f,v):
    wrapper = DIV()
    inp = SQLFORM.widgets.string.widget(f,v,_class="jqdate")
    jqscr = SCRIPT("jQuery(document).ready(function(){jQuery('#%s').datepicker({dateFormat:'yyyy-mm-dd'});});" % inp['_id'],_type="text/javascript")
    wrapper.components.extend([inp,jqscr])
    return wrapper
	
is_phone = IS_MATCH('^(\+\d{2}\-)?[\d\-]*(\#\d+)?$')

TASK_TYPES = ('Phone', 'Fax', 'Mail', 'Meet')

if auth.is_logged_in():
   me=auth.user.id
else:
   me=None

db.define_table('measurement_place',
    Field('name'),
    Field('description'),
	Field('instruments', 'list:reference instrument'))

db.measurement_place.name.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'measurement_place.name')]


db.define_table('device_type',
    Field('name'))

db.device_type.name.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'device_type.name')]


db.define_table('manufacturer',
    Field('name'),
    Field('address'),
    Field('phone'),
    Field('fax'),
    Field('email'),
    Field('url'),
    Field('created_by',db.auth_user,default=me,writable=False,readable=False),
    Field('created_on','datetime',default=request.now,writable=False,readable=False))

db.manufacturer.name.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(db,'manufacturer.name')]
db.manufacturer.url.requires=IS_EMPTY_OR(IS_URL())
db.manufacturer.phone.requires=is_phone
db.manufacturer.fax.requires=is_phone
db.manufacturer.email.requires=IS_EMPTY_OR(IS_EMAIL(error_message='invalid email!'))


db.define_table('instrument',
    Field('name'),
    Field('device_type','reference device_type'),
    Field('serial_number'),
    Field('id_number'),
    Field('cost_center'),
    Field('manufacturer','reference manufacturer'),
    Field('calibration_interval'),
    Field('last_calibration', 'date', 'widget=date_widget'),
    Field('next_calibration', 'date', 'widget=date_widget'),
    Field('status'),
    Field('location'),
    Field('created_by',db.auth_user,default=me,writable=False,readable=False),
    Field('created_on','datetime',default=request.now,writable=False,readable=False))

db.instrument.name.requires=IS_NOT_EMPTY()
    
    
db.define_table('task',
    Field('title'),
    Field('task_type'),
    Field('instrument','reference instrument',default=None),
    Field('description','text'),
    Field('start_time','datetime'),
    Field('stop_time','datetime'),
    Field('created_by',db.auth_user,default=me,writable=False,readable=False),
    Field('created_on','datetime',default=request.now,writable=False,readable=False))

db.task.title.requires=IS_NOT_EMPTY()
db.task.task_type.requires=IS_IN_SET(TASK_TYPES)
db.task.instrument.requires=IS_IN_DB(db,'instrument.id','%(name)s')
db.task.start_time.default=request.now
db.task.stop_time.default=request.now


db.define_table('log',
    Field('instrument','reference instrument'),
    Field('body','text'),
    Field('created_by',db.auth_user,default=me,writable=False,readable=False),
    Field('created_on','datetime',default=request.now,writable=False,readable=False))

db.log.instrument.requires=IS_IN_DB(db,'instrument.id','%(name)s')
db.log.body.requires=IS_NOT_EMPTY()


db.define_table('document',
    Field('instrument','reference instrument'),
    Field('name'),
    Field('file','upload'),
    Field('created_by',db.auth_user,default=me,writable=False,readable=False),
    Field('created_on','datetime',default=request.now,writable=False,readable=False))

db.document.instrument.requires=IS_IN_DB(db,'instrument.id','%(name)s')
db.document.name.requires=IS_NOT_EMPTY()
db.document.file.requires=IS_NOT_EMPTY()
