from datetime import datetime
from io import BytesIO

from django.test import TestCase
from django.core.files import File
from PIL import Image as ImagePIL

from webapp.core.forms import ImageForm
from webapp.core.models import Image


def get_image_file(name, ext='png', size=(50, 50), color=(256, 0, 0)):
    file_obj = BytesIO()

    image = ImagePIL.new('RGBA', size=size, color=color)
    image.save(file_obj, ext)

    file_obj.seek(0)

    return File(file_obj, name=name)


class ImageFormTest(TestCase):
    def setUp(self):
        self.form = ImageForm()

    def test_form_has_fields(self):
        """Form must have 2 fields"""
        expected = ['name', 'image']
        self.assertSequenceEqual(expected, list(self.form.fields))


class ImageModelTest(TestCase):
    def setUp(self):
        self.obj = Image(
            name='blue',
            image=get_image_file('image.png')
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Image.objects.exists())

    def test_created_at(self):
        """Image must have an auto create attr."""
        self.assertIsInstance(self.obj.uploaded_at, datetime)


class ImageViews(TestCase):
    def setUp(self):
        self.obj = Image(
            name='blue',
            image=get_image_file('image.png')
        )
        self.obj.save()

        self.resp = self.client.get(f'/img/blue/')

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/render_image.html')

    def test_context(self):
        image = self.resp.context['image']
        self.assertIsInstance(image, Image)

    def test_html(self):
        contents = (self.obj.name, self.obj.image)

        with self.subTest():
            for expected in contents:
                self.assertContains(self.resp, expected)


class ImageViewsNotFound(TestCase):
    def test_not_found(self):
        resp = self.client.get('/img/red/')
        self.assertEqual(404, resp.status_code)
