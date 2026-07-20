from enum import StrEnum
from pydantic import BaseModel


class SectorType(StrEnum):
    TECHNICAL_SECTION = "technical_section"
    ACADEMIC_SECTION = "academic_section"
    AUXILIARY_SECTION = "auxiliary_section"
    CHILDCARE_CENTER = "childcare_center"
    IT_DIRECTORATE = "it_directorate"


class SourceType(StrEnum):
    WEB_PAGE = "web_page"
    UPLOADED_DOCUMENT = "uploaded_document"


class SourceStatus(StrEnum):
    ACTIVE = "active"
    UNAVAILABLE = "unavailable"
    OUTDATED = "outdated"
    REVOKED = "revoked"


class DocumentStatus(StrEnum):
    ACTIVE = "active"
    REPLACED = "replaced"
    DEACTIVATED = "deactivated"


class SectorConfig(BaseModel):
    id: str
    name: str
    type: SectorType
    parent_id: str | None = None
    url_path: str | None = None


SECTORS: list[SectorConfig] = [
    SectorConfig(id="st-gp", name="Seção Técnica de Gestão de Pessoas", type=SectorType.TECHNICAL_SECTION),
    SectorConfig(id="st-com", name="Seção Técnica de Comunicações", type=SectorType.TECHNICAL_SECTION),
    SectorConfig(id="st-cont", name="Seção Técnica de Contabilidade", type=SectorType.TECHNICAL_SECTION),
    SectorConfig(id="st-fin", name="Seção Técnica de Finanças", type=SectorType.TECHNICAL_SECTION),
    SectorConfig(id="st-mat", name="Seção Técnica de Materiais", type=SectorType.TECHNICAL_SECTION),
    SectorConfig(id="st-sau", name="Seção Técnica de Saúde", type=SectorType.TECHNICAL_SECTION),
    SectorConfig(id="st-ted", name="Seção Técnica de Triagem, Emergência e Documentação", type=SectorType.TECHNICAL_SECTION),
    SectorConfig(id="cei", name="Centro de Educação Infantil", type=SectorType.CHILDCARE_CENTER),
    SectorConfig(id="sta", name="Seção Técnica Acadêmica", type=SectorType.ACADEMIC_SECTION),
    SectorConfig(id="st-grad", name="Seção Técnica de Graduação", type=SectorType.ACADEMIC_SECTION),
    SectorConfig(id="st-pos", name="Seção Técnica de Pós-Graduação", type=SectorType.ACADEMIC_SECTION),
    SectorConfig(id="st-apepe", name="Seção Técnica de Apoio ao Ensino, Pesquisa e Extensão", type=SectorType.ACADEMIC_SECTION),
    SectorConfig(id="saa", name="Seção de Atividades Auxiliares", type=SectorType.AUXILIARY_SECTION),
    SectorConfig(id="scm", name="Seção de Conservação e Manutenção", type=SectorType.AUXILIARY_SECTION),
    SectorConfig(id="dti", name="Diretoria Técnica de Informática", type=SectorType.IT_DIRECTORATE),
]
