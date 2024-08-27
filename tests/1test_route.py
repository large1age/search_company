import json
import unittest

from application.routes import app
from application.services.short_link_port import (
    ShortLinkGenerateInput,
    ShortLinkGenerateKey,
)
from application.services.short_link_usecase import ShortLinkUsecase
from tests.test_usecase import BaseTestUsecase


class TestShortLinkAPI(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.app = app.test_client()
        self.app.testing = True

    def test_get_api_should_return_302(self):
        # Arrange
        usecase = ShortLinkUsecase()
        _, output = usecase.generate(
            key=ShortLinkGenerateKey(),
            input_port=ShortLinkGenerateInput(url=self.sample_url),
        )

        # Act
        response = self.app.get(f"/short-links/{output.shortId}")
        data = json.loads(response.get_data(as_text=True))

        # Assert

        self.assertEqual(response.status_code, 302)
        self.assertIsInstance(data["data"], dict)

    def test_post_api_should_return_201(self):
        # Arrange
        pass

        # Act
        response = self.app.post(
            "/short-links",
            json={"url": self.sample_url},
        )
        data = json.loads(response.get_data(as_text=True))

        # Assert
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(data, dict)
