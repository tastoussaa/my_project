from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)  # Autorise toutes les origines par défaut

# Route pour gérer l'importation et le nettoyage de données
@app.route('/upload', methods=['POST'])
def upload_file():
    # Vérifier si un fichier a été envoyé
    if 'dataset' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'})

    file = request.files['dataset']

    # Vérifier si un fichier a bien été sélectionné
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'})

    # Lire le fichier CSV ou Excel
    try:
        if file.filename.endswith('.csv'):
            data = pd.read_csv(file)
        elif file.filename.endswith('.xlsx'):
            data = pd.read_excel(file)
        else:
            return jsonify({'status': 'error', 'message': 'Invalid file format'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

    # Appliquer les étapes de nettoyage
    data = clean_data(data)

    # Obtenir des informations sur le dataset
    numRows = data.shape[0]
    numCols = data.shape[1]
    columns = list(data.columns)
    dtypes = list(data.dtypes.astype(str))  # Récupérer les types de données sous forme de chaîne

    # Convertir les données nettoyées en JSON pour les renvoyer au front-end
    cleaned_data = data.to_json(orient='records')

    return jsonify({
        'status': 'success',
        'cleaned_data': cleaned_data,
        'info': {
            'numRows': numRows,
            'numCols': numCols,
            'columns': columns,
            'dtypes': dtypes  # Ajoute les types de données ici
        }
    })


def clean_data(data):
    # 1. Suppression des doublons
    data = remove_duplicates(data)

    # 2. Détection et traitement des valeurs manquantes
    data = handle_missing_values(data)

    # 3. Correction des incohérences dans les types de données
    data = correct_data_types(data)

    # 4. Gestion des valeurs aberrantes
    data = remove_outliers(data)

    # 5. Standardisation des valeurs catégoriques
    data = standardize_categorical(data)

    return data

def remove_duplicates(data):
    return data.drop_duplicates()

def handle_missing_values(data):
    for col in data.select_dtypes(include=['float64', 'int64']).columns:
        data[col].fillna(data[col].mean(), inplace=True)
    
    for col in data.select_dtypes(include=['object']).columns:
        data[col].fillna(data[col].mode()[0], inplace=True)

    return data

def correct_data_types(data):
    for col in data.columns:
        try:
            data[col] = pd.to_datetime(data[col], errors='coerce')
        except:
            pass  # Ignore les colonnes qui ne peuvent pas être converties

    return data

def remove_outliers(data):
    for col in data.select_dtypes(include=['float64', 'int64']).columns:
        Q1 = data[col].quantile(0.25)
        Q3 = data[col].quantile(0.75)
        IQR = Q3 - Q1
        data = data[~((data[col] < (Q1 - 1.5 * IQR)) | (data[col] > (Q3 + 1.5 * IQR)))]

    return data

def standardize_categorical(data):
    for col in data.select_dtypes(include=['object']).columns:
        data[col] = data[col].str.lower().str.strip()
    return data


if __name__ == '__main__':
    app.run(debug=True)
