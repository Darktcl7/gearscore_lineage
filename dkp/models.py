from django.db import models
from django.utils import timezone
from items.models import Character
from django.contrib.auth.models import User

class DKPProfile(models.Model):
    character = models.OneToOneField(Character, on_delete=models.CASCADE, related_name='dkp_profile')
    current_dkp = models.IntegerField("Current DKP", default=0)
    total_earned = models.IntegerField("Total Earned (Lifetime)", default=0)
    last_decay_percent = models.FloatField("Last Decay %", default=0, blank=True)
    
    def __str__(self):
        return f"{self.character.name} - {self.current_dkp} DKP"

    class Meta:
        verbose_name = "DKP Profile"

class DKPEvent(models.Model):
    name = models.CharField("Nama Event", max_length=200)
    date = models.DateTimeField("Tanggal", default=timezone.now)
    
    is_active = models.BooleanField("Open Check-in", default=True) 
    is_closed = models.BooleanField("Check-in Closed", default=False)
    is_finalized = models.BooleanField("Points Distributed", default=False)
    is_war_day = models.BooleanField("War Day", default=False)
    
    points_to_award = models.IntegerField("Points Reward", default=10)
    
    description = models.TextField(blank=True)
    note = models.TextField("Catatan", blank=True, default='')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.date.strftime('%d/%m/%Y')})"

class DKPAttendance(models.Model):
    event = models.ForeignKey(DKPEvent, on_delete=models.CASCADE, related_name='attendances')
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField("Verified", default=False)
    
    class Meta:
        unique_together = ('event', 'character')
        verbose_name = "DKP Attendance"

class DKPLog(models.Model):
    profile = models.ForeignKey(DKPProfile, on_delete=models.CASCADE, related_name='logs')
    amount = models.IntegerField("Jumlah")
    reason = models.CharField("Alasan", max_length=255)
    note = models.TextField("Catatan", blank=True, default='')
    is_war_day = models.BooleanField("War Day", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.profile.character.name}: {self.amount} ({self.reason})"

class BossPointConfig(models.Model):
    """Singleton model to store boss point settings in database (synced across all clients)"""
    config = models.JSONField("Boss Points Config", default=dict)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Boss Point Config"

    def __str__(self):
        return f"Boss Point Config (updated: {self.updated_at})"

    @classmethod
    def get_config(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={'config': {}})
        return obj


