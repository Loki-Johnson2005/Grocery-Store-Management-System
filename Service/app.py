from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from model import complaint

@app.route('/complaints', methods=['POST'])
def create_complaint():
    data = request.get_json()
    new_complaint = Complaint(
        name=data['name'],
        address=data['address'],
        complaint=data['complaint']
    )
    db.session.add(new_complaint)
    db.session.commit()
    return jsonify({'message': 'Complaint created successfully'}), 201

@app.route('/complaints', methods=['GET'])
def get_complaints():
    complaints = Complaint.query.all()
    output = []
    for complaint in complaints:
        complaint_data = {
            'id': complaint.id,
            'name': complaint.name,
            'address': complaint.address,
            'complaint': complaint.complaint
        }
        output.append(complaint_data)
    return jsonify({'complaints': output})

@app.route('/complaints/<id>', methods=['GET'])
def get_complaint(id):
    complaint = Complaint.query.get_or_404(id)
    return jsonify({
        'id': complaint.id,
        'name': complaint.name,
        'address': complaint.address,
        'complaint': complaint.complaint
    })

@app.route('/complaints/<id>', methods=['PUT'])
def update_complaint(id):
    data = request.get_json()
    complaint = Complaint.query.get_or_404(id)
    complaint.name = data['name']
    complaint.address = data['address']
    complaint.complaint = data['complaint']
    db.session.commit()
    return jsonify({'message': 'Complaint updated successfully'})

@app.route('/complaints/<id>', methods=['DELETE'])
def delete_complaint(id):
    complaint = Complaint.query.get_or_404(id)
    db.session.delete(complaint)
    db.session.commit()
    return jsonify({'message': 'Complaint deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
