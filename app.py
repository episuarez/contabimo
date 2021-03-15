import datetime
import math

from flask import Flask, flash, redirect, render_template, request, url_for
from pony.orm import Database

import models

app = Flask(__name__);

app.config["DEBUG"] = True;
app.config["SECRET_KEY"] = "fdfgdfgdfgdp90349g03j49jg3049jg0394tj094u2094u2039i0239ir0";

@app.route("/")
def home():
    return render_template("home.html");

# Companies

@app.route("/companies", defaults={"page": 1})
@app.route("/companies/<int:page>")
def companies(page):
    limit = 25;

    with models.orm.db_session:
        companies = models.orm.select(company for company in models.Companies).order_by(lambda: company.name);

        maxpage = math.ceil(companies.count() / limit);
        companies = list(companies.page(page, limit));

        return render_template("companies.html", companies=companies, maxpage=maxpage, page=page);

@app.route("/companies/add", methods=["GET", "POST"])
def add_company():
    if request.method == "POST" :
        with models.orm.db_session:
            if models.orm.count(company for company in models.Companies if company.name == request.form["name"]) > 0:
                flash(f"El nombre {request.form['name']} está repetido, no se ha podido agregar la empresa.");
                return redirect(url_for("companies"));
            elif models.orm.count(company for company in models.Companies if company.dni_cif == request.form["dni_cif"]) > 0:
                flash(f"El dni / cif {request.form['dni_cif']} está repetido, no se ha podido agregar la empresa.");
                return redirect(url_for("companies"));
            else:
                new_company = models.Companies(
                    name=request.form["name"],
                    dni_cif=request.form["dni_cif"],
                    email=request.form["email"],
                    phone=request.form["phone"],
                    date=datetime.datetime.now(),
                    modification_date=datetime.datetime.now(),
                    address=request.form["address"],
                    postal_code=request.form["postal_code"],
                    city=request.form["city"],
                    province=request.form["province"],
                    country=request.form["country"],
                    notes=request.form["notes"]
                );

                flash("Se ha agregado correctamente la empresa");
        return redirect(url_for("companies"));
    else:
        return render_template("add_company.html");

@app.route("/companies/delete/<id>")
def delete_company(id):
    with models.orm.db_session:
        if models.orm.count(company for company in models.Companies if company.id == id) > 0:
            models.Companies[id].delete();
            flash("Se ha eliminado la empresa.")
            return redirect(url_for("companies"));
        else:
            flash("No se encuentra a la compañia que intentas acceder.")
            return redirect(url_for("companies"));

@app.route("/companies/view/<id>")
def view_company(id):
    with models.orm.db_session:
        if models.orm.count(company for company in models.Companies if company.id == id) > 0:
            company = models.Companies[id];
            return render_template("view_company.html", company=company);
        else:
            flash("No se encuentra a la compañia que intentas acceder.")
            return redirect(url_for("companies"));

@app.route("/companies/edit/<id>", methods=["GET", "POST"])
def edit_company(id):
    if request.method == "POST" :
        with models.orm.db_session:
            if models.orm.count(company for company in models.Companies if company.id == id) > 0:
                company = models.Companies[id];

                if models.orm.count(company for company in models.Companies if company.name == request.form["name"]) > 0:
                    flash(f"El nombre {request.form['name']} está repetido, no se ha podido modificar la empresa.");
                    return redirect(url_for("companies"));
                elif models.orm.count(company for company in models.Companies if company.dni_cif == request.form["dni_cif"]) > 0:
                    flash(f"El dni / cif {request.form['dni_cif']} está repetido, no se ha podido modificar la empresa.");
                    return redirect(url_for("companies"));
                else:
                    company.name = request.form["name"];
                    company.dni_cif = request.form["dni_cif"];
                    company.email = request.form["email"];
                    company.phone = request.form["phone"];
                    company.modification_date = datetime.datetime.now();
                    company.address = request.form["address"];
                    company.postal_code = request.form["postal_code"];
                    company.city = request.form["city"];
                    company.province = request.form["province"];
                    company.country = request.form["country"];
                    company.notes = request.form["notes"];

                    flash("Se ha modificado correctamente la empresa");
                    return redirect(url_for("companies"));
    else:
        with models.orm.db_session:
            if models.orm.count(company for company in models.Companies if company.id == id) > 0:
                company = models.Companies[id];
                return render_template("edit_company.html", company=company);
            else:
                flash("No se encuentra a la compañia que intentas acceder.")
                return redirect(url_for("companies"));

# Invoices

@app.route("/invoices")
@app.route("/invoices/<year>")
def invoices():
    pass;

@app.route("/invoices/add", methods=["GET", "POST"])
def add_invoice():
    pass;

@app.route("/invoices/copy")
def copy_invoice():
    pass;

@app.route("/invoices/pdf/<id>")
def view_invoice_pdf(id):
    pass;

@app.route("/invoices/delete/<id>")
def delete_invoice(id):
    pass;

@app.route("/invoices/edit/<id>", methods=["GET", "POST"])
def edit_invoice(id):
    pass;

# Products

@app.route("/products/delete/<id>/<invoice_id>")
def delete_products(id, invoice_id):
    pass;

# Analytics

@app.route("/analytics")
def analytics():
    pass;
