import datetime
import json
import math
import time

import pdfkit
from flask import Flask, flash, redirect, render_template, request, url_for, make_response
from pony.orm import Database

import models

app = Flask(__name__);

app.config["DEBUG"] = True;
app.config["SECRET_KEY"] = "R7Dmcd3cMVET1lk121J8sQLFJGgXRFkCDwYYAC0ESHSGzWzaaNpDF5MGLpzy";

data = json.load(open("my_data.json", encoding="utf-8"));

@app.route("/")
def home():
    return render_template("home.html");

# Companies

@app.route("/companies", defaults={"page": 1})
@app.route("/companies/<int:page>")
def companies(page):
    limit = 25;

    with models.orm.db_session:
        companies = models.orm.select(
            (
                company, 
                sum(income.total for income in company.income_invoice),
                sum(expense.total for expense in company.expense_invoice),
            ) 
            for company in models.Companies).order_by(lambda: company.name);

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
    if request.method == "POST":
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

# Income

@app.route("/incomes", defaults={"page": 1})
@app.route("/incomes/<int:page>")
def incomes(page):
    limit = 25;

    with models.orm.db_session:
        incomes = models.orm.select(incomes for incomes in models.IncomeInvoice).order_by(lambda: incomes.id);

        maxpage = math.ceil(incomes.count() / limit);
        incomes = list(incomes.page(page, limit));

        return render_template("incomes.html", incomes=incomes, maxpage=maxpage, page=page);

@app.route("/incomes/add", methods=["GET", "POST"])
def add_income():
    if request.method == "POST":
        with models.orm.db_session:
            if models.orm.count(income for income in models.IncomeInvoice if income.identifier == request.form["identifier"]) > 0:
                flash(f"El identificador {request.form['identifier']} está repetido, no se ha podido agregar el ingreso.");
                return redirect(url_for("incomes"));
            else:
                new_income = models.IncomeInvoice(
                    company=request.form["company"],
                    identifier=request.form["identifier"],
                    date=datetime.datetime.now(),
                    modification_date=datetime.datetime.now(),
                    expiration_date=datetime.datetime.strptime(request.form["expiration_date"], "%d/%m/%Y"),
                    status=request.form["status"],
                    irpf=request.form["irpf"],
                    iva=request.form["iva"],
                    irpf_money=request.form["irpf_money"],
                    iva_money=request.form["iva_money"],
                    total=request.form["total"],
                    notes=request.form["notes"]
                );
                models.orm.commit();

                keys = list(dict(request.form).keys());
                for field in range(10, len(keys), 3):
                    position = keys[field][-3:];

                    new_product = models.IncomeProducts(
                        invoice=new_income.id,
                        description=request.form["description" + position],
                        amount=request.form["amount" + position],
                        price=request.form["price" + position]
                    );

                flash("Se ha agregado correctamente el ingreso");
        return redirect(url_for("incomes"));
    else:
        with models.orm.db_session:
            last_identifier = list(models.orm.select(income.identifier for income in models.IncomeInvoice if income.date > datetime.datetime(int(time.strftime("%Y")), 1, 1)))[-1];
        number = int(last_identifier[-3:]) + 1;
        number = ("0" * (3 - len(str(number))))  + str(number);

        identifier = data["DEFAULTS"]["START_IDENTIFIER"] + time.strftime("%Y") + number;

        with models.orm.db_session:
            companies = list(models.orm.select((company.id, company.name) for company in models.Companies).order_by(lambda: company.name));

        return render_template("add_income.html", companies=companies, identifier=identifier, iva=data["DEFAULTS"]["IVA"], irpf=data["DEFAULTS"]["IRPF"]);

@app.route("/incomes/copy/<id>")
def copy_income(id):
    with models.orm.db_session:
        if models.orm.count(income for income in models.IncomeInvoice if income.id == id) > 0:
            last_identifier = list(models.orm.select(income.identifier for income in models.IncomeInvoice if income.date > datetime.datetime(int(time.strftime("%Y")), 1, 1)))[-1];
            number = int(last_identifier[-3:]) + 1;
            number = ("0" * (3 - len(str(number))))  + str(number);

            identifier = data["DEFAULTS"]["START_IDENTIFIER"] + time.strftime("%Y") + number;

            income = models.IncomeInvoice[id];
            companies = list(models.orm.select((company.id, company.name) for company in models.Companies).order_by(lambda: company.name));

            return render_template("copy_income.html", identifier=identifier, income=income, companies=companies);
        else:
            flash("No se encuentra el ingreso que intentas copiar.")
            return redirect(url_for("incomes"));

