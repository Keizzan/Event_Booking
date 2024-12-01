# imports
import stripe
from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    session,
    jsonify,
    send_file,
)
from admin import (
    admin_login,
    move_event,
    pull_tables,
    create_event,
    pull_booking,
    pull_event,
    encod,
    delete_booking,
    update_event,
    validators,
    mailing_list,
    add_booking,
    email_classes,
    email_templates,
    guest_list,
)

# flask setting
app = Flask(__name__)


# stripe keys
stripe_keys = {
    "secret_key": "",
    "publishable_key": "",
    "endpoint_secret": "",
}

stripe.api_key = stripe_keys["secret_key"]


# define app secret key
app.secret_key = "secret key"


##########
##ROUTES##
##########


# home page
@app.route("/")
def home():
    return redirect("/login")


# admin page/login
@app.route("/login", methods=["GET", "POST"])
def login():
    # define msg variable
    msg = ""
    session["loggedIn"] = False
    # if form is subbmitted store values in variables
    form = validators.Login()
    if form.validate_on_submit():
        login_details = {"username": form.username.data, "password": form.password.data}

        # check login&password
        if admin_login.login(login_details["username"], login_details["password"]):
            session["loggedIn"] = True
            return redirect(url_for("upcoming"))

        else:
            msg = "Incorrect username/password"
    return render_template("index.html", msg=msg, form=form)


# admin home page/ list of upcoming events
@app.route("/admin/upcoming", methods=["GET", "POST"])
def upcoming():
    # check if logged in
    if session["loggedIn"]:
        # pull event tables
        upcoming_events = pull_tables.show_tables()
        upcoming_events.sort()
        return render_template("upcoming.html", events=upcoming_events)
    else:
        # redirect to login page if not logged in
        return redirect(url_for("login"))


# list of past events
@app.route("/admin/past", methods=["GET", "POST"])
def past():
    # check if logged in
    if session["loggedIn"]:
        # pull event tables
        past_events = pull_tables.show_past_tables()
        return render_template("past.html", events=past_events)
    else:
        # redirect to login page if not logged in
        return redirect(url_for("login"))


# create new event page
@app.route("/admin/new_event", methods=["GET", "POST"])
def new_event():
    # check if logged in
    if session["loggedIn"]:
        # if form is submitted create new event
        if request.method == "POST":
            name = request.form["name"].lower()
            date = (
                request.form["date"][-2:]
                + request.form["date"][-5:-3]
                + request.form["date"][:4]
            )
            time = request.form["time"].replace(":", "")
            price = request.form["price"]
            limit = request.form["limit"]
            desc = request.form["desc"]
            create_event.create_event(name, date, time, price, limit, desc)
            return redirect(url_for("upcoming"))
        else:
            return render_template("new_event.html")
    else:
        # redirect to login page if not logged in
        return redirect(url_for("login"))


# event view page
@app.route("/admin/<event>", methods=["GET"])
def view(event):

    # check if logged in
    if session["loggedIn"]:

        # check if event is in database
        if event in pull_tables.show_tables():

            # pull records from database
            event_details = pull_event.pull_event(event)[0]
            records, salt = pull_booking.pull_records(event)

            # create empty dict
            records_dict = {}

            # loop through records from database and insert them in dict
            for record in records:
                for i in record:
                    records_dict.update(
                        {
                            i[0]: {
                                "fname": encod.decrypt_data(salt, i[1]),
                                "lname": encod.decrypt_data(salt, i[2]),
                                "email": encod.decrypt_data(salt, i[3]),
                                "phone": encod.decrypt_data(salt, i[4]),
                                "booking": i[5],
                            }
                        }
                    )

            # get sum of all booking slots
            total_booking = []
            for booking in records_dict.values():
                total_booking.append(int(booking["booking"]))
            total_booking = sum(total_booking)

            return render_template(
                "view.html",
                records=records_dict,
                event=event_details,
                booking=total_booking,
            )
        # if event is not in database redirect to upcoming page
        else:
            return redirect(url_for("upcoming"))
    else:
        return redirect(url_for("login"))


