# coding: utf8
# intente algo como
def index():
    """
    Pagina principal de la administracion
    form = SQLFORM(db.busqueda, formstyle='divs', _id="buscar_palabra_admin", submit_button='Enviar')
    if form.accepts(request.vars, session, dbio=False): # metodo para validar las entradas del formulario, dbio=False no guarda en la bases de datos
        a = db(db.palabras.palabra==request.post_vars.buscar_palabra).select()
        if not a:
            session.flash = 'Ingresa nueva palabra'
            redirect(URL('agregar_palabra', args=request.post_vars.buscar_palabra))
            
        else:
            id_palabra = db(db.palabras.palabra==request.post_vars.buscar_palabra).select().first()
            redirect(URL('mostrar_palabra', args=id_palabra.id))
    """
    
           
           
    ejemplos = db((db.palabras.id==db.palabra_ejemplo.palabra)&(db.ejemplos.id==db.palabra_ejemplo.ejemplo)) # asi se igualan las tablas para las relaciones muchos a muchos
    return dict(ejemplos=ejemplos) # llama a la vista con el nombre de la funcion las variables
        
def agregar_palabra():
    """
    Se agregan  palabras y se muestran los ultimos 10 registros insertados con los cuales
    se pueden hacer distintas operaciones
    """
    if request.vars.a=='':
        session.flash = 'Intenta ingresar una nueva palabra en la busqueda'
        redirect(URL('index'))
    else: 
        db.palabras.palabra.default = request.vars.a
    db.palabras.palabra.requires = IS_NOT_IN_DB(db,'palabras.palabra') # Validacion para  la palabra que se inserte no puede estar ya en la DB
    agregar = SQLFORM(db.palabras, formstyle="divs", _id="form-agregar", submit_button="Enviar" , _autocomplete="off") # se genera el formulario para la tabla palabras
    if agregar.accepts(request.vars, session): #metodo para validar las entradas del formulario
       redirect(URL('buscar_ejemplos', vars=dict(a=request.post_vars.palabra)))
       #response.flash = 'Registro insertado' # mensajes del sistema
    elif agregar.errors:  # Metodo usado para cuando se producen errores
       response.flash = 'Hay un error'
    contador_ejemplo = db().select(db.palabra_ejemplo.ALL) # selecionar todos los registro de la tabla palabra_ejemplo para luego contarlos
    consulta = db().select(db.palabras.ALL, orderby=~db.palabras.id , limitby=(0,15)) # muestra los 10 ultimos registros insertados
    contador = db(db.palabras.id > 0).count() # cuenta cuantos registros hay en la DB
    return dict(agregar=agregar, consulta=consulta, contador=contador, contador_ejemplo=contador_ejemplo)
    
def buscar_ejemplos():
    return dict()
    
def buscar_ejemplos2():
    id = db(db.palabras.palabra==request.vars.b).select().first()
    buscar = db(db.ejemplos.ejemplo_de.contains(request.vars.b)).select()
    return dict(buscar=buscar, id=id)


def agregar_ejemplo():
    """
    Se agregan los ejemplos y se muestran los ultimos 10 registros insertados con los cuales
    se pueden hacer distintas operaciones
    """
    agregar_ejemplo = SQLFORM(db.ejemplos, formstyle="divs", _id="form-ejemplo", labels={'ejemplo_de':'', 'ejemplo_es':''} )
    if agregar_ejemplo.accepts(request.vars, session):
        response.flash = 'Ejemplo agregado'
        redirect(URL('agregar_ejemplo'))
    elif agregar_ejemplo.errors:
        response.flash="Hay algun error"
    nombre_fuente = db().select(db.fuentes.ALL)
    contador_palabra = db().select(db.palabra_ejemplo.ALL) # selecionar todos los registro de la tabla palabra_ejemplo para luego contarlos
    consulta_ejemplos = db().select(db.ejemplos.ALL, orderby=~db.ejemplos.id, limitby=(0,9)) # muestra los 10 ultimos registros insertados
    contador2 = db(db.ejemplos.id > 0).count() # cuenta cuantos registros hay en la DB
    ejemplos = db((db.palabras.id==db.palabra_ejemplo.palabra)&(db.ejemplos.id==db.palabra_ejemplo.ejemplo))
    #palabras = db(db.palabra_ejemplo.palabra==db.palabras.id)
    return dict(ejemplos=ejemplos, consulta_ejemplos=consulta_ejemplos, agregar_ejemplo=agregar_ejemplo, contador2=contador2, contador_palabra=contador_palabra, nombre_fuente=nombre_fuente)
    
