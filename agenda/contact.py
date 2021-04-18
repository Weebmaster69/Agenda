from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from  agenda.auth import login_required
from agenda.midb import get_db

bp= Blueprint("contact", __name__)

@bp.route("/")
@login_required
def index():
    db, c = get_db()
    c.execute(
        'select c.id, c.name, u.username, c.number, c.job '
        'from contact c JOIN user u on c.created_by = u.id where c.created_by = %s'
        %(g.user['id'],)
    )
    contacts = c.fetchall()

    return render_template("herramientas/index.html", contacts=contacts)

@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        name = request.form["name"]
        number = request.form["number"]
        job = request.form["job"]
        error = None

        if not name:
            error = "Nombre requerido"
        if not number:
            error = "Numero requerido"
        if not job:
            job=""
        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute(
                "insert into contact (name, number, job, created_by)"
                " values (%s, %s, %s, %s)",
                (name, number, job, g.user["id"])
            )
            db.commit()
            return redirect(url_for("contact.index"))

    return render_template("herramientas/create.html")

def get_contact(id):
    db, c=get_db()
    c.execute(
        'select c.id, c.name, u.username, c.number, c.job '
        'from contact c join user u on c.created_by = u.id where c.id = %s',
        (id,)
    )

    contact = c.fetchone()
    if contact is None:
        abort(404, "El contacto de id {0} no existe".format(id))

    return contact

@bp.route("/<int:id>/update", methods=["GET", "POST"])
@login_required
def update(id):
    contact = get_contact(id)
    if request.method == "POST":
        name = request.form["name"]
        number = request.form["number"]
        job = request.form["job"]
        error = None
        if not name:
            error = "Nombre es requerido"
        if not number:
            error="Numero es requerido"
        if error is not None:
            flash(error)
        else:
            db,c = get_db()
            c.execute(
                'update contact set name = %s, number = %s, job = %s'
                ' where id = %s and created_by = %s',
                (name, number, job, id, g.user['id'])
            )
            db.commit()
            return redirect(url_for("contact.index"))
    return render_template("herramientas/update.html",contact=contact)

@bp.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete(id):
    db, c = get_db()
    c.execute('delete from contact where id = %s and created_by = %s', (id, g.user['id']))
    db.commit()
    return redirect(url_for('contact.index'))
