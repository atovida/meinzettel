# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite')
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db = db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db, hmac_key=Auth.get_or_create_key())
crud, service, plugins = Crud(db), Service(), PluginManager()



## create all tables needed by auth if not custom tables
auth.define_tables()

## configure email
mail=auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth,filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

db.define_table('glosarios',
                Field('nombre_glosario', unique=True), # no puede estar repetido
                #Field('descripcion_glosario',  widget=SQLFORM.widgets.text.widget), #poner widget mostrar como campo text
                format = '%(nombre_glosario)s'
                )

db.define_table('preposiciones',
                Field('preposicion', 'string'),
                Field('clase', 'string')
                )

db.define_table('palabras',
                Field('palabra', 'string', unique=True),
                Field('sustantivo', 'boolean'),
                Field('articulo'),
                Field('plural', 'string'),
                Field('imagen', 'upload'),
                Field('adverbio', 'boolean'),
                Field('adjetivo', 'boolean'),
                # verbo
                Field('verbo', 'boolean'),
                Field('verbo_irregular', 'boolean'),
                Field('participio2', 'string'),
                Field('reflexivo', 'boolean'),
                Field('sein', 'boolean'),
                Field('presente_1'),
                Field('presente_2'),
                Field('presente_3'),
                Field('presente_1_p'),
                Field('presente_2_p'),
                Field('presente_3_p'),
                Field('pasado_1'),
                Field('pasado_2'),
                Field('pasado_3'),
                Field('pasado_1_p'),
                Field('pasado_2_p'),
                Field('pasado_3_p'),
                Field('anadir_glosario', 'boolean'),
                Field('glosario', 'list:reference glosarios')
                )

db.define_table('fuentes',
                Field('nombre', 'string')
                )

db.define_table('ejemplos',
                Field('ejemplo_de', 'text'),  # no puede estar vacio
                Field('ejemplo_es', 'text'),   # puede estar vacio
                Field('adverbio', 'boolean'),
                Field('verbo', 'boolean'),
                Field('adjetivo', 'boolean'),
                Field('sustantivo', 'boolean'),
                Field('preposicion', 'boolean'),
                Field('fuente', db.fuentes),
                Field('revisar','boolean')
                )
db.define_table('palabra_ejemplo',  # refereciada por los Id
                Field('palabra', db.palabras),   # no puede estar vacio
                Field('ejemplo', db.ejemplos))   # no puede estar vacio

## Tablas para los widget de autocompletar ##

db.define_table('autocompletar_palabra',
                Field('palabra')
                )

db.define_table('busqueda',
                 Field('buscar_palabra')
                 )

db.define_table('busqueda_front',
                 Field('buscar_palabra')
                 )

### Validacion glosario referece ###
#db.palabras.glosario.requires = IS_IN_DB(db,'glosarios.id',db.glosarios._format,multiple=True)


### Validaciones tabla glosario ###
#db.glosarios.nombre_glosario.requires = IS_NOT_IN_DB(db,'glosarios.nombre_glosario')

### Autocompletar palabra ###
#db.autocompletar_palabra.palabra.widget = SQLFORM.widgets.autocomplete(
  #   request, db.palabras.palabra, limitby=(0,10), min_length=1)

### Autocompletar busqueda ###
db.busqueda.buscar_palabra.widget = SQLFORM.widgets.autocomplete(
     request, db.palabras.palabra, limitby=(0,10), min_length=1)

### Autocompletar busqueda front ###
db.busqueda_front.buscar_palabra.widget = SQLFORM.widgets.autocomplete(
     request, db.palabras.palabra, limitby=(0,10), min_length=1)


### Validacion tabla palabras ###
#db.palabras.palabra.represent = lambda palabra: palabra.capitalize()
db.palabras.articulo.requires = IS_EMPTY_OR(IS_IN_SET(['Die', 'Der', 'Das'],zero=T('Elige uno'),
         error_message=T('Elige Die, Der o Das')))
