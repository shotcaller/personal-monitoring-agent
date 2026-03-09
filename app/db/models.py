# app/db/models.py
from sqlalchemy import (
    Column, String, Float, Integer, DateTime,
    Text, Boolean, JSON, UniqueConstraint
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

def gen_uuid():
    return str(uuid.uuid4())


class Resource(Base):
    """Every resource discovered across all subscriptions."""
    __tablename__ = "resources"

    id                  = Column(String, primary_key=True, default=gen_uuid)
    resource_id         = Column(String, nullable=False, unique=True)  # full Azure ARM resource ID
    name                = Column(String, nullable=False)
    resource_type       = Column(String, nullable=False)
    subscription_id     = Column(String, nullable=False)
    resource_group      = Column(String, nullable=False)
    location            = Column(String)
    owner_email         = Column(String)                 # from tags.owner
    team_name           = Column(String)                 # from tags.team
    environment         = Column(String)                 # from tags.env
    tags                = Column(JSON)                   # full tags blob
    last_seen_at        = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_at          = Column(DateTime, server_default=func.now())


class Finding(Base):
    """One open underutilisation finding per resource."""
    __tablename__ = "findings"

    id                      = Column(String, primary_key=True, default=gen_uuid)
    resource_id             = Column(String, nullable=False)   # FK to resources.resource_id
    resource_name           = Column(String, nullable=False)
    resource_type           = Column(String, nullable=False)
    subscription_id         = Column(String, nullable=False)
    resource_group          = Column(String, nullable=False)
    owner_email             = Column(String)
    team_name               = Column(String)
    environment             = Column(String)

    # finding detail
    severity                = Column(String, nullable=False)   # HIGH / MEDIUM / LOW
    reason_text             = Column(Text, nullable=False)     # GPT-generated plain English
    recommended_action      = Column(String)
    advisor_rec_id          = Column(String)                   # if Advisor flagged it
    advisor_flagged         = Column(Boolean, default=False)
    metrics_snapshot        = Column(JSON)                     # raw numbers at time of finding
    estimated_saving_usd    = Column(Float, default=0.0)       # potential $/month

    # lifecycle
    status                  = Column(String, default="OPEN")   # OPEN / ACTIONED / RESOLVED / IGNORED
    notified_at             = Column(DateTime)                 # set after Teams message sent
    created_at              = Column(DateTime, server_default=func.now())
    last_seen_at            = Column(DateTime, server_default=func.now())
    resolved_at             = Column(DateTime)

    __table_args__ = (
        # only one OPEN finding per resource at a time
        UniqueConstraint('resource_id', 'status',
                         name='uq_resource_open_finding'),
    )


class NotificationLog(Base):
    """Audit trail of every Teams message sent."""
    __tablename__ = "notification_log"

    id              = Column(String, primary_key=True, default=gen_uuid)
    finding_id      = Column(String, nullable=False)
    recipient       = Column(String)          # email or channel name
    channel         = Column(String)          # DM / WEBHOOK / FALLBACK
    payload         = Column(JSON)            # full card payload sent
    status          = Column(String)          # SENT / FAILED
    error_message   = Column(Text)
    sent_at         = Column(DateTime, server_default=func.now())


class SavingsSummary(Base):
    """Weekly roll-up snapshot for stakeholder reporting."""
    __tablename__ = "savings_summary"

    id                          = Column(String, primary_key=True, default=gen_uuid)
    week_ending                 = Column(String, nullable=False, unique=True)  # YYYY-MM-DD
    subscriptions_scanned       = Column(Integer, default=0)
    resources_scanned           = Column(Integer, default=0)
    total_open_findings         = Column(Integer, default=0)
    new_findings_this_week      = Column(Integer, default=0)
    findings_actioned           = Column(Integer, default=0)
    total_estimated_saving_usd  = Column(Float, default=0.0)   # potential (all OPEN)
    actioned_saving_usd         = Column(Float, default=0.0)   # committed (ACTIONED)
    top_team_by_waste           = Column(String)
    top_resource_type           = Column(String)
    gpt_exec_summary            = Column(Text)
    created_at                  = Column(DateTime, server_default=func.now())