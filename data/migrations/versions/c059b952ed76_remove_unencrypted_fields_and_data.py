"""Remove unencrypted fields and data

Revision ID: c059b952ed76
Revises: 49e1138ed12d
Create Date: 2019-08-19 16:31:00.952773

"""

# revision identifiers, used by Alembic.
revision = "c059b952ed76"
down_revision = "49e1138ed12d"

import logging
import uuid

from alembic import op as original_op
from data.migrations.progress import ProgressWrapper
import sqlalchemy as sa

from data.database import FederatedLogin, User, RobotAccountToken


logger = logging.getLogger(__name__)


def upgrade(tables, tester, progress_reporter):
    op = ProgressWrapper(original_op, progress_reporter)
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("oauthaccesstoken_refresh_token", table_name="oauthaccesstoken")
    op.drop_column(u"oauthaccesstoken", "refresh_token")

    op.drop_column("accesstoken", "code")

    op.drop_column("appspecificauthtoken", "token_code")

    op.drop_column("oauthaccesstoken", "access_token")
    op.drop_column("oauthapplication", "client_secret")

    op.drop_column("oauthauthorizationcode", "code")

    op.drop_column("repositorybuildtrigger", "private_key")
    op.drop_column("repositorybuildtrigger", "auth_token")
    # ### end Alembic commands ###

    # Overwrite all plaintext robot credentials.
    from app import app

    if app.config.get("SETUP_COMPLETE", False) or tester.is_testing():
        while True:
            try:
                robot_account_token = RobotAccountToken.get(fully_migrated=False)
                logger.debug("Found robot account token %s migrate", robot_account_token.id)

                robot_account = robot_account_token.robot_account
                assert robot_account.robot

                result = (
                    User.update(email=str(uuid.uuid4()))
                    .where(
                        User.id == robot_account.id,
                        User.robot == True,
                        User.uuid == robot_account.uuid,
                    )
                    .execute()
                )
                assert result == 1

                federated_login = FederatedLogin.get(user=robot_account)
                federated_login.service_ident = "robot:%s" % robot_account.id
                federated_login.save()

                robot_account_token.fully_migrated = True
                robot_account_token.save()

                logger.debug("Finished migrating robot account token %s", robot_account_token.id)
            except RobotAccountToken.DoesNotExist:
                break


def downgrade(tables, tester, progress_reporter):
    op = ProgressWrapper(original_op, progress_reporter)
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        u"oauthaccesstoken", sa.Column("refresh_token", sa.String(length=255), nullable=True)
    )
    op.create_index(
        "oauthaccesstoken_refresh_token", "oauthaccesstoken", ["refresh_token"], unique=False
    )

    op.add_column(
        "repositorybuildtrigger", sa.Column("auth_token", sa.String(length=255), nullable=True)
    )
    op.add_column("repositorybuildtrigger", sa.Column("private_key", sa.Text(), nullable=True))

    op.add_column("oauthauthorizationcode", sa.Column("code", sa.String(length=255), nullable=True))
    op.create_index("oauthauthorizationcode_code", "oauthauthorizationcode", ["code"], unique=True)

    op.add_column(
        "oauthapplication", sa.Column("client_secret", sa.String(length=255), nullable=True)
    )
    op.add_column(
        "oauthaccesstoken", sa.Column("access_token", sa.String(length=255), nullable=True)
    )

    op.create_index(
        "oauthaccesstoken_access_token", "oauthaccesstoken", ["access_token"], unique=False
    )

    op.add_column(
        "appspecificauthtoken", sa.Column("token_code", sa.String(length=255), nullable=True)
    )
    op.create_index(
        "appspecificauthtoken_token_code", "appspecificauthtoken", ["token_code"], unique=True
    )

    op.add_column("accesstoken", sa.Column("code", sa.String(length=255), nullable=True))
    op.create_index("accesstoken_code", "accesstoken", ["code"], unique=True)
    # ### end Alembic commands ###
