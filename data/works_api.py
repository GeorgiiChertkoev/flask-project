import flask

from . import db_session
from flask import *
from .works import Works


blueprint = flask.Blueprint(
    'works_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/works', methods=['POST'])
def create_work():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['title','genre_id', 'content', 'user_id', 'is_private']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    works = Works(
        title=request.json['title'],
        genre_id=request.json['genre_id'],
        content=request.json['content'],
        user_id=request.json['user_id'],
        is_private=request.json['is_private']
    )
    db_sess.add(works)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/works/<int:work_id>', methods=['DELETE'])
def delete_works(work_id):
    db_sess = db_session.create_session()
    works = db_sess.query(Works).get(work_id)
    if not works:
        return jsonify({'error': 'Not found'})
    db_sess.delete(works)
    db_sess.commit()
    return jsonify({'success': 'OK'})



@blueprint.route('/api/works/<int:work_id>', methods=['GET'])
def get_one_work(work_id):
    db_sess = db_session.create_session()
    work = db_sess.query(Works).get(work_id)
    if not work:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'work': work.to_dict(only=(
                'title', 'content', 'user_id', 'is_private'))
        }
    )