@app.route("/incomes/pdf/<pdf>/<id>")
def view_income_pdf_f(id, pdf):
    with models.orm.db_session:
        if models.orm.count(income for income in models.IncomeInvoice if income.id == id) > 0:
            income = list(models.orm.select(income for income in models.IncomeInvoice if income.id == id))[0];
            
            if pdf and pdf in "fp":
                if pdf == "f":
                    html = render_template("pdf/income.html", my_company=data["my_company"], income=income);
                else:
                    html = render_template("pdf/budget.html", my_company=data["my_company"], income=income);

                options = {
                    "page-size": "A4",
                    "dpi": 300
                }
                pdf = pdfkit.from_string(html, False, options=options, css="static/pdf.css");
                
                response = make_response(pdf);
                response.headers["Content-Type"] = "application/pdf"
                response.headers["Content-Disposition"] = f"filename={income.identifier}.pdf"
                
                return response;
            else:
                flash("Tipo de pdf invalido.")
                return redirect(url_for("incomes"));
        else:
            flash("No existe el ingreso.")
            return redirect(url_for("incomes"));

@app.route("/incomes/delete/<id>")
def delete_income(id):
    with models.orm.db_session:
        if models.orm.count(income for income in models.IncomeInvoice if income.id == id) > 0:
            models.IncomeInvoice[id].delete();
            flash("Se ha eliminado el ingreso.")
            return redirect(url_for("incomes"));
        else:
            flash("No se encuentra a la compañia que intentas acceder.")
            return redirect(url_for("incomes"));

@app.route("/incomes/view/<id>")
def view_income(id):
    with models.orm.db_session:
        if models.orm.count(income for income in models.IncomeInvoice if income.id == id) > 0:
            income = models.IncomeInvoice[id];
            return render_template("view_income.html", income=income);
        else:
            flash("No se encuentra el ingreso que intentas acceder.")
            return redirect(url_for("incomes"));

@app.route("/incomes/edit/<id>", methods=["GET", "POST"])
def edit_invoice(id):
    with models.orm.db_session:
        if models.orm.count(income for income in models.IncomeInvoice if income.id == id) > 0:
            if request.method == "POST":
                income = models.IncomeInvoice[id];

                income.company = request.form["company"];
                income.modification_date = datetime.datetime.now();
                income.expiration_date = datetime.datetime.strptime(request.form["expiration_date"], "%d/%m/%Y");
                income.status = request.form["status"];
                income.irpf = request.form["irpf"];
                income.iva = request.form["iva"];
                income.irpf_money = request.form["irpf_money"];
                income.iva_money = request.form["iva_money"];
                income.total = request.form["total"];
                income.notes = request.form["notes"];

                models.orm.select(income_product for income_product in models.IncomeProducts if income_product.invoice.id == income.id).delete();

                keys = list(dict(request.form).keys());
                for field in range(10, len(keys), 3):
                    position = keys[field][-3:];

                    new_product = models.IncomeProducts(
                        invoice=income.id,
                        description=request.form["description" + position],
                        amount=request.form["amount" + position],
                        price=request.form["price" + position]
                    );

                return redirect(url_for("incomes"));
            else:
                income = models.IncomeInvoice[id];
                companies = list(models.orm.select((company.id, company.name) for company in models.Companies).order_by(lambda: company.name));

                return render_template("edit_income.html", income=income, companies=companies);
        else:
            flash("No se encuentra el ingreso que intentas acceder.")
            return redirect(url_for("incomes"));

# Expenses

@app.route("/expenses", defaults={"page": 1})
@app.route("/expenses/<int:page>")
def expenses(page):
    limit = 25;

    with models.orm.db_session:
        expenses = models.orm.select(expense for expense in models.ExpenseInvoice).order_by(lambda: expense.id);

        maxpage = math.ceil(expenses.count() / limit);
        expenses = list(expenses.page(page, limit));

        return render_template("expenses.html", expenses=expenses, maxpage=maxpage, page=page);

