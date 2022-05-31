var _tblAtencion
$( document ).ready(function() {
    var ObtenerDatosAtencion=function (){
        var url="http://127.0.0.1:5000/api/atencion/all"
        $.ajax({
          type: "GET",
          url: url,
          success:  function(response) {
            if(response.success){
                var resp=JSON.parse(response.obj)
                CargarDatos(resp)
            }else {
                console.log("ocurrio un error")
            }

          },
          error: function(){
              console.log("Error")
          }
        });
    }
    var CargarDatos= function (datos){
        let totalSolicitudes=datos.length;
        let solicitudesAtendidas=0;
        let solicitudesProceso=0;
        let totalPrediccion=0;
        let tasaPrediccion=0;
        let totalCalificacion=0;
        let tasaCalificacion=0;
        let tasaTiempoPromedio=0;
        let totalTiempoPromedio=0;
        for(let i=0;i<datos.length;i++){
            if(datos[i].Calificacion!==null){
                solicitudesAtendidas++;
                totalPrediccion+=parseFloat(datos[i].TasaAcierto);
                totalCalificacion+=datos[i].Calificacion;
                let tiempo_inicio=datos[i].HoraInicio
                let tiempo_fin=datos[i].HoraFin
                let auxiliar=tiempo_inicio.split(":")
                tiempo_inicio=parseInt(auxiliar[0])*60+parseInt(auxiliar[1])
                auxiliar=tiempo_fin.split(":")
                tiempo_fin=parseInt(auxiliar[0])*60+parseInt(auxiliar[1])
                totalTiempoPromedio+= (tiempo_fin-tiempo_inicio)
            }else {
                datos[i].HoraFin=""
                datos[i].TasaAcierto=""
            }
        }
        tasaTiempoPromedio=totalTiempoPromedio/solicitudesAtendidas;
        tasaPrediccion=totalPrediccion/solicitudesAtendidas;
        tasaCalificacion=totalCalificacion/solicitudesAtendidas;
        solicitudesProceso=totalSolicitudes-solicitudesAtendidas;

        let html="";
        html+="<h4 class='card-title'>Total de solicitudes</h4>"
        html+="<p class='card-text' style='font-size: 60px'>"+ totalSolicitudes +"</p>"
        $("#bodyTotalSolicitudes").append(html)

        html="";
        html+="<h4 class='card-title'>Solicitudes Atendidas</h4>"
        html+="<p class='card-text' style='font-size: 60px'>"+ solicitudesAtendidas +"</p>"
        $("#bodyAtendidasSolicitudes").append(html)

        html="";
        html+="<h4 class='card-title'>Solicitudes Pendientes</h4>"
        html+="<p class='card-text' style='font-size: 60px'>"+ solicitudesProceso +"</p>"
        $("#bodyPendientesSolicitudes").append(html)

        html="";
        html+="<h4 class='card-title'>Tiempo promedio atencion (min.)</h4>"
        html+="<p class='card-text' style='font-size: 60px'>"+ tasaTiempoPromedio.toFixed(2) +"</p>"
        $("#bodyTiempoPromedio").append(html)

        html="";
        html+="<h4 class='card-title'>Tasa de Predicción</h4>"
        html+="<p class='card-text' style='font-size: 60px'>"+ tasaPrediccion.toFixed(2) +"</p>"
        $("#bodyPrediccion").append(html)

        html="";
        html+="<h4 class='card-title'>Tasa de Calificacion</h4>"
        html+="<p class='card-text' style='font-size: 60px'>"+ tasaCalificacion.toFixed(2) +"</p>"
        $("#bodyCalificacion").append(html)

        CargarTablaAtencion(datos)
    }
    var CargarTablaAtencion= function (datos){
        if(_tblAtencion!==undefined){
               _tblAtencion.destroy()
        }
        _tblAtencion = $('#tblAtencion').DataTable ( {
                        data:datos,
                        paging: true,
                        info: false,
                        columns: [
                            { "data": "IdAtencion" },
                            { "data": "FechaAtencion" },
                            { "data": "HoraInicio" },
                            { "data": "HoraFin" },
                            { "data": "Calificacion" },
                            { "data": "TasaAcierto" },
                        ],
                        language: {
                            "decimal": "",
                            "emptyTable": "No hay información",
                            "info": "Mostrando _START_ a _END_ de _TOTAL_ Entradas",
                            "infoEmpty": "Mostrando 0 to 0 of 0 Entradas",
                            "infoFiltered": "(Filtrado de _MAX_ total entradas)",
                            "infoPostFix": "",
                            "thousands": ",",
                            "lengthMenu": "Mostrar _MENU_ Entradas",
                            "loadingRecords": "Cargando...",
                            "processing": "Procesando...",
                            "search": "Buscar:",
                            "zeroRecords": "Sin resultados encontrados",
                            "paginate": {
                                "first": "Primero",
                                "last": "Ultimo",
                                "next": "Siguiente",
                                "previous": "Anterior"
                            }
                        }

                    });
    }
    ObtenerDatosAtencion();
});