# event view page
@app.route("/admin/past/<event>", methods=["GET"])
def view_past(event):

    # check if logged in
    if session["loggedIn"]:

        # check if event is in database
        if event in pull_tables.show_past_tables():

            # pull records from database
            event_details = pull_event.pull_pastevent(event)[0]
            records, salt = pull_booking.pull_records_past(event)

            # create empty dict
            records_dict = {}

            # loop through records from database and insert them in dict
            for record in records:
                for i in record:
                    records_dict.update(
                        {
                            i[0]: {
                                "fname": encod.decrypt_data(salt, i[1]),
                                "lname": encod.decrypt_data(salt, i[2]),
                                "email": encod.decrypt_data(salt, i[3]),
                                "phone": encod.decrypt_data(salt, i[4]),
                                "booking": i[5],
                            }
                        }
                    )

            # get sum of all booking slots
            total_booking = []
            for booking in records_dict.values():
                total_booking.append(int(booking["booking"]))
            total_booking = sum(total_booking)

            return render_template(
                "view_past.html",
                records=records_dict,
                event=event_details,
                booking=total_booking,
            )
        # if not redirect to past page
        else:
            return redirect(url_for("past"))
    else:
        return redirect(url_for("login"))


@app.route("/admin/<event>/update", methods=["GET", "POST"])
def update(event):
    # check if logged in
    if session["loggedIn"]:
        # if form is submitted update event
        if request.method == "POST":
            name = request.form["name"].replace(" ", "_").lower()
            date = (
                request.form["date"][-2:]
                + request.form["date"][-5:-3]
                + request.form["date"][:4]
            )
            time = request.form["time"].replace(":", "")
            price = request.form["price"]
            limit = request.form["limit"]
            desc = request.form["desc"]
            event_name = name + date + time
            update_event.update_event(event_name, name, date, time, price, limit, desc)
            return redirect(url_for("view", event=event_name))
        else:
            event_details = pull_event.pull_event(event)[0]
            return render_template("update_event.html", event=event_details)
    else:
        return redirect(url_for("login"))


@app.route("/admin/<event>/add_booking", methods=["GET", "POST"])
def man_new_booking(event):
    if event in pull_tables.show_tables():
        if session["loggedIn"]:
            # if form is submitted create new event
            if request.method == "POST":
                fname = request.form["fname"].capitalize()
                lname = request.form["lname"].capitalize()
                email = request.form["email"]
                phone = request.form["phone"]
                booking = request.form["booking"]
                add_booking.add_booking(event, fname, lname, email, phone, booking)
                return redirect(url_for("view", event=event))
            else:
                return render_template("man_new_booking.html", event=event)
        else:
            # redirect to login page if not logged in
            return redirect(url_for("login"))
    else:
        return render_template("404.html")


# add new booking
@app.route("/<event>", methods=["GET", "POST"])
def new_booking(event):

    # clear cookies
    session.pop("user_booking", None)
    session.pop("event_details", None)
    msg = ""
    # check if event is in database
    if event in pull_tables.show_tables():
        # pull event details
        event_details = pull_event.pull_event(event)[0]
        # pull total user bookings and store it in list
        records = pull_booking.pull_user_booking(event)
        user_bookings = []
        for booking in records:
            user_bookings.append(int(booking[0]))
        total_booking = sum(user_bookings)

        # check if total bookings exceed 80% available spaces
        show_left_bookings = False
        if total_booking > 0.8 * int(event_details[-4]):
            show_left_bookings = True
        left_spaces = int(event_details[-4]) - total_booking

        # create form from class user in validators.py
        form = validators.User()
        if form.validate_on_submit():
            # store data in cache
            session["user_booking"] = {
                "fname": form.fname.data,
                "lname": form.lname.data,
                "email": form.email.data,
                "phone": form.phone.data,
                "booking": form.booking.data,
                "mailing_list": form.mailing_list.data,
            }

            # check if user opt in for mailing list
            if session["user_booking"]["mailing_list"]:

                # if email already on mailing list pass
                if session["user_booking"]["email"] in mailing_list.pull_mail():
                    pass

                # else add email to mailing list
                else:
                    mailing_list.add_mail(session["user_booking"]["email"])

            # check if booking limit was not exceeded
            if total_booking + int(session["user_booking"]["booking"]) > int(
                event_details[-4]
            ):
                msg = "Booking limit for event was exceeded"
                return render_template(
                    "new_booking.html",
                    form=form,
                    event=event,
                    event_details=event_details,
                    left_spaces=left_spaces,
                    show_left_bookings=show_left_bookings,
                    msg=msg,
                )

            # proceed to payment form if all ok
            session["event_details"] = event_details
            return render_template(
                "checkout.html",
                user_booking=session["user_booking"],
                price=int(session["event_details"][4]),
            )

        return render_template(
            "new_booking.html",
            form=form,
            event=event,
            event_details=event_details,
            left_spaces=left_spaces,
            show_left_bookings=show_left_bookings,
            msg=msg,
        )
    # if event not found put 404.html
    else:
        return render_template("404.html")


