from aerich.models import Model
from aerich.models import fields


class User(Model):
    user_id = fields.IntField(pk=True)
    name = fields.CharField(max_length=15)
    openid = fields.CharField(max_length=128)


class Ingredient(Model):
    ingredient_id = fields.IntField(pk=True)
    chinese_name = fields.CharField(max_length=255, unique=True, description="中文名")
    ping_yin = fields.CharField(max_length=255, null=True, description="拼音")
    english_name = fields.CharField(max_length=255, unique=True, description="英文名")
    introduction = fields.TextField(description="简介")
    effects = fields.TextField(description="功效")
    rating = fields.FloatField(description="评分")
    potential_risk_people = fields.CharField(max_length=255, null=True, description="潜在风险人群")
    daily_intake_recommendation = fields.TextField(description="每日建议摄入量")


class Favorites(Model):
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE, related_name="favorites", description="用户id")
    favorites_id = fields.IntField(pk=True, description="收藏夹id")
    note = fields.CharField(max_length=255, default="这是一条历史记录", description="备注")
    ingredient = fields.ManyToManyField("models.Ingredient", on_delete=fields.CASCADE, related_name="favorites_ingredient")


class History(Model):
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE, related_name="history", description="用户id")
    image_url = fields.CharField(max_length=256, default=None, description="图片url")
    history_id = fields.IntField(pk=True, description="收藏夹id")
    date = fields.DateField(auto_now_add=True, generated=True, description="历史记录的时间")
    ingredient = fields.ManyToManyField("models.Ingredient", on_delete=fields.CASCADE, related_name="history_ingredient")
