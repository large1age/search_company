import unittest
from unittest import mock

from application.models.db.company_model import ShortLinkORM
from application.models.db.connection import session
from application.services.short_link_port import (
    ShortLinkGenerateInput,
    ShortLinkGenerateKey,
    ShortLinkGenerateOutputStatus,
    ShortLinkRetrieveInput,
    ShortLinkRetrieveKey,
    ShortLinkRetrieveOutputStatus,
)
from application.services.short_link_usecase import ShortLinkUsecase


class BaseTestUsecase(unittest.TestCase):
    def setUp(self) -> None:
        super().__init__()
        self.sample_url = "http://ab180.io"
        self.non_protocol_sample_url = "ab180.io"
        self.invalid_sample_url = "ab180"

    def tearDown(self) -> None:
        session.query(ShortLinkORM).delete()
        session.commit()


class TestShortLinkUsecase(BaseTestUsecase):
    def setUp(self) -> None:
        super().setUp()

    def test_short_link_generate_should_ok(self):
        # Arrange
        key = ShortLinkGenerateKey()
        input_port_1 = ShortLinkGenerateInput(url=self.sample_url)
        input_port_2 = ShortLinkGenerateInput(url=self.non_protocol_sample_url)
        usecase = ShortLinkUsecase()

        # Act
        status_1, output_1 = usecase.generate(key=key, input_port=input_port_1)
        status_2, output_2 = usecase.generate(key=key, input_port=input_port_2)

        # Assert
        self.assertEqual(status_1, ShortLinkGenerateOutputStatus.SUCCESS)
        self.assertEqual(len(output_1.shortId), 11)
        self.assertEqual(status_2, ShortLinkGenerateOutputStatus.SUCCESS)
        self.assertEqual(len(output_2.shortId), 11)

    def test_short_link_generate_should_ok_and_short_id_is_different_form_same_url(
        self,
    ):
        # Arrange
        key = ShortLinkGenerateKey()
        input_port_1 = ShortLinkGenerateInput(url=self.sample_url)
        input_port_2 = ShortLinkGenerateInput(url=self.sample_url)
        usecase = ShortLinkUsecase()

        # Act
        status_1, output_1 = usecase.generate(key=key, input_port=input_port_1)
        status_2, output_2 = usecase.generate(key=key, input_port=input_port_2)

        # Assert
        self.assertEqual(status_1, ShortLinkGenerateOutputStatus.SUCCESS)
        self.assertEqual(len(output_1.shortId), 11)
        self.assertEqual(status_2, ShortLinkGenerateOutputStatus.SUCCESS)
        self.assertEqual(len(output_2.shortId), 11)

        self.assertNotEquals(output_1.shortId, output_2.shortId)

    def test_short_link_is_generate_should_raise_validate_error(self):
        # Arrange
        key = ShortLinkGenerateKey()
        input_port = ShortLinkGenerateInput(url=self.invalid_sample_url)
        usecase = ShortLinkUsecase()

        # Act
        status, output = usecase.generate(key=key, input_port=input_port)

        # Assert
        self.assertEqual(status, ShortLinkGenerateOutputStatus.VALIDATION_ERROR)
        self.assertIsNone(output)

    def test_short_link_is_generate_should_raise_conflict_error(self):
        # Arrange
        key = ShortLinkGenerateKey()
        input_port = ShortLinkGenerateInput(url=self.sample_url)
        usecase = ShortLinkUsecase()
        _, output = usecase.generate(key=key, input_port=input_port)

        # Act
        with mock.patch(
            "application.services.short_link_service.ShortLinkService._generate_short_id",
            return_value=output.shortId,
        ):
            status, output = usecase.generate(key=key, input_port=input_port)

        # Assert
        self.assertEqual(status, ShortLinkGenerateOutputStatus.CONFLICT_ERROR)
        self.assertIsNone(output)

    def test_short_link_retrieve_should_ok(self):
        # Arrange
        usecase = ShortLinkUsecase()
        _, output = usecase.generate(
            key=ShortLinkGenerateKey(),
            input_port=ShortLinkGenerateInput(url=self.sample_url),
        )
        key = ShortLinkRetrieveKey(shortId=output.shortId)
        input_port = ShortLinkRetrieveInput()

        # Act
        status, output = usecase.retrieve(key=key, input_port=input_port)

        # Assert
        self.assertEqual(status, ShortLinkRetrieveOutputStatus.SUCCESS)
        self.assertEqual(output.url, self.sample_url)

    def test_short_link_retrieve_should_raise_validation_error(self):
        # Arrange
        usecase = ShortLinkUsecase()
        _, output = usecase.generate(
            key=ShortLinkGenerateKey(),
            input_port=ShortLinkGenerateInput(url=self.sample_url),
        )
        key = ShortLinkRetrieveKey(shortId=output.shortId[0:10])
        input_port = ShortLinkRetrieveInput()

        # Act
        status, output = usecase.retrieve(key=key, input_port=input_port)

        # Assert
        self.assertEqual(status, ShortLinkRetrieveOutputStatus.VALIDATION_ERROR)
        self.assertIsNone(output)

    def test_short_link_retrieve_should_raise_not_found_error(self):
        # Arrange
        usecase = ShortLinkUsecase()
        _, output = usecase.generate(
            key=ShortLinkGenerateKey(),
            input_port=ShortLinkGenerateInput(url=self.sample_url),
        )
        key = ShortLinkRetrieveKey(shortId=output.shortId)
        input_port = ShortLinkRetrieveInput()

        session.query(ShortLinkORM).delete()
        session.commit()

        # Act
        status, output = usecase.retrieve(key=key, input_port=input_port)

        # Assert
        self.assertEqual(status, ShortLinkRetrieveOutputStatus.NOT_FOUND_ERROR)
        self.assertIsNone(output)