class AdminRole(models.Model):
    """Granular admin permissions per user"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_role')
    is_dkp_admin = models.BooleanField("DKP Admin", default=False,
        help_text="Full access to DKP system (Add, Remove, Decay, etc.)")
    is_event_admin = models.BooleanField("Event Admin", default=False,
        help_text="Access to Activity Events management")
    is_treasury_admin = models.BooleanField("Treasury Admin", default=False,
        help_text="Access to Treasury item distribution and DKP deduction")
    is_auction_admin = models.BooleanField("Auction Admin", default=False,
        help_text="Access to future Auction system")
        
    # Granular DKP Admin controls
    can_give_dkp = models.BooleanField("Can Give DKP", default=False)
    can_remove_dkp = models.BooleanField("Can Remove DKP", default=False)
    can_decay_dkp = models.BooleanField("Can Decay DKP", default=False)

    class Meta:
        verbose_name = "Admin Role"

    def __str__(self):
        roles = []
        if self.is_dkp_admin: roles.append("DKP")
        if self.is_treasury_admin: roles.append("Treasury")
        if self.is_auction_admin: roles.append("Auction")
        return f"{self.user.username} - [{', '.join(roles) or 'No Roles'}]"


class TreasuryItemConfig(models.Model):
    """Singleton model to store treasury item pricing/limits (like BossPointConfig)"""
    config = models.JSONField("Treasury Items Config", default=dict)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Treasury Item Config"

    def __str__(self):
        return f"Treasury Item Config (updated: {self.updated_at})"

    @classmethod
    def get_config(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={'config': cls.get_default_config()})
        # Auto-migrate old flat config to clan-nested config
        if obj.config and 'blue_books' in obj.config and 'Valkyrie' not in obj.config:
            old_config = obj.config.copy()
            obj.config = {
                'Valkyrie': old_config,
                'Valhalla': {
                    'blue_books': [],
                    'blue_equipment': [],
                    'other_items': [],
                    'diamond_items': [],
                }
            }
            obj.save()
        return obj

    @classmethod
    def get_default_config(cls):
        default_items = {
            "blue_books": [
                {"name": "Standard Book", "price": 50, "currency": "DKP", "max_per_person": 0, "category": "blue_books"},
                {"name": "Advanced Book", "price": 75, "currency": "DKP", "max_per_person": 0, "category": "blue_books"},
                {"name": "High-Class Book (Group Heal)", "price": 200, "currency": "DKP", "max_per_person": 0, "category": "blue_books"},
                {"name": "High-Class Book (War Frenzy)", "price": 200, "currency": "DKP", "max_per_person": 0, "category": "blue_books"},
                {"name": "High-Class Book (Crowd Control)", "price": 150, "currency": "DKP", "max_per_person": 0, "category": "blue_books"},
                {"name": "Rare Book (Class Skill)", "price": 125, "currency": "DKP", "max_per_person": 0, "category": "blue_books"},
            ],
            "blue_equipment": [
                {"name": "Blue Accessory (Ring/Earring/Necklace)", "price": 25, "currency": "DKP", "max_per_person": 2, "category": "blue_equipment"},
                {"name": "Blue Sigil", "price": 25, "currency": "DKP", "max_per_person": 2, "category": "blue_equipment"},
                {"name": "Blue Armor Set (Helmet)", "price": 50, "currency": "DKP", "max_per_person": 1, "category": "blue_equipment"},
                {"name": "Blue Armor Set (Armor)", "price": 75, "currency": "DKP", "max_per_person": 1, "category": "blue_equipment"},
                {"name": "Blue Armor Set (Gloves)", "price": 50, "currency": "DKP", "max_per_person": 1, "category": "blue_equipment"},
                {"name": "Blue Armor Set (Boots)", "price": 50, "currency": "DKP", "max_per_person": 1, "category": "blue_equipment"},
                {"name": "Blue Wolf Set", "price": 100, "currency": "DKP", "max_per_person": 1, "category": "blue_equipment"},
                {"name": "Doom Set", "price": 100, "currency": "DKP", "max_per_person": 1, "category": "blue_equipment"},
                {"name": "Blue Weapon (Standard)", "price": 150, "currency": "DKP", "max_per_person": 1, "category": "blue_equipment"},
                {"name": "Giant Weapon", "price": 300, "currency": "DKP", "max_per_person": 1, "category": "blue_equipment"},
            ],
            "other_items": [
                {"name": "Bless Stone", "price": 15, "currency": "DKP", "max_per_person": 5, "category": "other_items"},
                {"name": "Purify Stone", "price": 15, "currency": "DKP", "max_per_person": 5, "category": "other_items"},
                {"name": "Elixir (HP/MP)", "price": 10, "currency": "DKP", "max_per_person": 10, "category": "other_items"},
                {"name": "Scroll Enchant Blessed (Weapon)", "price": 30, "currency": "DKP", "max_per_person": 3, "category": "other_items"},
                {"name": "Scroll Enchant Blessed (Armor)", "price": 25, "currency": "DKP", "max_per_person": 3, "category": "other_items"},
                {"name": "Scroll Enchant (Weapon)", "price": 20, "currency": "DKP", "max_per_person": 5, "category": "other_items"},
                {"name": "Scroll Enchant (Armor)", "price": 15, "currency": "DKP", "max_per_person": 5, "category": "other_items"},
            ],
            "diamond_items": [
                {"name": "Cursed Weapon", "price": 500, "currency": "Diamond", "max_per_person": 1, "category": "diamond_items"},
                {"name": "Cursed Armor", "price": 400, "currency": "Diamond", "max_per_person": 1, "category": "diamond_items"},
                {"name": "Ink (Tattoo Material)", "price": 200, "currency": "Diamond", "max_per_person": 3, "category": "diamond_items"},
                {"name": "Rare Enchant Scroll", "price": 300, "currency": "Diamond", "max_per_person": 2, "category": "diamond_items"},
            ],
        }
        return {
            "Valkyrie": default_items,
            "Valhalla": {
                "blue_books": [],
                "blue_equipment": [],
                "other_items": [],
                "diamond_items": [],
            }
        }


class TreasuryTransaction(models.Model):
    """Log every treasury item distribution"""
    profile = models.ForeignKey(DKPProfile, on_delete=models.CASCADE, related_name='treasury_logs')
    item_name = models.CharField("Item Name", max_length=200)
    item_category = models.CharField("Category", max_length=50)
    amount_deducted = models.IntegerField("Amount Deducted")
    currency = models.CharField("Currency", max_length=20, default='DKP')  # 'DKP' or 'Diamond'
    clan = models.CharField("Clan", max_length=50, default='Valkyrie')
    note = models.TextField("Note", blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Treasury Transaction"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.profile.character.name} received {self.item_name} (-{self.amount_deducted} {self.currency})"


class Auction(models.Model):
    """Auction item listing - admin creates, members bid via Discord"""
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('ACTIVE', 'Active'),
        ('CLOSED', 'Closed'),
        ('CANCELLED', 'Cancelled'),
    ]
    title = models.CharField("Item Name", max_length=200)
    description = models.TextField("Description", blank=True, default='')
    image = models.ImageField("Item Image", upload_to='auction/', blank=True, null=True)
    starting_bid = models.IntegerField("Starting Bid (DKP)", default=100)
    min_increment = models.IntegerField("Minimum Bid Increment", default=10)
    current_bid = models.IntegerField("Current Highest Bid", default=0)
    current_winner = models.ForeignKey(
        DKPProfile, null=True, blank=True, on_delete=models.SET_NULL,
        related_name='auction_leading'
    )
    duration_minutes = models.IntegerField("Duration (Minutes)", default=60)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    clan = models.CharField("Eligible Clan", max_length=50, default='All',
        help_text="'All' = both clans can bid, or 'Valkyrie'/'Valhalla' for specific clan")
    started_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    discord_message_id = models.CharField(max_length=50, blank=True, default='')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Auction"
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.status}] {self.title} - Bid: {self.current_bid} DKP"

    @property
    def is_expired(self):
        if self.status == 'ACTIVE' and self.ends_at:
            return timezone.now() >= self.ends_at
        return False

    @property
    def time_remaining(self):
        if self.status == 'ACTIVE' and self.ends_at:
            delta = self.ends_at - timezone.now()
            if delta.total_seconds() <= 0:
                return "Expired"
            m, s = divmod(int(delta.total_seconds()), 60)
            h, m = divmod(m, 60)
            d, h = divmod(h, 24)
            if d > 0:
                return f"{d}d {h}h {m}m"
            if h > 0:
                return f"{h}h {m}m"
            return f"{m}m {s}s"
        return "-"


class AuctionBid(models.Model):
    """Individual bid on an auction"""
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='bids')
    profile = models.ForeignKey(DKPProfile, on_delete=models.CASCADE, related_name='auction_bids')
    amount = models.IntegerField("Bid Amount (DKP)")
    is_winner = models.BooleanField(default=False)
    is_refunded = models.BooleanField("DKP Refunded", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Auction Bid"
        ordering = ['-amount']

    def __str__(self):
        return f"{self.profile.character.name} bid {self.amount} DKP on {self.auction.title}"