def agregar_fuente():
    agregar_fuente = SQLFORM(db.fuentes, formstyle="divs", _id="form-fuentes" )
    if agregar_fuente.accepts(request.vars, session):
       response.flash = 'Fuente insertado'
    elif agregar_fuente.errors:
       response.flash = 'Hay un error'
    consulta = db().select(db.fuentes.ALL, orderby=~db.fuentes.id , limitby=(0,9)) # muestra los 10 ultimos registros insertados
    contador = db(db.fuentes.id > 0).count() # cuenta cuantos registros hay en la DB
    return dict(agregar_fuente=agregar_fuente, consulta=consulta, contador=contador)
    
def agregar_glosario():
    agregar_glosario = SQLFORM(db.glosarios, formstyle="divs", _id="form-glsoario" )
    if agregar_glosario.accepts(request.vars, session):
       response.flash = 'Fuente insertado'
    elif agregar_glosario.errors:
       response.flash = 'Hay un error'
    consulta = db().select(db.glosarios.ALL, orderby=~db.glosarios.id , limitby=(0,9)) # muestra los 10 ultimos registros insertados
    contador = db(db.glosarios.id > 0).count() # cuenta cuantos registros hay en la DB
    return dict(agregar_glosario=agregar_glosario, consulta=consulta, contador=contador)
    
def agregar_palabra_grid():
    """
    El grid propocionado por web2py, utilizado para administracion
    """
    agregar = SQLFORM.grid(db.worte, _class="table margin-top table-striped")
    return dict(agregar=agregar)

def borrar_palabra():# 
    """
    simplemente carga la vista para ejecutar el Modal
    """
    return dict()

def borrar_palabra2():
    """
    Es la accion que borra la palabra y redirecciona al index de admin
    """
    db(db.palabras.id == request.raw_args).delete() # borra la palabra de la DB
    session.flash='Registro borrado' # se usa cuando se redirecciona a otra, y se quiere mostrar el mensaje del sistema
    redirect(URL('agregar_palabra'))
 
def borrar_ejemplo(): 
    """
    simplemente carga la vista para ejecutar el Modal
    """
    return dict()

def borrar_ejemplo2():
    """
    realiza la accion de borrar y redirecciona
    """
    db(db.ejemplos.id == request.raw_args).delete() # borra la palabra de la DB
    session.flash='Ejemplo borrado'
    redirect(URL('agregar_ejemplo'))
    
def borrar_fuente():# 
    """
    simplemente carga la vista para ejecutar el Modal
    """
    return dict()
    
def borrar_fuente2():
    """
    realiza la accion de borrar y redirecciona
    """
    db(db.fuentes.id == request.args(0)).delete() # borra la palabra de la DB
    session.flash='Fuente borrada'
    redirect(URL('agregar_fuente'))

def editar_palabra():
    """
    Se carga el formulario para editar el registro
    """
    record = db.palabras(request.args(0)) # Seleciona el registro de la DB con el primer argumentro pasado
    agregar = SQLFORM(db.palabras, record, formstyle='divs', _class='form-inline wellparley', _id='form-editar') # formulario para actualizar hay que pasarle el registro que se quiere actualizar
    if agregar.accepts(request.vars, session):
       session.flash='Palabra editada' 
       redirect(URL('agregar_palabra'))
    elif agregar.errors:
     response.flash = 'El formulario tiene errores'
    return dict(agregar=agregar)
    

    
def editar_ejemplo():
    """
    carga el formulario para la edicion de el ejemplo, valida y redirecciona
    """
    record = db.ejemplos(request.raw_args) # Seleciona el registro de la DB con el primer argumentro pasado
    form = SQLFORM(db.ejemplos, record, formstyle='divs', _class='form-inline wellparley', _id='form-editar-ejemplo')
    if form.accepts(request.vars):
       session.flash='Ejemplo editado' 
       redirect(URL('agregar_ejemplo'))
    elif form.errors:
       response.flash = 'El formulario tiene errores'
    return dict(form=form)
    
def editar_fuente():
    """
    carga el formulario para la edicion de el ejemplo, valida y redirecciona
    """
    record = db.fuentes(request.args(0)) # Seleciona el registro de la DB con el primer argumentro pasado
    form = SQLFORM(db.fuentes, record, formstyle='divs', _class='form-inline wellparley', _id='form-editar-fuente')
    if form.accepts(request.vars):
       session.flash='Fuente editada' 
       redirect(URL('agregar_fuente'))
    elif form.errors:
       response.flash = 'form has errors'
    return dict(form=form)
    