@app.route("/expenses/add", methods=["GET", "POST"])
def add_expense():
    if request.method == "POST":
        with models.orm.db_session:
            if models.orm.count(expense for expense in models.ExpenseInvoice if expense.identifier == request.form["identifier"]) > 0:
                flash(f"El identificador {request.form['identifier']} está repetido, no se ha podido agregar el gasto.");
                return redirect(url_for("expenses"));
            else:
                new_expense = models.ExpenseInvoice(
                    company=request.form["company"],
                    identifier=request.form["identifier"],
                    date=datetime.datetime.now(),
                    modification_date=datetime.datetime.now(),
                    expiration_date=datetime.datetime.strptime(request.form["expiration_date"], "%d/%m/%Y"),
                    status=request.form["status"],
                    irpf=request.form["irpf"],
                    iva=request.form["iva"],
                    irpf_money=request.form["irpf_money"],
                    iva_money=request.form["iva_money"],
                    total=request.form["total"],
                    notes=request.form["notes"]
                );
                models.orm.commit();

                keys = list(dict(request.form).keys());
                for field in range(10, len(keys), 3):
                    position = keys[field][-3:];

                    new_product = models.ExpenseProducts(
                        invoice=new_expense.id,
                        description=request.form["description" + position],
                        amount=request.form["amount" + position],
                        price=request.form["price" + position]
                    );

                flash("Se ha agregado correctamente el ingreso");
        return redirect(url_for("expenses"));
    else:
        with models.orm.db_session:
            companies = list(models.orm.select((company.id, company.name) for company in models.Companies).order_by(lambda: company.name));

        return render_template("add_expense.html", companies=companies, iva=data["DEFAULTS"]["IVA"], irpf=data["DEFAULTS"]["IRPF"]);

@app.route("/expenses/copy/<id>")
def copy_expense(id):
    with models.orm.db_session:
        if models.orm.count(expense for expense in models.ExpenseInvoice if expense.id == id) > 0:
            expense = models.ExpenseInvoice[id];
            companies = list(models.orm.select((company.id, company.name) for company in models.Companies).order_by(lambda: company.name));

            return render_template("copy_expense.html", expense=expense, companies=companies);
        else:
            flash("No se encuentra el ingreso que intentas copiar.")
            return redirect(url_for("expenses"));

@app.route("/expenses/delete/<id>")
def delete_expense(id):
    with models.orm.db_session:
        if models.orm.count(expense for expense in models.ExpenseInvoice if expense.id == id) > 0:
            models.ExpenseInvoice[id].delete();
            flash("Se ha eliminado el gasto.")
            return redirect(url_for("expenses"));
        else:
            flash("No se encuentra el gasto que intentas acceder.")
            return redirect(url_for("expenses"));

@app.route("/expenses/view/<id>")
def view_expense(id):
    with models.orm.db_session:
        if models.orm.count(expense for expense in models.ExpenseInvoice if expense.id == id) > 0:
            expense = models.ExpenseInvoice[id];
            return render_template("view_expense.html", expense=expense);
        else:
            flash("No se encuentra el gasto que intentas acceder.")
            return redirect(url_for("expenses"));

@app.route("/expenses/edit/<id>", methods=["GET", "POST"])
def edit_expense(id):
    with models.orm.db_session:
        if models.orm.count(expense for expense in models.ExpenseInvoice if expense.id == id) > 0:
            if request.method == "POST":
                expense = models.ExpenseInvoice[id];

                expense.company = request.form["company"];
                expense.modification_date = datetime.datetime.now();
                expense.expiration_date = datetime.datetime.strptime(request.form["expiration_date"], "%d/%m/%Y");
                expense.status = request.form["status"];
                expense.irpf = request.form["irpf"];
                expense.iva = request.form["iva"];
                expense.irpf_money = request.form["irpf_money"];
                expense.iva_money = request.form["iva_money"];
                expense.total = request.form["total"];
                expense.notes = request.form["notes"];

                models.orm.select(expense_product for expense_product in models.ExpenseProducts if expense_product.invoice.id == expense.id).delete();

                keys = list(dict(request.form).keys());
                for field in range(10, len(keys), 3):
                    position = keys[field][-3:];

                    new_product = models.ExpenseProducts(
                        invoice=expense.id,
                        description=request.form["description" + position],
                        amount=request.form["amount" + position],
                        price=request.form["price" + position]
                    );

                return redirect(url_for("expenses"));
            else:
                expense = models.ExpenseInvoice[id];
                companies = list(models.orm.select((company.id, company.name) for company in models.Companies).order_by(lambda: company.name));

                return render_template("edit_expense.html", expense=expense, companies=companies);
        else:
            flash("No se encuentra el gasto que intentas acceder.")
            return redirect(url_for("expenses"));
