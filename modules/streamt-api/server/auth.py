from streamt_db.user import User


def load_user_fn(db):
    def load_user(id):
        return db.session.query(User).filter_by(login_id=id).first()
    return load_user