#db.palabras.glosario.requires = IS_EMPTY_OR(IS_IN_DB(db, 'glosarios.id', '%(nombre_glosario)s'))


 
### WIDGET AUTOCOMPLETAR para la tabla fuentes ###
db.ejemplos.fuente.widget = SQLFORM.widgets.autocomplete(
     request, db.fuentes.nombre, id_field=db.fuentes.id, min_length=1)
db.fuentes.nombre.requires = IS_NOT_EMPTY()

### Validierung EJEMPLOS ###
db.ejemplos.ejemplo_de.requires = IS_NOT_EMPTY()
db.ejemplos.ejemplo_es.requires = IS_NOT_EMPTY()


### WIDGET AUTOCOMPLETAR para la tabla palabra_ejemplo ###
db.palabra_ejemplo.palabra.widget = SQLFORM.widgets.autocomplete(
     request, db.palabras.palabra, id_field=db.palabras.id, min_length=1)
db.palabra_ejemplo.ejemplo.widget = SQLFORM.widgets.autocomplete(
     request, db.ejemplos.ejemplo_de, id_field=db.ejemplos.id, min_length=1)

### Caja de busqueda de palabra administracion ###
form_busqueda_palabra_admin = SQLFORM(db.busqueda, formstyle='divs', _id="buscar_palabra_admin", submit_button='Enviar')
if form_busqueda_palabra_admin.accepts(request.vars, session, dbio=False): # metodo para validar las entradas del formulario, dbio=False no guarda en la bases de datos
    a = db(db.palabras.palabra==request.post_vars.buscar_palabra).select().first()
    if not a:
        redirect(URL('agregar_palabra', vars=dict(a=request.post_vars.buscar_palabra)))
        
    else:
        id_palabra = db(db.palabras.palabra==request.post_vars.buscar_palabra).select().first()
        redirect(URL('mostrar_palabra', args=id_palabra.id))
        
### Caja de busqueda de palabra la pagina principal ###
form_busqueda_palabra_front = SQLFORM(db.busqueda_front, formstyle='divs', _id="buscar_palabra_front", submit_button='Buscar')
if form_busqueda_palabra_front.accepts(request.vars, session, dbio=False): # metodo para validar las entradas del formulario, dbio=False no guarda en la bases de datos
    
    a = db(db.palabras.palabra==request.post_vars.buscar_palabra).select().first()
    if not a:
        session.flash = "Palabra no existe"
    else:
        id_palabra = db(db.palabras.palabra==request.post_vars.buscar_palabra).select().first()
        redirect(URL('default', 'mostrar', args=id_palabra.id, vars=dict(b=request.post_vars.buscar_palabra)))


### buscar e imprimir glosarios ###
buscar_glosarios = db().select(db.glosarios.nombre_glosario)

### Contar los registro de las tablas principales ###
total_palabras = db(db.palabras.id > 0).count()
total_ejemplos = db(db.ejemplos.id > 0).count()

####################################################################
#                    Codigo para pegar y copiar
#
# db.palabras.palabra.requires = IS_NOT_IN_DB(db,'palabras.palabra') << Devuelve un error si el campo se encuentra en la DB o si estas vacio. tambien se le debe colocar el  unique=True  >> 
# db.palabras.palabra.requires = IS_NOT_EMPTY() << no es necesario si se usa este validador >>
# db.palabra_ejemplo.ejemplo.requires = IS_IN_DB(db, 'ejemplo.id', '%(ejemplo)s') << este validador crea una lista >>
# db.palabras.articulo.requires = IS_IN_SET(['Die', 'Der', 'Das'],zero=T('Elige uno'), error_message=T('Elige Die, Der o Das'))
# db.busqueda.buscar_palabra.widget = SQLFORM.widgets.autocomplete(request, db.palabras.palabra, limitby=(0,10), min_length=2)      
# db.busqueda.buscar_palabra.widget = SQLFORM.widgets.autocomplete(request, db.palabras.palabra, id_field=db.palabras.id, min_length=1)
#
#
#
#
#
#
#
#
#
#
#
#
#