def relacionar_ejemplo():
    """
    Recibe el id de la palabra para guardarlo en
    DB junto al ejemplo a relacionar, quiere decir que tengo que cargar el un formulario
    con los campos de la tabla ejemplo, meter las id en variables y luego guardarlas en las tablas
    correspondiente
    """
    id_palabra = request.raw_args # Mete en una variable el valor de request.args(0), no es necesario
    palabra = db(db.palabras.id==id_palabra).select().first() # selecciona el primer registro que se igual al id de la palabra
    form = SQLFORM(db.ejemplos, labels={'ejemplo_de':'', 'ejemplo_es':''}) # para ingresar en la db debe tener el metodo form.accepts
    if form.accepts(request.vars, session):
        id_ejemplo = db(db.ejemplos.ejemplo_de==request.vars.ejemplo_de).select().first() # mete la consulta en una variable
        db.palabra_ejemplo.insert(palabra=id_palabra, ejemplo=id_ejemplo.id) # inserta en la DB los id de los registro selecionados, estos es para las relaciones muchos a muschos
        session.flash = 'Ejemplo Relacionado'
        redirect(URL('agregar_palabra'))
    elif form.errors:
        response.flash = 'Mira otra vez'
    return dict(palabra=palabra, form=form,)
    
def relacionar_palabra(): #Redisenar 
    """
    Recibe el id de el ejemplo para guardarlo en
    DB junto a la palabra a relacionar, quiere decir que tengo que cargar el un formulario
    con los campos de la tabla palabra, meter las id en variables y luego guardarlas en las tablas
    correspondiente *********importante cuando se relacione la palabra hay que traer todos los campos de ingresar palabra cuando la palabra no se encuentra en DB
    *********** redisenar no sirve este codigo
    """
    id_ejemplo = request.args(0)
    #form=FORM('Palabra:',
              #INPUT(_name='palabra', requires=IS_NOT_EMPTY()),
              #INPUT(_type='submit'))
    ejemplo = db(db.ejemplos.id==id_ejemplo).select().first()
    form = SQLFORM(db.autocompletar_palabra, _autocomplete="off")
    if form.accepts(request.vars, session, dbio=False):
        consulta = db(db.palabras.palabra==request.vars.palabra).select().first() # se busca si la palabra ya esta en la DB
        #igualar = db((db.palabras.id==db.palabra_ejemplo.palabra)&(db.ejemplos.id==db.palabra_ejemplo.ejemplo))
        #selecionar = igualar(db.palabras.palabra==request.vars.palabra).select(db.palabra_ejemplo.ALL)
        #consulta = selecionar
        if consulta: # si la palabra esta ya en la db, solo hay que ingresar ambos id de la palabra y el ejemplo en la tabla palabra_ejemplo
            consulta_id_palabra = db((db.palabra_ejemplo.palabra==consulta.id)&(db.palabra_ejemplo.ejemplo==request.args(0))).select().first() # consulta si el id de la palabra ya se encuentra en la db
            if consulta_id_palabra:
                session.flash="Palabra ya relacionada con el ejemplo"
                redirect(URL('admin', 'agregar_ejemplo'))
            else:
                db.palabra_ejemplo.insert(palabra=consulta.id, ejemplo=request.args(0))
                session.flash = 'Palabra relacionada'
                redirect(URL('admin', 'agregar_ejemplo'))
        else:
            db.palabras.insert(palabra=request.vars.palabra)
            ultimo_registro = db(db.palabras.id > 0).select().last()
            db.palabra_ejemplo.insert(palabra=ultimo_registro.id, ejemplo=request.args(0))
            session.flash = 'Palabra relacionada y agregada'
            redirect(URL('admin', 'agregar_ejemplo'))
            
    elif form.errors:
        response.flash = 'Mira otra vez'
    return dict(ejemplo=ejemplo, form=form)    
    
def relacionar():
    a = request.post_vars.relacionar 
    for i in a:
        db.palabra_ejemplo.insert(palabra=int(request.post_vars.id_palabra), ejemplo=i)
    db((db.palabra_ejemplo.ejemplo==0) | (db.palabra_ejemplo.palabra==None)).delete()
    session.flash = 'Ejemplos relacionados'
    redirect(URL('index'))
    
def mostrar_palabra():
    record = db.palabras(request.raw_args) # Seleciona el registro de la DB con el primer argumentro pasado
    form = SQLFORM(db.palabras, record, formstyle='divs', _class='form-inline wellparley', _id='form-editar') # formulario para actualizar hay que pasarle el registro que se quiere actualizar
    if form.accepts(request.vars, session):
       response.flash='Palabra editada' 
       #redirect(URL('agregar_palabra'))
    elif form.errors:
        response.flash = 'El formulario tiene errores'
    igualar = db((db.palabras.id==db.palabra_ejemplo.palabra)&(db.ejemplos.id==db.palabra_ejemplo.ejemplo))
    palabra = igualar(db.palabras.id==request.raw_args).select(db.ejemplos.ALL)
    return dict(palabra=palabra, form=form, record=record)
    
   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
