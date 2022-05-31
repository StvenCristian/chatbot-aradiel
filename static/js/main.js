var _tblContexto
$( document ).ready(function() {
    console.log( "ready!" );
    $( "#btnRegistrarContexto" ).click(function() {
        console.log( "click registrar contexto!" );
        RegistrarContexto();
    });



    var RegistrarContexto= function (){
        var detalle_contexto=$('#txtContexto').val()
        var id_categoria=$('#ddlCategoria').val()
        if(detalle_contexto.length>250){
            alert("No se puede ingresar texto de mas de 250 caracteres :)")
            return
        }
        var datos={
            detalle_contexto:detalle_contexto,
            id_categoria:id_categoria
        }
        console.log(datos)
        var url="http://127.0.0.1:5000/api/contexto/registrar"
        $.ajax({
          type: "POST",
          url: url,
          contentType: "application/json; charset=utf-8",
          data: JSON.stringify(datos),
          success:  function(response) {
            if(response.success){
                alert("Se registró correctamente")
                CargarTablaContexto()
            }else {
                alert("ocurrio un error"+ response.message)
            }
          },
          error: function(){
              console.log("Error")
          }

        });
    }


    var CargarCategorias = function (){
        var url="http://127.0.0.1:5000/api/categorias/all"
        $.ajax({
          type: "GET",
          url: url,
          success:  function(response) {
            if(response.success){
                var resp=JSON.parse(response.obj)
                CargarComboCategorias(resp)
            }else {
                console.log("ocurrio un error")
            }

          },
          error: function(){
              console.log("Error")
          }
        });
    }
    var CargarComboCategorias= function (data){
        var html=""
        for(var i=0;i<data.length;i++){
            html="<option value='"+ data[i].IdCategoria +"'>"+data[i].Descripcion+"</option>"
            $("#ddlCategoria").append(html)
        }
    }
    var CargarTablaContexto=function (){
        var datos
        $.ajax ( {
            url: "http://127.0.0.1:5000/api/contexto/all",
            method: 'GET',
            success: function (data)
            {
                datos=JSON.parse(data.obj)
                if(_tblContexto!==undefined){
                    _tblContexto.destroy()
                }
                _tblContexto = $('#tblContexto').DataTable ( {
                        data:datos,
                        paging: true,
                        info: false,
                        columns: [
                            { "data": "IdContexto" },
                            { "data": "DetalleContexto" },
                            { "data": "DetalleCategoria" }
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
        });

    }

    CargarCategorias()
    CargarTablaContexto()
});