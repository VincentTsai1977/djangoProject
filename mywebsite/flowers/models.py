from django.db import models

# Create your models here.
# 引入 slugify 函數用於將文字轉換為 URL 友好的格式
from django.utils.text import slugify
# 引入 reverse 函數用於生成 URL 路徑
from django.urls import reverse

# 定義分類名稱欄位
class Category(models.Model):
    title = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.title
    
# 定義標籤名稱欄位
class Tag(models.Model):
    title = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.title
    
# 定義花卉名稱欄位
class Flower(models.Model):
    # 花卉名稱，最大長度255字元，預設為空字串
    title = models.CharField(max_length=255, default='')
    # 花卉描述，使用TextField可以儲存長文本，預設為空字串
    description = models.TextField(default='')
    # 用於URL的slug欄位，允許為空，預設為空字串
    slug = models.SlugField(blank=True, default='')
    # 外鍵關聯到Category模型，使用PROTECT保護策略防止刪除已被引用的分類，允許為空
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    # 多對多關係連接到Tag模型，一個花卉可以有多個標籤，一個標籤也可以用於多個花卉
    tags = models.ManyToManyField(Tag)
    # 圖片欄位，使用ImageField儲存圖片，允許為空
    image = models.ImageField(upload_to='flowers/', null=True, blank=True)
    # 價格欄位，使用DecimalField儲存價格，預設為0.00
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # 定義模型的字串表示方法，返回花卉名稱
    def __str__(self):
        return self.title

    # 重寫save方法，在保存對象前處理slug
    def save(self, *args, **kwargs):
        # 如果slug為空，則根據title自動生成一個URL友好的slug
        if not self.slug:
            self.slug = slugify(self.title)
        # 調用父類的save方法完成實際的保存操作
        super().save(*args, **kwargs)

    # 獲取對象的絕對URL，用於在模板中生成指向此花卉詳情頁的連結
    def get_absolute_url(self):
        # 使用reverse函數根據URL名稱'flower_detail'和slug參數生成URL
        return reverse('flower_detail', args=[str(self.slug)])

# 請說明null=True和blank=True的差異
# null=True表示該字段允許為空，即在資料庫中可以存儲NULL值
# blank=True表示該字段允許為空，即在表單中可以不填寫該字段的值
# 在這個模型中，category允許為空，slug允許為空
# 這樣設計的好處是，當我們在表單中不選擇分類時，不會報錯，而是會將category設為None
# 這樣設計的壞處是，當我們在表單中不填寫slug時，會報錯，因為slug是必填字段

# 請說明PROTECT的含義
# PROTECT表示在刪除引用此對象的對象時，會阻止刪除，而是會拋出ProtectedError錯誤