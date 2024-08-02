from flask import Blueprint, request, jsonify
from app.models import Guide, GuideSchema
from app import db

bp = Blueprint('guides', __name__)

guide_schema = GuideSchema()
guides_schema = GuideSchema(many=True)

@bp.route('/guide', methods=["POST"])
def add_guide():
    title = request.json['title']
    content = request.json['content']

    new_guide = Guide(title, content)

    db.session.add(new_guide)
    db.session.commit()

    guide = Guide.query.get(new_guide.id)

    return guide_schema.jsonify(guide)

@bp.route('/guides', methods=["GET"])
def all_guides():
    all_guides = Guide.query.all()
    result = guides_schema.dump(all_guides)
    
    return jsonify(result)

@bp.route("/guide/<id>", methods=["GET"])
def get_guide(id):
    guide = Guide.query.get(id)

    return guide_schema.jsonify(guide)

