from decimal import Decimal
import database as db
import bot as _bot
import entity
from datetime import datetime
import entity as entidad

def RegistrarCategoria(categoria):
    conex = db.Database()
    try:
        conex.RegistrarCategoria(categoria)
        conex.commit()
        return True
    except:
        conex.rollback()
        return False
    finally:
        conex.close()

def ObtenerListaAtencion():
    conex = db.Database()
    try:
        lista_atencion=conex.FiltrarAtencion()
        return lista_atencion
    except:
        return None
    finally:
        conex.close()

def RegistrarContexto(contexto):
    conex = db.Database()
    try:
        conex.RegistrarContexto(contexto)
        conex.commit()
        return True
    except:
        conex.rollback()
        return False
    finally:
        conex.close()

def ObtenerFullContexto(lista_contexto):
    contexto=""
    try:
        for item in lista_contexto:
            contexto=contexto + ". " + item.DetalleContexto
        return contexto
    except:
        return contexto
def ObtenerCategorias():
    conex = db.Database()
    lista_categorias = []
    try:
        lista_categorias = conex.FiltrarCategoria()
        return lista_categorias
    except:
        return lista_categorias
    finally:
        conex.close()

def ObtenerContextos():
    conex = db.Database()
    lista_contextos = []
    try:
        lista_contextos = conex.FiltrarContexto(0)
        return lista_contextos
    except:
        return lista_contextos
    finally:
        conex.close()

def ObtenerRespuesta(pregunta,categoria,id_atencion):
    conex = db.Database()
    try:

        lista_contexto = conex.FiltrarContexto(categoria)
        contexto=ObtenerFullContexto(lista_contexto)
        if contexto=="":
            return "No se pudo encontrar contexto la categoria ingresada"
        bot=_bot.BotAradiel(contexto,pregunta)
        salida=bot.ResponderPregunta()
        respuesta=entity.Respuesta()
        respuesta.DetalleRespuesta=salida['answer']
        respuesta.TasaPrediccion = round(Decimal(str(salida['score'])), 2)
        if respuesta.TasaPrediccion < 0.01:
            respuesta.DetalleRespuesta = "Ahora mismo desconozco la respuesta a tu pregunta"
        respuesta.TasaPrediccion=str(respuesta.TasaPrediccion)
        respuesta.IdAtencion=id_atencion
        conex.RegistrarRespuesta(respuesta)
        conex.commit()
        return respuesta
    except:
        print("error obteniendo respuesta")
        conex.rollback()
        return None
    finally:
        conex.close()

def GenerarAtencion():
    conex = db.Database()
    try:

        atencion=entidad.Atencion()
        print(atencion.FechaAtencion)
        print(datetime.today().strftime('%Y-%m-%d'))
        atencion.FechaAtencion=datetime.today().strftime('%Y-%m-%d')
        atencion.HoraInicio = datetime.today().strftime('%H:%M:%S')
        atencion.IdAtencion=atencion.FechaAtencion.replace("-", "") + atencion.HoraInicio.replace(":", "")
        conex.RegistrarAtencion(atencion)
        conex.commit()
        return atencion
    except Exception as ex:
        print("Error generando atencion \n"+ex)
        conex.rollback()
        return None
    finally:
        conex.close()

def FinalizarAtencion(id_atencion,calificacion):
    conex = db.Database()
    try:

        lista_respuesta=conex.FiltrarRespuesta(id_atencion)

        contador= len(lista_respuesta)
        print(contador)
        suma=0
        for item in lista_respuesta:
            suma=suma+ item.TasaPrediccion
        if(contador!=0):
            tasa_promedio = suma / contador
        else:
            tasa_promedio = 0
        atencion=entidad.Atencion()
        atencion.IdAtencion=id_atencion
        atencion.HoraFin=datetime.today().strftime('%H:%M:%S')
        atencion.TasaAcierto=tasa_promedio
        atencion.Calificacion=calificacion
        print("Iniciando actualizacion")
        conex.ActualizarAtencion(atencion)
        print("finalizando actualizacion")
        conex.commit()
        return True
    except Exception as ex:
        print("Error finalizando atencion\nError:"+ex)
        conex.rollback()
        return None
    finally:
        conex.close()