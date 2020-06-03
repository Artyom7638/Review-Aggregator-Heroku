from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField

from src import Config


class PhotoUploadForm(FlaskForm):
    photo = FileField('Фото', description="Выбрать фото",
                      validators=[FileAllowed(Config.UPLOAD_EXTENSIONS,
                                             'Можно загружать только фотографии в форматах png, jpg, jpeg')])
    save = SubmitField('Сохранить')
