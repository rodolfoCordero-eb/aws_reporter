
import pytest
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError
from src.sessions.org_sessions import OrgSession  


@pytest.fixture
def mock_boto3_session():
    """Mock for boto3.Session()."""
    mock_session = MagicMock()
    mock_session.client.return_value = MagicMock()
    return mock_session


@pytest.fixture
def mock_boto3_clients():
    """Mocks for boto3 clients: sts and organizations."""
    mock_sts = MagicMock()
    mock_org = MagicMock()

    # Simulate get_caller_identity() response
    mock_sts.get_caller_identity.return_value = {"Account": "111111111111"}

    # Simulate list_accounts paginator
    paginator = MagicMock()
    paginator.paginate.return_value = [
        {"Accounts": [
            {"Id": "111111111111", "Name": "Main", "Status": "ACTIVE"},
            {"Id": "222222222222", "Name": "Finance", "Status": "SUSPENDED"},
            {"Id": "333333333333", "Name": "Dev", "Status": "ACTIVE"},
        ]}
    ]
    mock_org.get_paginator.return_value = paginator
    return mock_sts, mock_org


@patch("src.sessions.org_sessions.boto3")  # ← replace 'src.sessions.org_sessions' with the actual module name
def test_init_list_accounts(mock_boto3, mock_boto3_clients):
    """Verify that OrgSession initializes correctly and only lists ACTIVE accounts."""
    mock_sts, mock_org = mock_boto3_clients
    mock_boto3.client.side_effect = lambda service: mock_org if service == "organizations" else mock_sts
    mock_boto3.Session.return_value = MagicMock()

    org_session = OrgSession()

    assert len(org_session.accounts) == 2
    assert all(acc["Status"] == "ACTIVE" for acc in org_session.accounts)
    mock_org.get_paginator.assert_called_once_with("list_accounts")


@patch("src.sessions.org_sessions.boto3")
def test_assume_role_success(mock_boto3, mock_boto3_clients):
    """Verify that assume_role returns a new session with simulated credentials."""
    mock_sts, mock_org = mock_boto3_clients
    mock_sts.assume_role.return_value = {
        "Credentials": {
            "AccessKeyId": "FAKEKEY",
            "SecretAccessKey": "FAKESECRET",
            "SessionToken": "FAKETOKEN",
        }
    }
    mock_boto3.client.side_effect = lambda service: mock_org if service == "organizations" else mock_sts
    mock_boto3.Session.return_value = MagicMock()

    org_session = OrgSession()
    new_session = org_session.assume_role("333333333333", "OrganizationAccountAccessRole")

    mock_sts.assume_role.assert_called_once()
    mock_boto3.Session.assert_called_with(
        aws_access_key_id="FAKEKEY",
        aws_secret_access_key="FAKESECRET",
        aws_session_token="FAKETOKEN",
    )
    assert new_session is not None


@patch("src.sessions.org_sessions.boto3")
def test_assume_role_same_account_returns_default(mock_boto3, mock_boto3_clients):
    """If the account ID is the same as the current account, it should return the default session."""
    mock_sts, mock_org = mock_boto3_clients
    mock_boto3.client.side_effect = lambda service: mock_org if service == "organizations" else mock_sts
    mock_boto3.Session.return_value = MagicMock()

    org_session = OrgSession()
    session = org_session.assume_role("111111111111", "OrganizationAccountAccessRole")

    assert session == org_session.session_default


@patch("src.sessions.org_sessions.boto3")
def test_assume_role_client_error(mock_boto3, mock_boto3_clients):
    """Verify that assume_role returns None when a ClientError is raised."""
    mock_sts, mock_org = mock_boto3_clients
    mock_sts.assume_role.side_effect = ClientError(
        {"Error": {"Code": "AccessDenied", "Message": "Not authorized"}},
        "AssumeRole"
    )
    mock_boto3.client.side_effect = lambda service: mock_org if service == "organizations" else mock_sts
    mock_boto3.Session.return_value = MagicMock()

    org_session = OrgSession()
    session = org_session.assume_role("333333333333", "OrganizationAccountAccessRole")

    assert session is None

