import pytest
from unittest.mock import MagicMock, patch
from resources.importer_vpc_peering import VPCPeeringImporter  


@pytest.fixture
def mock_session():
    """Mock AWS boto3 session"""
    return MagicMock()


def test_name_and_description():
    importer = VPCPeeringImporter()
    assert importer.name() == "vpc_peering"
    assert importer.description() == "Imports VPC Peering Connections"
    assert importer.menu_name() == "VPC Peering"


@patch.object(VPCPeeringImporter, "save")
def test_run_calls_save(mock_save, mock_session, tmp_path):
    importer = VPCPeeringImporter(path=str(tmp_path))

    # Mock EC2 client y paginator
    mock_ec2 = MagicMock()
    mock_paginator = MagicMock()
    mock_session.client.return_value = mock_ec2
    mock_ec2.get_paginator.return_value = mock_paginator

    # Simular 2 páginas de resultados
    mock_paginator.paginate.return_value = [
        {"VpcPeeringConnections": [{"VpcPeeringConnectionId": "pcx-123"}]},
        {"VpcPeeringConnections": [{"VpcPeeringConnectionId": "pcx-456"}]},
    ]

    # Ejecutar
    importer.run(
        session=mock_session,
        acc_id="111111111111",
        acc_name="dev",
        region="us-east-1",
    )

    # Validar llamadas a boto3
    mock_session.client.assert_called_once_with("ec2", region_name="us-east-1")
    mock_ec2.get_paginator.assert_called_once_with("describe_vpc_peering_connections")
    mock_paginator.paginate.assert_called_once()

    # Validar que combine resultados
    expected_data = [
        {"VpcPeeringConnectionId": "pcx-123"},
        {"VpcPeeringConnectionId": "pcx-456"},
    ]

    # Validar llamada a save()
    mock_save.assert_called_once_with("111111111111", "dev", expected_data)
