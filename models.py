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
    invoices = orm.Set("Invoices");

class Invoices(db.Entity):
    id = orm.PrimaryKey(int, auto=True);
    company = orm.Required(Companies);
    type_invoices = orm.Required(bool)
    date = orm.Required(datetime.date);
    expiration_dae = orm.Required(datetime.date);
    identifier = orm.Required(str, unique=True);
    irpf = orm.Required(float);
    iva = orm.Required(float);
    notes = orm.Optional(str, nullable=True);
    products = orm.Set("Products");
    company = orm.Required(Companies);

class Products(db.Entity):
    id = orm.PrimaryKey(int, auto=True);
    description = orm.Required(str);
    amount = orm.Required(float);
    price = orm.Required(float);
    invoice = orm.Required(Invoices);

db.bind(provider="sqlite", filename="data.db", create_db=True);
db.generate_mapping(create_tables=True);
