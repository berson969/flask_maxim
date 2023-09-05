from flask import Flask, jsonify
from flask.views import MethodView
from flask import request
from hashlib import md5
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from models import Ads, Session
from validation import CreateAds, UpdateAds

app = Flask('app')
SALT = '23vtht567ujmn'


class HttpError(Exception):

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


def validate(json_data, schema):
    try:
        model = schema(**json_data)
        return model.dict(exclude_none=True)
    except ValidationError as err:
        error_message = err.json()
        raise HttpError(400, error_message)


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    http_response = jsonify({'status': 'error', 'message': error.message})
    http_response.status_code = error.status_code
    return http_response


# def hash_password(password: str):
#     password = f'{SALT}{password}'
#     password = password.encode()
#     password = md5(password).hexdigest()
#     return password


def get_id(ads_id: int, session: Session):
    ads = session.get(Ads, ads_id)
    if ads is None:
        raise HttpError(404, 'Ads not found!')
    return ads


class AdsViews(MethodView):
    def get(self, ads_id):
        print(ads_id)
        with Session() as session:
            ads = get_id(ads_id, session)
            return jsonify({'id': ads.id,
                            'header': ads.header})

    def post(self):
        # json_data = validate(request.json, CreateAds)
        # json_data['password'] = hash_password(json_data['password'])
        with Session() as session:
            new_ads = Ads(**request.json)
            session.add(new_ads)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(408, 'User already exists')
            return jsonify({'id': new_ads.id,
                            'header': new_ads.header})

    def patch(self, ads_id):
        with Session() as session:
            ads = get_id(ads_id, session)
            for k, v in request.json.items():
                setattr(ads, k, v)
            session.add(ads)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(408, 'User already exists')
            return jsonify({'status': 'success'})

    def delete(self, ads_id):
        with Session() as session:
            ads = get_id(ads_id, session)
            session.delete(ads)
            session.commit()
            return jsonify({'delete ads_id': ads.id})


ads_view = AdsViews.as_view('ads')

app.add_url_rule('/ads/', view_func=ads_view, methods=['POST'])
app.add_url_rule('/ads/<int:ads_id>', view_func=ads_view, methods=['GET', 'PATCH', 'DELETE'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
