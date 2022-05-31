import pymysql
import  entity as entidad

class Database():

    def __init__(self):
        self.connection=pymysql.connect(
            host='HOST',
            user='USER',
            password='PASSWORD',
            db='DATABASE'
        )
        self.cursor=self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        self.connection.close()

    def FiltrarContexto(self,categoria):
        ListaContexto=[]
        sql = ' select c.id_contexto,c.detalle_contexto,c.id_categoria, a.descripcion from contexto c left join categoria a'
        sql += ' on c.id_categoria=a.id_categoria'
        if categoria != 0:
            sql += f' and c.id_categoria={categoria}'
        try:
            self.cursor.execute(sql)
            respuesta=self.cursor.fetchall()
            for item in respuesta:
                itemContexto=entidad.Contexto()
                itemContexto.IdContexto=item[0]
                itemContexto.DetalleContexto=item[1]
                itemContexto.IdCategoria=item[2]
                itemContexto.DetalleCategoria = item[3]
                ListaContexto.append(itemContexto)
            return ListaContexto
        except Exception as e:
            print("\nError ejecutando la consulta "+ sql +"\error:"+str(e))

    def FiltrarRespuesta(self,id_atencion):
        ListaRespuesta=[]
        sql = ' select id_respuesta,detalle_respuesta,fecha_respuesta,hora_respuesta,tasa_prediccion,id_atencion from respuesta '
        if id_atencion != "":
            sql += " where id_atencion='{}'".format(id_atencion)
        try:
            self.cursor.execute(sql)
            respuesta=self.cursor.fetchall()
            for item in respuesta:
                itemRespuesta=entidad.Respuesta()
                itemRespuesta.IdRespuesta=item[0]
                itemRespuesta.DetalleRespuesta=item[1]
                itemRespuesta.FechaRespuesta=item[2]
                itemRespuesta.HoraRespuesta = item[3]
                itemRespuesta.TasaPrediccion = item[4]
                itemRespuesta.IdAtencion = item[5]
                ListaRespuesta.append(itemRespuesta)
            return ListaRespuesta
        except Exception as e:
            print("\nError ejecutando la consulta "+ sql)
            return None

    def RegistrarCategoria(self,categoria):
        try:
            sql = 'insert into categoria(descripcion,fecha_creacion) '
            sql += "values('{}',now())".format(categoria.Descripcion)
            self.cursor.execute(sql)
        except Exception as e:
            print("\nError ejecutando la consulta " + sql)

    def RegistrarContexto(self,contexto):
        print("Registrando contexto..")
        try:
            sql = 'insert into contexto(detalle_contexto,id_categoria,fecha_creacion) '
            sql +="values('{}',{},now())".format(contexto.DetalleContexto,contexto.IdCategoria)
            print(sql)
            self.cursor.execute(sql)
        except Exception as e:
            print("\nError ejecutando la consulta " + sql + "\error:" + str(e))

    def RegistrarRespuesta(self,respuesta):
        try:
            sql = 'insert into respuesta(detalle_respuesta,fecha_respuesta,hora_respuesta,tasa_prediccion,id_atencion) '
            sql +="values('{}',curdate(),curtime(),{},'{}')".format(respuesta.DetalleRespuesta,respuesta.TasaPrediccion,respuesta.IdAtencion)
            self.cursor.execute(sql)
        except Exception as e:
            print("\nError ejecutando la consulta " + sql)

    def RegistrarAtencion(self,atencion):
        print("ejecutando consulta")
        try:
            sql = 'insert into atencion(id_atencion,fecha_atencion,hora_inicio) '
            sql +=" values('{}','{}','{}')".format(atencion.IdAtencion,atencion.FechaAtencion,atencion.HoraInicio)
            print(sql)
            self.cursor.execute(sql)
        except Exception as e:
            print("\nError ejecutando la consulta " + sql)

    def ActualizarAtencion(self,atencion):
        try:
            sql = ' update atencion '
            sql += " set hora_fin='{}', calificacion='{}', tasa_acierto={}".format(atencion.HoraFin,atencion.Calificacion,atencion.TasaAcierto)
            sql += " where id_atencion='{}'".format(atencion.IdAtencion)
            print(sql)
            self.cursor.execute(sql)
        except Exception as e:
            print("\nError ejecutando la consulta " + sql +"\Error:"+e)

    def FiltrarCategoria(self):
        ListaCategoria=[]
        sql = ' select id_categoria,descripcion,fecha_creacion from categoria'
        try:
            self.cursor.execute(sql)
            respuesta=self.cursor.fetchall()
            for item in respuesta:
                itemCategoria=entidad.Categoria()
                itemCategoria.IdCategoria=item[0]
                itemCategoria.Descripcion=item[1]
                itemCategoria.Fecha_Creacion=str(item[2])
                ListaCategoria.append(itemCategoria)
            return ListaCategoria
        except Exception as e:
            print("\nError ejecutando la consulta "+ sql)

    def FiltrarAtencion(self):
        ListaAtencion=[]
        sql = ' select id_atencion,fecha_atencion,hora_inicio,hora_fin,calificacion,tasa_acierto from atencion'
        try:
            self.cursor.execute(sql)
            respuesta=self.cursor.fetchall()
            for item in respuesta:
                itemAtencion=entidad.Atencion()
                itemAtencion.IdAtencion=item[0]
                itemAtencion.FechaAtencion=str(item[1])
                itemAtencion.HoraInicio=str(item[2])
                itemAtencion.HoraFin = str(item[3])
                itemAtencion.Calificacion = item[4]
                itemAtencion.TasaAcierto = str(item[5])
                ListaAtencion.append(itemAtencion)
            return ListaAtencion
        except Exception as e:
            print("\nError ejecutando la consulta "+ sql + "\Error:"+str(e))
            return None

