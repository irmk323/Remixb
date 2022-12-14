from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField,DateField,SelectField,ValidationError
from wtforms.validators import DataRequired, Email,Regexp,InputRequired
from wtforms import (EmailField, PasswordField, BooleanField,MultipleFileField,
   SubmitField, StringField ,TextAreaField)

message_required="この項目は必須項目です。"

class LoginForm(FlaskForm):

   email = EmailField('Email address', validators=[DataRequired(), Email()])
   password = PasswordField('Password', validators=[DataRequired()])
   remember_me = BooleanField('Remember me')
   submit = SubmitField('Sign in')

class RegisterForm(FlaskForm):

   username = StringField('Username')
   email = EmailField('Email', validators=[DataRequired(), Email()])
   password = PasswordField('Password', validators=[DataRequired()])
   submit = SubmitField('Register')

class MessageForm(FlaskForm):

    message = TextAreaField('Message:', validators=[DataRequired()])
    submit = SubmitField('Submit')
   
class NewpostForm(FlaskForm):
   title = StringField('タイトル', validators=[DataRequired(message=message_required)])
   detail = TextAreaField('詳細', validators=[DataRequired(message=message_required)])
   monthly_rent = StringField('家賃', validators=[Regexp("^[0-9]+$" ,message="半角数字で入力してください"),DataRequired(message=message_required)])
   is_bill_included = BooleanField('光熱費込み',render_kw={'value': 'True'}, false_values={False, 'false', ''})
   # deposit = StringField('デポジット', validators=[Regexp("^[a-zA-Z0-9]+$")])
   deposit = StringField('デポジット', validators=[Regexp("^[0-9]+$" ,message="半角数字で入力してください"),DataRequired(message=message_required)])
   start_date = DateField('入居可能日',validators=[InputRequired(message="入居可能開始日を入力してください")])
   room_type = SelectField('部屋タイプ', choices=[('flat', 'フラットルーム'), ('studio', 'スタジオ'), ('rent', '賃貸物件')])
   duration = SelectField('滞在期間', choices=[('0', '指定なし'), ('1', '1ヶ月以内'), ('3', '3ヶ月以内'), ('6', '6ヶ月以内'),('12', '1年以内'),('24', '2年以内'),('25', 'それ以上')])
   is_furnished = SelectField('家具', choices=[('True', '有り'), ('False', '無し')],coerce=lambda x: True if x == 'True' else False)
   gender = SelectField('性別', choices=[('both', '指定無し'), ('female', '女性'), ('male', '男性')])
   is_smorkable = SelectField('喫煙', choices=[('True', '可'), ('False', '不可')],coerce=lambda x: True if x == 'True' else False)
   with_landload = SelectField('大家', choices=[('False', '別居'),('True', '同居')], validators=[InputRequired()],coerce=lambda x: True if x == 'True' else False)
   picture = MultipleFileField('Update Profile Pic')
   submit = SubmitField('投稿する')

   def validate_title(self, title):
      if len(title.data) < 5:
         raise ValidationError("タイトルを5文字以上入力してください")
      
   # def validate_tags(self, tags):
   #    tag_list = tags.data.strip().split(",")
   #    if len(tag_list) > 3:
   #       raise ValidationError("タグは3つ以下にしてください。")