## stripe payment form
@app.route("/create-checkout-session")
def create_checkout_session():
    domain_url = "http://127.0.0.1:5000/"
    stripe.api_key = stripe_keys["secret_key"]
    try:
        # Create new Checkout Session for the order
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + "success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=domain_url + "cancelled",
            payment_method_types=["card"],
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": "gbp",
                        "product_data": {
                            "name": session["event_details"][1]
                            .replace("_", " ")
                            .capitalize(),
                        },
                        "unit_amount": (int(session["event_details"][4]) * 100),
                    },
                    "quantity": int(session["user_booking"]["booking"]),
                }
            ],
        )
        return jsonify({"sessionId": checkout_session["id"]})
    except Exception as e:
        return jsonify(error=str(e)), 403


# success redirection
@app.route("/success")
def success():
    # table name variable
    table_name = (
        session["event_details"][1]
        + session["event_details"][2]
        + session["event_details"][3]
    )
    # add new record in table
    add_booking.add_booking(
        table_name,
        session["user_booking"]["fname"],
        session["user_booking"]["lname"],
        session["user_booking"]["email"],
        session["user_booking"]["phone"],
        session["user_booking"]["booking"],
    )

    # send confirmation emails
    email_classes.Confimation(
        session["user_booking"]["email"],
        email_templates.confirmation_text,
        email_templates.confirmation_html,
        session["user_booking"]["fname"],
    ).send()

    email_classes.Admin_confirmation(
        email_templates.confirmation_admin,
        session["user_booking"]["fname"],
        session["user_booking"]["lname"],
        session["user_booking"]["booking"],
        session["event_details"][1].replace("_", " ").capitalize(),
    ).send()

    # clear cookies
    session.pop("user_booking", None)
    session.pop("event_details", None)
    return render_template("success.html")


# cancel redirection
@app.route("/cancelled")
def cancelled():

    # clear cookies
    session.pop("user_booking", None)
    return render_template("cancelled.html")


# delete booking
@app.route("/admin/<event>/<int:id>")
def delete_booked_record(event, id):
    # check if logged in
    if session["loggedIn"]:
        delete_booking.delete_booking(event, id)
        return redirect(url_for("view", event=event))
    else:
        return redirect(url_for("login"))


# cancel event
@app.route("/admin/<event>/cancel")
def cancel_event(event):
    # check if logged in
    if session["loggedIn"]:

        # get emails and salt
        emails, salt = pull_booking.get_emails(event)

        # loop through list of emails
        # decrypt them and send email
        for email in emails:
            email_classes.Cancellation(
                encod.decrypt_data(salt, email[0]),
                email_templates.cancellation_text,
                email_templates.cancellation_html,
                event[:-12].replace("_", " ").capitalize(),
                event[-12:-10] + "/" + event[-10:-8] + "/" + event[-8:-4],
                event[-4:-2] + ":" + event[-2:],
            ).send()

        # delete event table and move it to past_event db
        move_event.event(event, "cancelled")

        return redirect(url_for("past"))
    else:
        return redirect(url_for("login"))


# get stripe public key
@app.route("/config")
def get_publishable_key():
    stripe_config = {"publicKey": stripe_keys["publishable_key"]}
    return jsonify(stripe_config)


# close & download event
@app.route("/admin/<event>/download")
def download_list(event):
    if session["loggedIn"]:
        return guest_list.download_list(event)
    else:
        return redirect(url_for("login"))


@app.route("/admin/<event>/close")
def close(event):
    if session["loggedIn"]:
        move_event.event(event, "closed")
        return redirect(url_for("past"))
    else:
        return redirect(url_for("login"))


# logout function
@app.route("/logout")
def logout():
    session.pop("loggedIn", False)
    return redirect(url_for("login"))


# error page - 404 not found
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
