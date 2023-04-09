"""create_main_tables
Revision ID: 03f067f6d106
Revises: 
Create Date: 2023-04-08 17:09:41.265525
"""
from alembic import op
import sqlalchemy as sa
# revision identifiers, used by Alembic
revision = '12345678654'
down_revision = None
branch_labels = None
depends_on = None
def create_carparks_table() -> None:
    op.create_table(
        "cleanCarparks",
        sa.Column("id", sa.Integer, index = True, autoincrement=True),
        sa.Column("cp_code", sa.String(5), primary_key=True, index=True),
        sa.Column("name", sa.Text),
        sa.Column("locations", sa.PickleType),
        sa.Column("rate", sa.Float),
        sa.Column("min", sa.Text),
    )
def upgrade() -> None:
    create_carparks_table()
def downgrade() -> None:
    op.drop_table("cleanCarparks")