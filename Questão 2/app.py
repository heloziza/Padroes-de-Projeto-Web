# app.py
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class ContactModel:
    def __init__(self):
        self.contacts = []

    def add_contact(self, name, phone, email):
        contact = {'name': name, 'phone': phone, 'email': email}
        self.contacts.append(contact)

    def get_contacts(self):
        return self.contacts

    def remove_contact(self, index):
        del self.contacts[index]

class ContactPresenter:
    def __init__(self, view, model):
        self.view = view
        self.model = model

    def add_contact(self, name, phone, email):
        self.model.add_contact(name, phone, email)
        self.update_view()

    def remove_contact(self, index):
        self.model.remove_contact(index)
        self.update_view()

    def get_contacts_with_indices(self):
        return enumerate(self.model.get_contacts())

    def update_view(self):
        contacts_with_indices = self.get_contacts_with_indices()
        return self.view.display_contacts(contacts_with_indices)

class ContactView:
    def display_contacts(self, contacts_with_indices):
        return render_template('index.html', contacts_with_indices=contacts_with_indices)

model = ContactModel()
view = ContactView()
presenter = ContactPresenter(view, model)

@app.route('/')
def index():
    return presenter.update_view()

@app.route('/add_contact', methods=['POST'])
def add_contact():
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    presenter.add_contact(name, phone, email)
    return redirect(url_for('index'))

@app.route('/remove_contact/<int:index>')
def remove_contact(index):
    presenter.remove_contact(index)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
