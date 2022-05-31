class Categoria:
    IdCategoria=None
    Descripcion = None
    Fecha_Creacion = None
    def __init__(self):
        self.IdCategoria=0
        self.Descripcion=""
        self.Fecha_Creacion=""

class Contexto:
    IdContexto = None
    DetalleContexto = None
    IdCategoria = None
    FechaCreacion=None
    DetalleCategoria=None
    def __init__(self):
        self.IdContexto = 0
        self.DetalleContexto = ""
        self.IdCategoria = 0
        self.FechaCreacion=""
        self.DetalleCategoria=""



class Respuesta:
    IdRespuesta = None
    DetalleRespuesta = None
    FechaRespuesta = None
    HoraRespuesta = None
    TasaPrediccion=None
    IdContexto=None
    IdAtencion=None
    def __init__(self):
        self.IdRespuesta = 0
        self.DetalleRespuesta = ""
        self.FechaRespuesta=""
        self.HoraRespuesta=""
        self.TasaPrediccion = 0
        self.IdContexto = 0
        self.IdAtencion = 0

class Atencion():
    IdAtencion = None
    FechaAtencion = None
    HoraInicio = None
    HoraFin = None
    Calificacion = None
    TasaAcierto = None
    def __init__(self):
        self.IdAtencion = 0
        self.FechaAtencion = ""
        self.HoraInicio = ""
        self.HoraFin = ""
        self.Calificacion = 0
        self.TasaAcierto = 0