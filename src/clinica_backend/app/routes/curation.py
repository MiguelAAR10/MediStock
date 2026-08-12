from flask import Blueprint, request

from app.services.data_curation_service import DataCurationService
from app.utils.response import APIResponse


curation_bp = Blueprint("curation", __name__)


@curation_bp.route("/curation/paciente-preview", methods=["POST"])
def preview_paciente_curation():
    json_data = request.get_json() or {}
    result = DataCurationService.curate_paciente_payload(json_data)
    return APIResponse.success(data=result)


@curation_bp.route("/curation/consulta-preview", methods=["POST"])
def preview_consulta_curation():
    json_data = request.get_json() or {}
    result = DataCurationService.curate_consulta_payload(json_data)
    return APIResponse.success(data=result)


@curation_bp.route("/curation/quality", methods=["GET"])
def quality_snapshot():
    try:
        result = DataCurationService.data_quality_snapshot()
        return APIResponse.success(data=result)
    except Exception as e:
        return APIResponse.error(str(e), status_code=500)
