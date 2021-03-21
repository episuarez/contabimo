import datetime

from pony import orm

db = orm.Database();

class Companies(db.Entity):
    id = orm.PrimaryKey(int, auto=True);
    name = orm.Required(str, unique=True);
    dni_cif = orm.Required(str, unique=True);
    email = orm.Optional(str, nullable=True);
    phone = orm.Optional(str, nullable=True);
    date = orm.Required(datetime.date);
    modification_date = orm.Required(datetime.date);
    address = orm.Required(str);
    postal_code = orm.Required(str);
    city = orm.Required(str);
    province = orm.Required(str);
    country = orm.Required(str);
    notes = orm.Optional(str, nullable=True)
    income_invoice = orm.Set("IncomeInvoice");
    expense_invoice = orm.Set("ExpenseInvoice");

class IncomeInvoice(db.Entity):
    id = orm.PrimaryKey(int, auto=True);
    identifier = orm.Required(str, unique=True);
    date = orm.Required(datetime.date);
    modification_date = orm.Required(datetime.date);
    expiration_date = orm.Required(datetime.date);
    status = orm.Required(str);
    irpf = orm.Required(float);
    iva = orm.Required(float);
    irpf_money = orm.Required(float);
    iva_money = orm.Required(float);
    total = orm.Required(float);
    notes = orm.Optional(str, nullable=True);
    company = orm.Required(Companies);
    products = orm.Set("IncomeProducts");

class ExpenseInvoice(db.Entity):
    id = orm.PrimaryKey(int, auto=True);
    identifier = orm.Required(str, unique=True);
    date = orm.Required(datetime.date);
    modification_date = orm.Required(datetime.date);
    expiration_date = orm.Required(datetime.date);
    status = orm.Required(str);
    irpf = orm.Required(float);
    iva = orm.Required(float);
    irpf_money = orm.Required(float);
    iva_money = orm.Required(float);
    total = orm.Required(float);
    notes = orm.Optional(str, nullable=True);
    company = orm.Required(Companies);
    products = orm.Set("ExpenseProducts");

class IncomeProducts(db.Entity):
    id = orm.PrimaryKey(int, auto=True);
    description = orm.Required(str);
    amount = orm.Required(float);
    price = orm.Required(float);
    invoice = orm.Required(IncomeInvoice);

class ExpenseProducts(db.Entity):
    id = orm.PrimaryKey(int, auto=True);
    description = orm.Required(str);
    amount = orm.Required(float);
    price = orm.Required(float);
    invoice = orm.Required(ExpenseInvoice);

db.bind(provider="sqlite", filename="data.db", create_db=True);
db.generate_mapping(create_tables=True);
