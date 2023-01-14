from flask import Flask , render_template , request , jsonify
import prediction

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# api ouvindo solicitações POST e prevendo sentimentos
@app.route('/predict' , methods = ['POST'])
def predict():

    response = ""
    review = request.json.get('customer_review')
    if not review:
        response = {'status' : 'error',
                    'message' : 'Avaliação em Branco'}
    
    else:

        # chamando o método predict do módulo de previsão.py
        sentiment , path = prediction.predict(review)
        response = {'status' : 'success',
                    'message' : 'Got it',
                    'sentiment' : sentiment,
                    'path' : path}

    return jsonify(response)


# Criando uma API para salvar a avaliação. O usuário clica no botão Salvar
@app.route('/save-entry' , methods = ['POST'])
def save():

    # extraindo data , nome do produto , avaliação e sentimento associado aos dados JSON
    date = request.json.get('dados')
    product = request.json.get('produto')
    review = request.json.get('revisao')
    sentiment = request.json.get('emocao')

    # criando uma variável final separada por vírgulas
    data_entry = date + "," + product + "," + review + "," + sentiment

    # abra o arquivo no modo 'append'
    data_entry = open("./static/assets/data_files/updated_product_dataset.csv","a")
    data_entry.write(data_entry+"\n")
    # Registre os dados no arquivo

    # retorne uma mensagem de sucesso
    return jsonify({'status' : 'success' , 
                    'message' : 'Dados Registrados'})


if __name__  ==  "__main__":
    app.run(debug = True)