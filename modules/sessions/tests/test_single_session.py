import pytest
from unittest.mock import MagicMock, patch
from src.sessions.single_session import SingleSession

@pytest.fixture
def mock_boto3_session():
    """Mock de boto3.session.Session"""
    session = MagicMock()
    sts_client = MagicMock()
    org_client = MagicMock()

    # Mock de respuestas de AWS
    sts_client.get_caller_identity.return_value = {
        "UserId": "AIDAEXAMPLEUSER",
        "Account": "123456789012"
    }
    org_client.describe_account.return_value = {
        "Account": {"Name": "example-account"}
    }

    session.client.side_effect = lambda service: {
        "sts": sts_client,
        "organizations": org_client
    }[service]

    return session


def test_set_caller_identity(mock_boto3_session):
    ss = SingleSession(mock_boto3_session)
    identity = ss.set_caller_identity()

    assert identity["Account"] == "123456789012"
    assert ss.account_id == "123456789012"
    assert ss.account_name == "example-account"
    assert ss.userId == "AIDAEXAMPLEUSER"


def test_get_account_info(mock_boto3_session):
    ss = SingleSession(mock_boto3_session)
    ss.set_caller_identity()

    info = ss.get_account_info()
    assert info == {
        "account_id": "123456789012",
        "account_name": "example-account",
        "user_id": "AIDAEXAMPLEUSER"
    }




def test_run_analycer(mock_boto3_session):
    ss = SingleSession(mock_boto3_session)
    ss.set_caller_identity()

    analycer = MagicMock()
    analycer.name.return_value = "test_analycer"

    ss.run_analycer(analycer, "/tmp/output")

    analycer.run.assert_called_once_with(
        {
            "account_id": "123456789012",
            "account_name": "example-account"
        },
        "test_analycer",
        "/tmp/output"
    )


def test_run_exporter(mock_boto3_session):
    ss = SingleSession(mock_boto3_session)
    ss.set_caller_identity()

    exporter = MagicMock()
    exporter.name.return_value = "test_exporter"

    ss.run_exporter(exporter)

    exporter.run.assert_called_once_with(
        {
            "account_id": "123456789012",
            "account_name": "example-account"
        },
        "test_exporter"
    )


def test_run_in_all_regions(mock_boto3_session):
    # Create SingleSession mock with basic identity
    ss = SingleSession(mock_boto3_session)
    ss.set_caller_identity()

    # Mock methods used inside run_in_all_regions
    ss.get_regions = MagicMock(return_value=["us-east-1", "us-west-2"])
    ss.run_importer = MagicMock()

    importer = MagicMock()
    importer.name.return_value = "test_importer"

    # Run the method
    ss.run_in_all_regions(importer)

    # Validate get_regions was called once
    ss.get_regions.assert_called_once()

    # Validate run_importer was called for each region
    ss.run_importer.assert_any_call(importer, "us-east-1")
    ss.run_importer.assert_any_call(importer, "us-west-2")
    assert ss.run_importer.call_count == 2
