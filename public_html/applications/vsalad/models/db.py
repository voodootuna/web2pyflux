# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################
from time import time as now
## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    #
    #db = DAL('sqlite://storage.sqlite')
    db = DAL('mysql://vtuna:CP3JvoSZKd@vtuna.mysql.fluxflex.com:3306/vtuna')

else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore/')
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


db.define_table(
    auth.settings.table_user_name,
    Field('username', length=17,unique=False),
    Field('email', length=128, default='', unique=True), 
    Field('password', 'password', length=512,    # required
          readable=False, label='Password'),      
    Field('joindate','double',default=now, writable=False, readable=False), 
    Field('karma','integer',writable=False, readable=False),
    Field('registration_key', length=512,
            writable=False, readable=False, default=''),
        Field('reset_password_key', length=512,
            writable=False, readable=False, default=''),
        Field('registration_id', length=512,
            writable=False, readable=False, default='')) 
 
custom_auth_table = db[auth.settings.table_user_name]
custom_auth_table.password.requires = [IS_NOT_EMPTY(),CRYPT()]
custom_auth_table.email.requires = [
    IS_EMAIL(error_message=auth.messages.invalid_email),
    IS_NOT_IN_DB(db, custom_auth_table.email),IS_NOT_EMPTY()]

auth.settings.table_user = custom_auth_table
## create all tables needed by auth if not custom tables
auth.define_tables(username=True)

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

db.define_table(
    'article',
    Field('title','string', length=100),
    Field('url', length=2048),
    Field('content','string', length=2048),
    Field('author', 'string'),
    Field('nsfw','boolean', default=False),
    Field('selftext', 'boolean', default=False),
    Field('score', 'integer', default=0),
    Field('comments','integer',default=0),
    Field('flagged','boolean', default=False),
    Field('category'),
    Field('created_on','datetime', default=request.now))
    
db.article.title.requires=IS_NOT_EMPTY()
    
db.define_table('category',
   Field('name'),
   Field('description'))

db.define_table('comments',
                Field('article', db.article),
                Field('parent_node','integer', default=0),
                Field('body'),
                Field('deleted','boolean'),
                Field('votes','integer',default=1),
                Field('author'),
                Field('created_on','datetime',default=request.now,readable=False,writable=False))   
                           
    
if len(db().select(db.article.ALL))==0:
   db.article.insert(title='TIL that in Harry Potter, the spell for world peace is "Ronus Paulus"', content='RON PAUL 2012',author='john', score="12")
   db.article.insert(title='I never read comments AMA ',content='totally serious guise',author='rob',  score="312")
   db.article.insert(title="Upvote to double NASA's annual budget ",content='signed the neckbeard virgin',author='pokemonster', score="162")
