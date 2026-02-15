from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash
from app import app, db
from app.models.authuser import AuthUser, PrivateContact

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.reflect()
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    user1 = AuthUser(
        email="kittipitch@gmail.com",
        name='สมชาย ทรงแบด',
        password=generate_password_hash('1234', method='sha256'),
        avatar_url=("https://ui-avatars.com/api/"
                    "?name=สมชาย+ทรงแบด"
                    "&background=83ee03&color=fff")
    )

    user2 = AuthUser(
        email="flask1@204212",
        name='ส้มโอ โอเค',
        password=generate_password_hash('1234', method='sha256'),
        avatar_url=("https://ui-avatars.com/api/"
                    "?name=ส้มโอ+โอเค"
                    "&background=83ee03&color=fff")
    )

    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    # Now we can add the contact using user.id
    private_contact = PrivateContact(
        firstname='ส้มโอ',
        lastname='โอเค',
        phone='081-111-1112',
        owner_id=user1.id  # Explicitly pass owner_id
    )

    db.session.add(private_contact)
    db.session.commit()


if __name__ == "__main__":
    cli()
