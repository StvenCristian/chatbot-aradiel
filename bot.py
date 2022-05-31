from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
class BotAradiel():
    contexto=None
    pregunta=None
    def __init__(self,contexto,pregunta):
        the_model = 'mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es'
        self.tokenizer = AutoTokenizer.from_pretrained(the_model, do_lower_case=False)
        self.model = AutoModelForQuestionAnswering.from_pretrained(the_model)
        self.contexto=contexto
        self.pregunta = pregunta

    def ResponderPregunta(self):
        nlp = pipeline('question-answering', model=self.model, tokenizer=self.tokenizer)
        salida = nlp({'question': self.pregunta, 'context': self.contexto})
        return salida
