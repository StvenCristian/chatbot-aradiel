let saludos=['buenos dias','hola','buenas tardes','buenas noches','hey']
let despedidas=['adios','gracias','hasta pronto']
let saludoInicial="Bienvenido, Soy Aradiel y puedes consultarme cualquier tema relacionado a una tesis"
let despedida="Gracias espero haberte ayudado, Por favor no olvides de calificar mi atención"


$( document ).ready(function() {

    $( "#btnChatBot" ).click(function() {
        console.log( "click inicio bot!" );
        GenerarAtencion()
    });
    $( "#btnEnviarCalificacion" ).click(function() {
        console.log( "enviando calificacion!" );
        FinalizarAtencion()
    });

    //$('#myModal').modal('show')
    var GenerarAtencion= function (){
        console.log("generando atencion..")
        if(sessionStorage.getItem('id_atencion')!==null) return

        var url="http://127.0.0.1:5000/api/atencion/generar"
        $.ajax({
          type: "GET",
          url: url,
          success:  function(response) {
            if(response.success){
                console.log("se generó correctamente")
                var resp=JSON.parse(response.obj)
                sessionStorage.setItem('id_atencion', resp.IdAtencion);
            }else {
                console.log("ocurrio un error")
            }

          },
          error: function(){
              console.log("Error")
          }

        });
    }
    var FinalizarAtencion= function (){
        console.log("finalizando atencion..")
        //if(sessionStorage.getItem('id_atencion')!==null) return
        let id_atencion=sessionStorage.getItem('id_atencion')
        let calificacion=$("#ddlCalifica").val()
        let datos={
            id_atencion:id_atencion,
            calificacion:calificacion
        }
        var url="http://127.0.0.1:5000/api/atencion/finalizar"
        $.ajax({
          type: "POST",
          url: url,
          contentType: "application/json; charset=utf-8",
          data: JSON.stringify(datos),
          success:  function(response) {
            if(response.success){
                console.log("Finalizacion exitosa")
                sessionStorage.clear()
                $('#modalCalifica').modal('hide');
                $('.chatbox__support').removeClass('chatbox--active')
            }else {
                console.log("ocurrio un error")
            }

          },
          error: function(){
              console.log("Error")
          }

        });
    }
    const chatbox = new Chatbox();
    chatbox.display();
});

class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.messages = [];
    }

    display() {
        const {openButton, chatBox, sendButton} = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox))

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })
    }

    toggleState(chatbox) {
        this.state = !this.state;

        // show or hides the box
        if(this.state) {
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }

    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }

        let msg1 = { name: "User", message: text1 }
        this.messages.push(msg1);
        let msg = { name: "Aradiel", message: "escribiendo.." }
        this.messages.push(msg);
        this.updateChatText(chatbox,true)

        let id_atencion=sessionStorage.getItem('id_atencion')
        let pregunta= text1
        textField.value = ''
        if(saludos.indexOf(pregunta.toLowerCase().trim())!==-1){
            let msg2 = { name: "Aradiel", message: saludoInicial };
            this.messages.push(msg2);
            this.updateChatText(chatbox,false)
            return;
        }else if (despedidas.indexOf(pregunta.toLowerCase().trim())!==-1) {
            let msg2 = { name: "Aradiel", message: despedida };
            this.messages.push(msg2);
            this.updateChatText(chatbox,false)
            $('#modalCalifica').modal('show')
            return;
        }
        let id_categoria=0
        let datos={
            id_atencion:id_atencion,
            pregunta:pregunta,
            id_categoria:id_categoria
        }
        console.log(JSON.stringify(datos))
        fetch('http://127.0.0.1:5000/api/bot/preguntar', {
            method: 'POST',
            body: JSON.stringify(datos),
            headers: {
              'Content-Type': 'application/json'
            }
          })
          .then(r => r.json())
          .then(r => {
            let response=JSON.parse(r.obj)
            console.log(response)
            let msg2 = { name: "Aradiel", message: response.DetalleRespuesta };
            this.messages.push(msg2);
            this.updateChatText(chatbox,false)

        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox,false)
          });
    }

    updateChatText(chatbox,writing) {
        var html = '';
        if(!writing){
            this.messages=this.messages.filter( function (e){
                return e.message!=="escribiendo..";
            }
            );
        }
        this.messages.slice().reverse().forEach(function(item, index) {
            if (item.message === "escribiendo.." && !writing) {
                return;
            }
            if (item.name === "Aradiel")
            {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
            }
            else
            {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }
          });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }

    clearElement(){
        this.messages = [];
    }

}

