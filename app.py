from flask import Flask, render_template, request, url_for, redirect
import os

app = Flask(__name__)

COMBOS = [
    {"id":1, "name":"Ceviche Clásico del Puerto", "type":"marino", "plate":"Ceviche clásico con camote y choclo", "drink":"Limonada", "img":"ceviche.png", "price":"S/25"},
    {"id":2, "name":"Chicharrón Crocante Marino", "type":"marino", "plate":"Chicharrón de pescado con salsa criolla", "drink":"Cerveza", "img":"chicharron.png", "price":"S/28"},
    {"id":3, "name":"Arroz con Mariscos Nikkei", "type":"marino", "plate":"Arroz salteado con mariscos y toque nikkei", "drink":"Maracuyá", "img":"arroz_mariscos.png", "price":"S/32"},
    {"id":4, "name":"Causa Acevichada", "type":"marino", "plate":"Causa rellena con pescado acevichado", "drink":"Chicha Morada", "img":"ceviche.png", "price":"S/22"},
    {"id":5, "name":"Lomo Saltado Premium", "type":"criollo", "plate":"Lomo saltado con papas crocantes", "drink":"Pisco Sour", "img":"lomo_saltado.png", "price":"S/35"},
    {"id":6, "name":"Ají de Gallina Cremoso", "type":"criollo", "plate":"Ají de gallina con arroz blanco y papa", "drink":"Limonada", "img":"ajidegallina.png", "price":"S/24"},
    {"id":7, "name":"Combo Universitario Power", "type":"universitario", "plate":"Arroz con pollo + bebida", "drink":"Gaseosa", "img":"combo_familiar.png", "price":"S/12"},
    {"id":8, "name":"Combo Pareja Marina", "type":"pareja", "plate":"Ceviche + Chicharrón para compartir", "drink":"Pisco Sour", "img":"ceviche.png", "price":"S/55"},
    {"id":9, "name":"Combo Familiar Mixto", "type":"familiar", "plate":"Arroz con mariscos + Lomo + guarniciones", "drink":"Cerveza 6 pack", "img":"combo_familiar.png", "price":"S/120"},
    {"id":10, "name":"Festín Criollo", "type":"familiar", "plate":"Seco, tacu tacu y anticuchos", "drink":"Old Times", "img":"combo_familiar.png", "price":"S/140"}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recomendacion', methods=['POST'])
def recomendacion():
    sabor = request.form.get('sabor','').lower()
    proteina = request.form.get('proteina','').lower()
    bebida = request.form.get('bebida','').lower()
    compania = request.form.get('compania','').lower()
    momento = request.form.get('momento','').lower()
    presupuesto = request.form.get('presupuesto','').lower()

    scores = {c['id']:0 for c in COMBOS}

    for c in COMBOS:
        if sabor == 'picante' and 'ceviche' in c['name'].lower():
            scores[c['id']] += 2
        if sabor == 'crocante' and 'chicharr' in c['name'].lower():
            scores[c['id']] += 2
        if proteina in ['pescado','mariscos'] and c['type']=='marino':
            scores[c['id']] += 2
        if proteina in ['carne','pollo'] and c['type']=='criollo':
            scores[c['id']] += 2
        if compania in ['familia'] and c['type']=='familiar':
            scores[c['id']] += 3
        if compania in ['pareja'] and c['type']=='pareja':
            scores[c['id']] += 3
        if compania in ['universidad','universitario'] and c['type']=='universitario':
            scores[c['id']] += 3
        if presupuesto in ['económico','universitario'] and int(''.join(filter(str.isdigit,c['price']))) < 30:
            scores[c['id']] += 2
        if presupuesto in ['premium','festivo'] and int(''.join(filter(str.isdigit,c['price']))) >= 30:
            scores[c['id']] += 2
        if bebida in c['drink'].lower():
            scores[c['id']] += 1

    best_id = max(scores, key=lambda k: scores[k])
    best = next((c for c in COMBOS if c['id']==best_id), COMBOS[0])

    return render_template('resultado.html', combo=best)

@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        telefono = request.form.get('telefono')
        mensaje = request.form.get('mensaje')
        return render_template('contact_ok.html', nombre=nombre)
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
