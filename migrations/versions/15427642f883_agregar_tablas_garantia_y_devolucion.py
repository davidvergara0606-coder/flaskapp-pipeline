"""agregar tablas garantia y devolucion

Revision ID: 15427642f883
Revises: 5cc1197b8c7f
Create Date: 2026-09-15 14:52:10.205038

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = "15427642f883"
down_revision = "5cc1197b8c7f"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "devolucion",
        sa.Column("id_devolucion", sa.Integer(), nullable=False),
        sa.Column("id_producto", sa.Integer(), nullable=False),
        sa.Column("observacion", sa.String(length=255), nullable=False),
        sa.Column("fecha", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["id_producto"],
            ["producto.id_producto"],
        ),
        sa.PrimaryKeyConstraint("id_devolucion"),
    )
    op.create_table(
        "garantia",
        sa.Column("id_garantia", sa.Integer(), nullable=False),
        sa.Column("id_producto", sa.Integer(), nullable=False),
        sa.Column("observacion", sa.String(length=255), nullable=False),
        sa.Column("fecha", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["id_producto"],
            ["producto.id_producto"],
        ),
        sa.PrimaryKeyConstraint("id_garantia"),
    )
    with op.batch_alter_table("alerta", schema=None) as batch_op:
        batch_op.alter_column(
            "mensaje",
            existing_type=mysql.TEXT(),
            type_=sa.String(length=255),
            nullable=False,
        )
        batch_op.alter_column(
            "id_producto", existing_type=mysql.INTEGER(display_width=11), nullable=False
        )

    with op.batch_alter_table("movimiento", schema=None) as batch_op:
        batch_op.alter_column(
            "tipo_movimiento",
            existing_type=mysql.ENUM("ENTRADA", "SALIDA", "AJUSTE"),
            type_=sa.String(length=50),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "descripcion",
            existing_type=mysql.VARCHAR(length=200),
            type_=sa.String(length=255),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "id_usuario", existing_type=mysql.INTEGER(display_width=11), nullable=False
        )

    with op.batch_alter_table("producto", schema=None) as batch_op:
        batch_op.alter_column(
            "nombre",
            existing_type=mysql.VARCHAR(length=150),
            type_=sa.String(length=100),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "stock_actual",
            existing_type=mysql.INTEGER(display_width=11),
            nullable=False,
            existing_server_default=sa.text("0"),
        )
        batch_op.alter_column(
            "stock_minimo",
            existing_type=mysql.INTEGER(display_width=11),
            nullable=False,
            existing_server_default=sa.text("5"),
        )
        batch_op.alter_column(
            "id_categoria",
            existing_type=mysql.INTEGER(display_width=11),
            nullable=False,
        )

    with op.batch_alter_table("proveedor", schema=None) as batch_op:
        batch_op.alter_column(
            "nombre",
            existing_type=mysql.VARCHAR(length=150),
            type_=sa.String(length=100),
            existing_nullable=False,
        )

    with op.batch_alter_table("usuario", schema=None) as batch_op:
        batch_op.alter_column(
            "tipo_documento",
            existing_type=mysql.ENUM("CC", "CE", "NIT", "PP"),
            type_=sa.String(length=20),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "documento",
            existing_type=mysql.VARCHAR(length=20),
            type_=sa.String(length=50),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "correo",
            existing_type=mysql.VARCHAR(length=255),
            type_=sa.String(length=100),
            nullable=False,
        )
        batch_op.alter_column(
            "id_rol", existing_type=mysql.INTEGER(display_width=11), nullable=False
        )


def downgrade():
    with op.batch_alter_table("usuario", schema=None) as batch_op:
        batch_op.alter_column(
            "id_rol", existing_type=mysql.INTEGER(display_width=11), nullable=True
        )
        batch_op.alter_column(
            "correo",
            existing_type=sa.String(length=100),
            type_=mysql.VARCHAR(length=255),
            nullable=True,
        )
        batch_op.alter_column(
            "documento",
            existing_type=sa.String(length=50),
            type_=mysql.VARCHAR(length=20),
            existing_nullable=False,
        )
        batch_op.alter_column(
            "tipo_documento",
            existing_type=sa.String(length=20),
            type_=mysql.ENUM("CC", "CE", "NIT", "PP"),
            existing_nullable=False,
        )

    with op.batch_alter_table("proveedor", schema=None) as batch_op:
        batch_op.alter_column(
            "nombre",
            existing_type=sa.String(length=100),
            type_=mysql.VARCHAR(length=150),
            existing_nullable=False,
        )

    with op.batch_alter_table("producto", schema=None) as batch_op:
        batch_op.alter_column(
            "id_categoria", existing_type=mysql.INTEGER(display_width=11), nullable=True
        )
        batch_op.alter_column(
            "stock_minimo",
            existing_type=mysql.INTEGER(display_width=11),
            nullable=True,
            existing_server_default=sa.text("5"),
        )
        batch_op.alter_column(
            "stock_actual",
            existing_type=mysql.INTEGER(display_width=11),
            nullable=True,
            existing_server_default=sa.text("0"),
        )
        batch_op.alter_column(
            "nombre",
            existing_type=sa.String(length=100),
            type_=mysql.VARCHAR(length=150),
            existing_nullable=False,
        )

    with op.batch_alter_table("movimiento", schema=None) as batch_op:
        batch_op.alter_column(
            "id_usuario", existing_type=mysql.INTEGER(display_width=11), nullable=True
        )
        batch_op.alter_column(
            "descripcion",
            existing_type=sa.String(length=255),
            type_=mysql.VARCHAR(length=200),
            existing_nullable=True,
        )
        batch_op.alter_column(
            "tipo_movimiento",
            existing_type=sa.String(length=50),
            type_=mysql.ENUM("ENTRADA", "SALIDA", "AJUSTE"),
            existing_nullable=False,
        )

    with op.batch_alter_table("alerta", schema=None) as batch_op:
        batch_op.alter_column(
            "id_producto", existing_type=mysql.INTEGER(display_width=11), nullable=True
        )
        batch_op.alter_column(
            "mensaje",
            existing_type=sa.String(length=255),
            type_=mysql.TEXT(),
            nullable=True,
        )

    op.drop_table("garantia")
    op.drop_table("devolucion")
